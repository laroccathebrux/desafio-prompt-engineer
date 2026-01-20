"""
Evaluate prompts against quality metrics using LangSmith.

This module runs automated evaluation of prompts against 4 quality metrics:
- Tone Score: Language appropriateness and professionalism
- Acceptance Criteria Score: Quality of acceptance criteria
- User Story Format Score: Adherence to User Story format
- Completeness Score: Coverage of all bug aspects

Usage:
    python src/evaluate.py

Target: All metrics >= 0.9 for APPROVED status.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils import load_env, load_yaml, print_error, print_success, validate_env_vars
from metrics import METRICS, PASSING_THRESHOLD, evaluate_all
from dataset import get_all_bugs, format_bug_for_prompt


# Configuration
PROMPT_PATH = "prompts/bug_to_user_story_v2.yml"


def get_llm_provider() -> tuple:
    """
    Detect which LLM provider is configured from environment variables.

    Checks for OPENAI_API_KEY first, then GOOGLE_API_KEY.

    Returns:
        Tuple of (provider_name, api_key) where provider_name is 'openai' or 'google'.

    Raises:
        ValueError: If no LLM provider is configured.

    Example:
        >>> # When OPENAI_API_KEY is set:
        >>> provider, key = get_llm_provider()
        >>> provider in ['openai', 'google']
        True
    """
    openai_key = os.environ.get('OPENAI_API_KEY')
    google_key = os.environ.get('GOOGLE_API_KEY')

    if openai_key:
        return ('openai', openai_key)
    elif google_key:
        return ('google', google_key)
    else:
        raise ValueError("No LLM provider configured. Set OPENAI_API_KEY or GOOGLE_API_KEY in .env")


def create_llm(provider: str):
    """
    Create an LLM instance based on the provider.

    Args:
        provider: Either 'openai' or 'google'.

    Returns:
        A LangChain LLM instance.

    Raises:
        ValueError: If provider is not supported.

    Example:
        >>> # When credentials are configured:
        >>> llm = create_llm('openai')
        >>> llm is not None
        True
    """
    if provider == 'openai':
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    elif provider == 'google':
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def create_prompt_chain(prompt_data: Dict[str, Any], llm):
    """
    Create a LangChain prompt chain from the YAML prompt data.

    Args:
        prompt_data: Dictionary containing the prompt data from YAML.
        llm: A LangChain LLM instance.

    Returns:
        A LangChain runnable chain.

    Example:
        >>> # When prompt_data and llm are configured:
        >>> chain = create_prompt_chain(prompt_data, llm)
        >>> chain is not None
        True
    """
    from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

    system_prompt = prompt_data.get('system_prompt', '')
    user_template = prompt_data.get('user_prompt_template', '{bug_report}')

    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_prompt),
        HumanMessagePromptTemplate.from_template(user_template)
    ])

    chain = prompt_template | llm

    return chain


def run_evaluation(chain, bugs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Run the evaluation on all bugs using the prompt chain.

    Args:
        chain: A LangChain runnable chain.
        bugs: List of bug report dictionaries.

    Returns:
        List of evaluation results, each containing input, output, and scores.

    Example:
        >>> # When chain and bugs are configured:
        >>> results = run_evaluation(chain, bugs)
        >>> len(results) == len(bugs)
        True
    """
    results = []

    for bug in bugs:
        # Format the bug for the prompt
        bug_text = format_bug_for_prompt(bug)

        try:
            # Generate the User Story
            response = chain.invoke({"bug_report": bug_text})
            output = response.content if hasattr(response, 'content') else str(response)

            # Evaluate with all metrics
            scores = evaluate_all(output, bug)

            results.append({
                "bug_id": bug.get('id', 'unknown'),
                "bug_title": bug.get('title', 'Unknown'),
                "input": bug_text,
                "output": output,
                "scores": scores
            })

        except Exception as e:
            print_error(f"Error processing bug {bug.get('id', 'unknown')}: {e}")
            results.append({
                "bug_id": bug.get('id', 'unknown'),
                "bug_title": bug.get('title', 'Unknown'),
                "input": bug_text,
                "output": "",
                "scores": {k: 0.0 for k in METRICS.keys()},
                "error": str(e)
            })

    return results


