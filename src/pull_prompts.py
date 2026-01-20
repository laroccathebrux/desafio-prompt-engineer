"""
Pull prompts from LangSmith Prompt Hub.

This module downloads the initial low-quality prompt from LangSmith Prompt Hub
and saves it locally in YAML format for analysis and optimization.

Usage:
    python src/pull_prompts.py

The prompt is saved to: prompts/bug_to_user_story_v1.yml
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils import load_env, save_yaml, print_error, print_success, validate_env_vars


# Configuration
PROMPT_NAME = "leonanluppi/bug_to_user_story_v1"
OUTPUT_PATH = "prompts/bug_to_user_story_v1.yml"


def load_credentials() -> bool:
    """
    Load environment variables from .env file.

    Validates that required LangSmith credentials are present.

    Returns:
        True if all required credentials are loaded, False otherwise.

    Example:
        >>> load_credentials()
        True
    """
    # Load .env file
    if not load_env():
        print_error("No .env file found. Please create one based on .env.example")
        return False

    # Validate required variables
    required_vars = ["LANGCHAIN_API_KEY"]
    return validate_env_vars(required_vars)


def pull_prompt(prompt_name: str) -> dict:
    """
    Pull a prompt from LangSmith Prompt Hub.

    Args:
        prompt_name: The fully qualified prompt name (e.g., 'user/prompt_name').

    Returns:
        Dictionary containing the prompt data.

    Raises:
        Exception: If the prompt cannot be pulled (authentication, network, etc.).

    Example:
        >>> prompt_data = pull_prompt("leonanluppi/bug_to_user_story_v1")
        >>> 'messages' in str(type(prompt_data))
        True
    """
    # Import using the modern LangSmith SDK API
    from langsmith import Client

    print(f"Pulling prompt from LangSmith Hub...")
    print(f"Prompt: {prompt_name}")

    client = Client()
    prompt = client.pull_prompt(prompt_name)
    return prompt


def convert_prompt_to_dict(prompt) -> dict:
    """
    Convert a LangChain prompt template to a dictionary for YAML storage.

    Args:
        prompt: A LangChain prompt template object.

    Returns:
        Dictionary representation of the prompt.

    Example:
        >>> prompt = pull_prompt("leonanluppi/bug_to_user_story_v1")
        >>> data = convert_prompt_to_dict(prompt)
        >>> isinstance(data, dict)
        True
    """
    prompt_dict = {
        "metadata": {
            "name": "bug_to_user_story_v1",
            "description": "Original prompt for converting bug reports to User Stories",
            "source": PROMPT_NAME,
            "techniques": [],
            "tags": ["bug-report", "user-story", "original"]
        }
    }

    # Extract messages from ChatPromptTemplate
    if hasattr(prompt, 'messages'):
        for message in prompt.messages:
            if hasattr(message, 'prompt'):
                template = message.prompt.template if hasattr(message.prompt, 'template') else str(message.prompt)
            else:
                template = str(message)

            # Determine message type
            message_type = type(message).__name__.lower()

            if 'system' in message_type:
                prompt_dict['system_prompt'] = template
            elif 'human' in message_type or 'user' in message_type:
                prompt_dict['user_prompt_template'] = template

    # Fallback: try to get template directly
    if 'system_prompt' not in prompt_dict:
        if hasattr(prompt, 'template'):
            prompt_dict['system_prompt'] = prompt.template
        else:
            prompt_dict['system_prompt'] = str(prompt)

    # Add empty examples section (to be filled in optimized version)
    prompt_dict['examples'] = []

    return prompt_dict


def save_prompt_to_yaml(prompt_data: dict, output_path: str) -> None:
    """
    Save prompt data to a YAML file.

    Args:
        prompt_data: Dictionary containing the prompt data.
        output_path: Path where the YAML file will be saved.

    Raises:
        OSError: If the file cannot be written.

    Example:
        >>> save_prompt_to_yaml({"name": "test"}, "prompts/test.yml")
    """
    save_yaml(prompt_data, output_path)
    print_success(f"Saved to: {output_path}")


def main() -> int:
    """
    Main entry point for the pull_prompts script.

    Downloads the prompt from LangSmith Hub and saves it locally.

    Returns:
        Exit code: 0 for success, 1 for error.

    Example:
        >>> # When .env is configured correctly:
        >>> exit_code = main()
        >>> exit_code == 0
        True
    """
    try:
        # Step 1: Load credentials
        if not load_credentials():
            return 1

        # Step 2: Pull prompt from LangSmith
        try:
            prompt = pull_prompt(PROMPT_NAME)
        except Exception as e:
            error_msg = str(e).lower()
            if 'auth' in error_msg or '401' in error_msg or '403' in error_msg:
                print_error("Authentication failed. Please check your LANGCHAIN_API_KEY in .env")
            elif 'connection' in error_msg or 'network' in error_msg or 'timeout' in error_msg:
                print_error("Unable to connect to LangSmith Hub. Please check your internet connection.")
            else:
                print_error(f"Failed to pull prompt: {e}")
            return 1

        # Step 3: Convert to dictionary format
        prompt_dict = convert_prompt_to_dict(prompt)

        # Step 4: Save to YAML file
        try:
            save_prompt_to_yaml(prompt_dict, OUTPUT_PATH)
        except OSError as e:
            print_error(f"Failed to write file: {e}")
            return 1

        print_success("Pull completed successfully!")
        return 0

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
