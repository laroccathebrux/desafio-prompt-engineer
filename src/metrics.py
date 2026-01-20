"""
Evaluation Metrics for the LangSmith Prompt Optimization Challenge.

This module implements 4 custom metrics to evaluate the quality of
User Stories generated from bug reports:

1. Tone Score: Evaluates language appropriateness and professionalism
2. Acceptance Criteria Score: Evaluates quality of acceptance criteria
3. User Story Format Score: Evaluates adherence to standard User Story format
4. Completeness Score: Evaluates coverage of all bug aspects

Each metric returns a score between 0.0 and 1.0, where >= 0.9 is passing.
"""

import re
from typing import Dict, Any, Callable


def evaluate_tone(output: str, reference: Dict[str, Any] = None) -> float:
    """
    Evaluate the tone and professionalism of the generated User Story.

    Checks for:
    - Professional language (no casual/inappropriate terms)
    - Clear and concise writing
    - Appropriate formatting
    - Constructive framing (solutions not just problems)

    Args:
        output: The generated User Story text.
        reference: Optional reference data (bug report) for context.

    Returns:
        Score between 0.0 and 1.0.

    Example:
        >>> score = evaluate_tone("## User Story\\n\\n**As a** user...")
        >>> 0.0 <= score <= 1.0
        True
    """
    if not output or not output.strip():
        return 0.0

    score = 0.0
    checks_passed = 0
    total_checks = 5

    # Check 1: Uses professional language (no casual terms)
    casual_terms = ['stuff', 'thing', 'whatever', 'kinda', 'gonna', 'wanna', 'lol', 'btw']
    if not any(term in output.lower() for term in casual_terms):
        checks_passed += 1

    # Check 2: Uses proper sentence structure (starts with capital, ends with punctuation)
    sentences = re.split(r'[.!?]', output)
    proper_sentences = sum(1 for s in sentences if s.strip() and s.strip()[0].isupper())
    if proper_sentences >= len([s for s in sentences if s.strip()]) * 0.8:
        checks_passed += 1

    # Check 3: Contains structured headers (markdown formatting)
    if re.search(r'^#+\s+', output, re.MULTILINE) or '**' in output:
        checks_passed += 1

    # Check 4: Focuses on solution/improvement rather than just problem
    solution_words = ['want', 'need', 'should', 'will', 'can', 'able', 'improve', 'ensure', 'enable']
    if any(word in output.lower() for word in solution_words):
        checks_passed += 1

    # Check 5: Reasonable length (not too short or too long)
    word_count = len(output.split())
    if 50 <= word_count <= 500:
        checks_passed += 1

    score = checks_passed / total_checks
    return round(score, 2)


def evaluate_acceptance_criteria(output: str, reference: Dict[str, Any] = None) -> float:
    """
    Evaluate the quality of acceptance criteria in the User Story.

    Checks for:
    - Presence of acceptance criteria section
    - Given/When/Then format (or equivalent)
    - Testable conditions
    - Coverage of main scenario and edge cases

    Args:
        output: The generated User Story text.
        reference: Optional reference data (bug report) for context.

    Returns:
        Score between 0.0 and 1.0.

    Example:
        >>> output = "### Acceptance Criteria\\n- Given... When... Then..."
        >>> score = evaluate_acceptance_criteria(output)
        >>> score > 0.5
        True
    """
    if not output or not output.strip():
        return 0.0

    score = 0.0
    checks_passed = 0
    total_checks = 5

    output_lower = output.lower()

    # Check 1: Contains acceptance criteria section
    ac_patterns = ['acceptance criteria', 'acceptance scenario', 'criteria', 'scenarios']
    if any(pattern in output_lower for pattern in ac_patterns):
        checks_passed += 1

    # Check 2: Uses Given/When/Then format
    gwt_patterns = [
        (r'given\s+.+', r'when\s+.+', r'then\s+.+'),
        ('given', 'when', 'then'),
        ('precondition', 'action', 'result')
    ]
    for patterns in gwt_patterns:
        if all(re.search(p, output_lower) for p in patterns if isinstance(p, str)):
            checks_passed += 1
            break
        if isinstance(patterns[0], str) and all(p in output_lower for p in patterns):
            checks_passed += 1
            break

    # Check 3: Has multiple criteria (at least 2 bullet points or numbered items)
    bullet_count = len(re.findall(r'^[\s]*[-*•]\s+', output, re.MULTILINE))
    numbered_count = len(re.findall(r'^\s*\d+[.)]\s+', output, re.MULTILINE))
    if bullet_count >= 2 or numbered_count >= 2:
        checks_passed += 1

    # Check 4: Criteria are testable (contain verifiable actions/states)
    testable_words = ['should', 'must', 'will', 'is', 'are', 'displays', 'shows', 'returns', 'receives']
    testable_count = sum(1 for word in testable_words if word in output_lower)
    if testable_count >= 3:
        checks_passed += 1

    # Check 5: Mentions expected outcome
    outcome_words = ['expected', 'result', 'outcome', 'then', 'should see', 'should be']
    if any(word in output_lower for word in outcome_words):
        checks_passed += 1

    score = checks_passed / total_checks
    return round(score, 2)


