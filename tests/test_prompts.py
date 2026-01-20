"""
Pytest tests for validating prompt structure.

This module implements 6 mandatory tests (FR-012) to validate that the
optimized prompt meets all structural requirements before evaluation.

Tests:
1. test_prompt_has_system_prompt - Verifies system_prompt exists and is non-empty
2. test_prompt_has_role_definition - Verifies "You are" or "Você é" pattern
3. test_prompt_mentions_format - Verifies "User Story" or "Markdown" mention
4. test_prompt_has_few_shot_examples - Verifies examples list has >= 1 item
5. test_prompt_no_todos - Verifies no "[TODO]" markers
6. test_minimum_techniques - Verifies metadata.techniques has >= 2 items

Usage:
    pytest tests/test_prompts.py
"""

import os
import sys
import re
import pytest
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import load_yaml


# Path to the optimized prompt file
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"


@pytest.fixture
def prompt_data():
    """
    Load the optimized prompt data from YAML file.

    Returns:
        Dictionary containing the prompt data.

    Raises:
        FileNotFoundError: If the prompt file does not exist.
    """
    if not PROMPT_PATH.exists():
        pytest.fail(
            f"Prompt file not found at {PROMPT_PATH}. "
            "Please create the optimized prompt first."
        )
    return load_yaml(str(PROMPT_PATH))


def test_prompt_has_system_prompt(prompt_data):
    """
    Verify that the prompt contains a non-empty system_prompt.

    The system_prompt is the core instruction set that guides the LLM's behavior.
    It must exist and contain actual content.

    Hint: Add a 'system_prompt' field with role definition and instructions.
    """
    assert 'system_prompt' in prompt_data, (
        "Prompt is missing required field: system_prompt. "
        "Hint: Add a 'system_prompt' field with role definition and instructions."
    )

    system_prompt = prompt_data['system_prompt']

    assert system_prompt is not None, (
        "system_prompt cannot be None. "
        "Hint: Provide actual content for the system prompt."
    )

    assert isinstance(system_prompt, str), (
        f"system_prompt must be a string, got {type(system_prompt).__name__}. "
        "Hint: Ensure system_prompt is a text value, not a list or dict."
    )

    assert len(system_prompt.strip()) > 0, (
        "system_prompt cannot be empty or whitespace-only. "
        "Hint: Add meaningful instructions that define the LLM's role and behavior."
    )


def test_prompt_has_role_definition(prompt_data):
    """
    Verify that the system_prompt contains a role definition pattern.

    Role Prompting is a key prompt engineering technique where we assign
    a specific persona to the LLM (e.g., "You are an experienced Product Manager").

    Expected patterns: "You are" or "Você é" (Portuguese)

    Hint: Add a clear role definition like "You are an experienced Product Manager"
    """
    assert 'system_prompt' in prompt_data, (
        "Cannot check role definition: system_prompt is missing."
    )

    system_prompt = prompt_data['system_prompt'].lower()

    # Check for role definition patterns
    has_english_role = 'you are' in system_prompt
    has_portuguese_role = 'você é' in system_prompt

    assert has_english_role or has_portuguese_role, (
        "System prompt must contain a role definition. "
        "Expected pattern: 'You are' or 'Você é'. "
        "Hint: Add a clear role definition like 'You are an experienced Product Manager "
        "with expertise in Agile methodologies.'"
    )


def test_prompt_mentions_format(prompt_data):
    """
    Verify that the system_prompt mentions the expected output format.

    The prompt should clearly specify that the output should be in User Story
    format and/or Markdown structure.

    Expected mentions: "User Story" or "Markdown"

    Hint: Add instructions about output format, e.g., "Format your response as a User Story in Markdown"
    """
    assert 'system_prompt' in prompt_data, (
        "Cannot check format mention: system_prompt is missing."
    )

    system_prompt = prompt_data['system_prompt'].lower()

    # Check for format mentions
    has_user_story = 'user story' in system_prompt
    has_markdown = 'markdown' in system_prompt

    assert has_user_story or has_markdown, (
        "System prompt must mention the output format. "
        "Expected mention: 'User Story' or 'Markdown'. "
        "Hint: Add instructions like 'Structure your response in Markdown with the "
        "following sections: User Story title, As a/I want/So that format, and "
        "Acceptance Criteria.'"
    )