def calculate_scores(results: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Aggregate metric results from all evaluations.

    Args:
        results: List of evaluation results from run_evaluation().

    Returns:
        Dictionary with average scores for each metric.

    Example:
        >>> results = [{"scores": {"tone_score": 0.9}}]
        >>> avg_scores = calculate_scores(results)
        >>> 'tone_score' in avg_scores
        True
    """
    if not results:
        return {k: 0.0 for k in METRICS.keys()}

    # Initialize accumulators
    totals = {k: 0.0 for k in METRICS.keys()}
    count = len(results)

    # Sum all scores
    for result in results:
        scores = result.get('scores', {})
        for metric in METRICS.keys():
            totals[metric] += scores.get(metric, 0.0)

    # Calculate averages
    averages = {k: round(v / count, 2) for k, v in totals.items()}

    # Calculate overall average
    averages['average'] = round(sum(averages[k] for k in METRICS.keys()) / len(METRICS), 2)

    # Determine status
    all_passing = all(averages[k] >= PASSING_THRESHOLD for k in METRICS.keys())
    averages['status'] = 'APPROVED' if all_passing else 'FAILED'

    return averages


def display_results(scores: Dict[str, float], prompt_name: str) -> None:
    """
    Display evaluation results with APPROVED/FAILED status.

    Shows all metric scores and highlights which metrics need improvement.

    Args:
        scores: Dictionary with metric scores from calculate_scores().
        prompt_name: Name of the prompt being evaluated.

    Example:
        >>> scores = {"tone_score": 0.9, "status": "APPROVED", "average": 0.9}
        >>> display_results(scores, "test_prompt")
    """
    print("\nExecutando avaliação dos prompts...")
    print("=" * 40)
    print(f"Prompt: {prompt_name}")

    # Display individual metric scores
    for metric in METRICS.keys():
        score = scores.get(metric, 0.0)
        status_icon = "✓" if score >= PASSING_THRESHOLD else "✗"
        metric_display = metric.replace('_', ' ').title().replace(' Score', '')
        print(f"  {status_icon} {metric_display} Score: {score}")

    print("=" * 40)
    print(f"Average: {scores.get('average', 0.0)}")

    # Display status
    status = scores.get('status', 'FAILED')
    if status == 'APPROVED':
        print(f"Status: APROVADO ✓ - Todas as métricas atingiram o mínimo de {PASSING_THRESHOLD}")
    else:
        print(f"Status: FALHOU - Métricas abaixo do mínimo de {PASSING_THRESHOLD}")
        print()
        print("Métricas que precisam melhorar:")

        # Show which metrics need improvement with delta
        for metric in METRICS.keys():
            score = scores.get(metric, 0.0)
            if score < PASSING_THRESHOLD:
                delta = round(PASSING_THRESHOLD - score, 2)
                metric_display = metric.replace('_', ' ').title().replace(' Score', '')
                print(f"  - {metric_display} Score: {score} (precisa +{delta})")


def main() -> int:
    """
    Main entry point for the evaluate script.

    Loads prompt, runs evaluation against dataset, and displays results.

    Returns:
        Exit code: 0 for success (evaluation completed), 1 for error.

    Example:
        >>> # When all configuration is correct:
        >>> exit_code = main()
        >>> exit_code in [0, 1]
        True
    """
    try:
        # Step 1: Load environment
        if not load_env():
            print_error("No .env file found. Please create one based on .env.example")
            return 1

        required_vars = ["LANGCHAIN_API_KEY"]
        if not validate_env_vars(required_vars):
            return 1

        # Step 2: Check LLM provider
        try:
            provider, _ = get_llm_provider()
            print(f"Using LLM provider: {provider}")
        except ValueError as e:
            print_error(str(e))
            return 1

        # Step 3: Load prompt from YAML
        if not os.path.exists(PROMPT_PATH):
            print_error(f"Prompt file not found at {PROMPT_PATH}")
            print("Please create the optimized prompt first.")
            return 1

        prompt_data = load_yaml(PROMPT_PATH)
        prompt_name = prompt_data.get('metadata', {}).get('name', 'unknown')

        # Step 4: Create LLM and chain
        try:
            llm = create_llm(provider)
            chain = create_prompt_chain(prompt_data, llm)
        except Exception as e:
            print_error(f"Failed to initialize LLM: {e}")
            return 1

        # Step 5: Get dataset
        bugs = get_all_bugs()
        print(f"Evaluating with {len(bugs)} bug reports...")

        # Step 6: Run evaluation
        try:
            results = run_evaluation(chain, bugs)
        except Exception as e:
            error_msg = str(e).lower()
            if 'auth' in error_msg or '401' in error_msg or '403' in error_msg:
                print_error("API authentication failed. Please check your API keys in .env")
            elif 'rate' in error_msg or 'quota' in error_msg:
                print_error("API rate limit exceeded. Please wait and try again.")
            else:
                print_error(f"Evaluation failed: {e}")
            return 1

        # Step 7: Calculate and display results
        scores = calculate_scores(results)
        display_results(scores, prompt_name)

        print_success("Evaluation completed!")
        return 0

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