def evaluate_user_story_format(output: str, reference: Dict[str, Any] = None) -> float:
    """
    Evaluate adherence to standard User Story format.

    Checks for:
    - "As a [user type]" statement
    - "I want [goal]" statement
    - "So that [benefit]" statement
    - Proper markdown structure
    - Clear title

    Args:
        output: The generated User Story text.
        reference: Optional reference data (bug report) for context.

    Returns:
        Score between 0.0 and 1.0.

    Example:
        >>> output = "**As a** user **I want** to login **So that** I can access"
        >>> score = evaluate_user_story_format(output)
        >>> score > 0.6
        True
    """
    if not output or not output.strip():
        return 0.0

    score = 0.0
    checks_passed = 0
    total_checks = 5

    output_lower = output.lower()

    # Check 1: Contains "As a [user type]" pattern
    as_a_patterns = [
        r'as\s+a[n]?\s+\w+',
        r'\*\*as\s+a[n]?\*\*',
        r'como\s+um[a]?\s+\w+'  # Portuguese
    ]
    if any(re.search(p, output_lower) for p in as_a_patterns):
        checks_passed += 1

    # Check 2: Contains "I want [goal]" pattern
    i_want_patterns = [
        r'i\s+want\s+',
        r'\*\*i\s+want\*\*',
        r'eu\s+quero'  # Portuguese
    ]
    if any(re.search(p, output_lower) for p in i_want_patterns):
        checks_passed += 1

    # Check 3: Contains "So that [benefit]" pattern
    so_that_patterns = [
        r'so\s+that\s+',
        r'\*\*so\s+that\*\*',
        r'para\s+que'  # Portuguese
    ]
    if any(re.search(p, output_lower) for p in so_that_patterns):
        checks_passed += 1

    # Check 4: Has title/header
    title_patterns = [
        r'^#+ .+',  # Markdown header
        r'^user story:',
        r'^\*\*.+\*\*'  # Bold text at start
    ]
    if any(re.search(p, output_lower, re.MULTILINE) for p in title_patterns):
        checks_passed += 1

    # Check 5: Contains structured sections (headers, bullets, or numbered lists)
    has_structure = bool(
        re.search(r'^#+\s+', output, re.MULTILINE) or
        re.search(r'^[\s]*[-*•]\s+', output, re.MULTILINE) or
        re.search(r'^\s*\d+[.)]\s+', output, re.MULTILINE)
    )
    if has_structure:
        checks_passed += 1

    score = checks_passed / total_checks
    return round(score, 2)