def test_prompt_has_few_shot_examples(prompt_data):
    """
    Verify that the prompt contains at least one few-shot example.

    Few-shot learning is a prompt engineering technique where we provide
    input/output examples to guide the LLM's behavior.

    Each example should have 'input' (bug report) and 'output' (User Story).

    Hint: Add an 'examples' list with at least one {input: ..., output: ...} item
    """
    assert 'examples' in prompt_data, (
        "Prompt is missing required field: examples. "
        "Hint: Add an 'examples' list with few-shot input/output pairs."
    )

    examples = prompt_data['examples']

    assert isinstance(examples, list), (
        f"examples must be a list, got {type(examples).__name__}. "
        "Hint: Format examples as a YAML list with '- input:' and 'output:' items."
    )

    assert len(examples) >= 1, (
        f"examples must have at least 1 item, found {len(examples)}. "
        "Hint: Add at least one example showing how to convert a bug report to a User Story."
    )

    # Validate each example has required fields
    for i, example in enumerate(examples):
        assert 'input' in example, (
            f"Example {i} is missing required field: input. "
            "Hint: Each example needs an 'input' field with a sample bug report."
        )
        assert 'output' in example, (
            f"Example {i} is missing required field: output. "
            "Hint: Each example needs an 'output' field with the expected User Story."
        )
        assert example['input'], (
            f"Example {i} has empty input. "
            "Hint: Provide a realistic bug report as input."
        )
        assert example['output'], (
            f"Example {i} has empty output. "
            "Hint: Provide the expected User Story transformation as output."
        )


def test_prompt_no_todos(prompt_data):
    """
    Verify that the prompt contains no [TODO] markers.

    [TODO] markers indicate incomplete sections that need to be filled in.
    All placeholders must be resolved before the prompt is ready for use.

    Hint: Search for '[TODO]' in your prompt and replace with actual content
    """
    # Convert entire prompt to string for comprehensive check
    prompt_str = str(prompt_data)

    assert '[TODO]' not in prompt_str, (
        "Prompt contains [TODO] markers that must be resolved. "
        "Hint: Search for '[TODO]' in prompts/bug_to_user_story_v2.yml and "
        "replace all placeholders with actual content."
    )

    # Also check for common TODO variations
    prompt_lower = prompt_str.lower()
    todo_patterns = ['[todo]', '# todo', '// todo', '/* todo']

    for pattern in todo_patterns:
        assert pattern not in prompt_lower, (
            f"Prompt contains TODO marker: '{pattern}'. "
            "Hint: All TODO placeholders must be replaced with actual content."
        )


def test_minimum_techniques(prompt_data):
    """
    Verify that the prompt metadata lists at least 2 prompt engineering techniques.

    The techniques field in metadata documents which prompt engineering methods
    were applied (e.g., role_prompting, few_shot_learning, chain_of_thought).

    Expected: metadata.techniques list with >= 2 items

    Hint: Add techniques like 'role_prompting', 'few_shot_learning', 'chain_of_thought'
    """
    assert 'metadata' in prompt_data, (
        "Prompt is missing required field: metadata. "
        "Hint: Add a 'metadata' section with name, description, and techniques."
    )

    metadata = prompt_data['metadata']

    assert 'techniques' in metadata, (
        "metadata is missing required field: techniques. "
        "Hint: Add a 'techniques' list documenting the prompt engineering methods used."
    )

    techniques = metadata['techniques']

    assert isinstance(techniques, list), (
        f"metadata.techniques must be a list, got {type(techniques).__name__}. "
        "Hint: Format techniques as a YAML list, e.g., '- role_prompting'"
    )

    assert len(techniques) >= 2, (
        f"metadata.techniques must have at least 2 items, found {len(techniques)}. "
        "Hint: Apply and document at least 2 techniques. Recommended: "
        "role_prompting, few_shot_learning, chain_of_thought"
    )

    # Check that techniques are non-empty strings
    for i, technique in enumerate(techniques):
        assert isinstance(technique, str) and technique.strip(), (
            f"metadata.techniques[{i}] must be a non-empty string. "
            "Hint: Use descriptive technique names like 'role_prompting'."
        )


# Additional test for comprehensive validation (bonus)
def test_prompt_structure_complete(prompt_data):
    """
    Bonus test: Verify overall prompt structure is complete and valid.

    This test performs a comprehensive check of all required fields
    to ensure the prompt is ready for evaluation.
    """
    # Check metadata
    assert 'metadata' in prompt_data, "Missing metadata section"
    metadata = prompt_data['metadata']
    assert 'name' in metadata and metadata['name'], "Missing or empty metadata.name"
    assert 'description' in metadata and metadata['description'], "Missing or empty metadata.description"

    # Check system_prompt
    assert 'system_prompt' in prompt_data, "Missing system_prompt"
    assert len(prompt_data['system_prompt'].strip()) > 100, (
        "system_prompt seems too short. A good prompt should have detailed instructions."
    )

    # Check user_prompt_template
    assert 'user_prompt_template' in prompt_data, "Missing user_prompt_template"
    assert '{bug_report}' in prompt_data['user_prompt_template'], (
        "user_prompt_template must contain {bug_report} variable"
    )

    # Check examples
    assert 'examples' in prompt_data, "Missing examples"
    assert len(prompt_data['examples']) >= 1, "Need at least 1 example"