def evaluate_completeness(output: str, reference: Dict[str, Any] = None) -> float:
    """
    Evaluate how completely the User Story covers the bug report.

    Checks for:
    - Addresses the core issue from bug report
    - Includes relevant context
    - Mentions priority/severity
    - Considers edge cases or technical notes
    - Sufficient detail level

    Args:
        output: The generated User Story text.
        reference: Optional reference data (bug report) for context.

    Returns:
        Score between 0.0 and 1.0.

    Example:
        >>> output = "## Fix Login Bug\\n\\nAs a user...\\n\\n### Priority: High"
        >>> score = evaluate_completeness(output)
        >>> score > 0.5
        True
    """
    if not output or not output.strip():
        return 0.0

    score = 0.0
    checks_passed = 0
    total_checks = 5

    output_lower = output.lower()

    # Check 1: Sufficient length (indicates detailed coverage)
    word_count = len(output.split())
    if word_count >= 75:
        checks_passed += 1

    # Check 2: Mentions priority or severity
    priority_words = ['priority', 'severity', 'critical', 'high', 'medium', 'low', 'urgent']
    if any(word in output_lower for word in priority_words):
        checks_passed += 1

    # Check 3: Contains technical context or notes
    tech_patterns = ['technical', 'note', 'implementation', 'backend', 'frontend', 'api', 'database', 'fix']
    if any(pattern in output_lower for pattern in tech_patterns):
        checks_passed += 1

    # Check 4: Has multiple sections (indicates comprehensive coverage)
    section_markers = re.findall(r'^#+\s+', output, re.MULTILINE)
    if len(section_markers) >= 2:
        checks_passed += 1

    # Check 5: Addresses user impact or benefit
    impact_words = ['user', 'customer', 'benefit', 'experience', 'access', 'able to', 'can']
    impact_count = sum(1 for word in impact_words if word in output_lower)
    if impact_count >= 2:
        checks_passed += 1

    score = checks_passed / total_checks
    return round(score, 2)


# Metric registry for evaluation framework
METRICS: Dict[str, Callable] = {
    "tone_score": evaluate_tone,
    "acceptance_criteria_score": evaluate_acceptance_criteria,
    "user_story_format_score": evaluate_user_story_format,
    "completeness_score": evaluate_completeness
}

# Passing threshold for all metrics
PASSING_THRESHOLD = 0.9


def evaluate_all(output: str, reference: Dict[str, Any] = None) -> Dict[str, float]:
    """
    Run all metrics on the given output.

    Args:
        output: The generated User Story text.
        reference: Optional reference data (bug report) for context.

    Returns:
        Dictionary with all metric scores and overall status.

    Example:
        >>> results = evaluate_all("## User Story\\n\\n**As a** user...")
        >>> 'tone_score' in results
        True
        >>> 'average' in results
        True
    """
    results = {}

    for metric_name, metric_func in METRICS.items():
        results[metric_name] = metric_func(output, reference)

    # Calculate average
    results['average'] = round(
        sum(results[k] for k in METRICS.keys()) / len(METRICS),
        2
    )

    # Determine pass/fail status
    all_passing = all(results[k] >= PASSING_THRESHOLD for k in METRICS.keys())
    results['status'] = 'APPROVED' if all_passing else 'FAILED'

    return results


if __name__ == "__main__":
    # Test with a sample User Story
    sample_output = """
## User Story: Fix Mobile Login Button

**As a** mobile user
**I want** to click the login button successfully
**So that** I can access my account on mobile devices

### Acceptance Criteria

- Given I am on the login page on a mobile device
- When I tap the login button
- Then I should be logged in or see validation errors

- Given I enter invalid credentials
- When I tap the login button
- Then I should see an appropriate error message

### Priority: High

### Technical Notes
- Check touch event handling on mobile browsers
- Verify button z-index and clickable area
- Test on iOS Safari and Android Chrome
"""

    print("Metrics Evaluation Test")
    print("=" * 40)
    results = evaluate_all(sample_output)

    for metric, score in results.items():
        if metric in ['average', 'status']:
            continue
        status = "✓" if score >= PASSING_THRESHOLD else "✗"
        print(f"{status} {metric}: {score}")

    print("-" * 40)
    print(f"Average: {results['average']}")
    print(f"Status: {results['status']}")
