# Implementation Plan: LangSmith Prompt Optimization Challenge

**Branch**: `001-prompt-optimization` | **Date**: 2026-01-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-prompt-optimization/spec.md`

## Summary

Build a prompt engineering system that pulls low-quality prompts from LangSmith Prompt Hub, optimizes them using advanced techniques (Few-shot Learning, Chain of Thought, Role Prompting), and achieves >= 0.9 scores on all 4 evaluation metrics (Tone, Acceptance Criteria, User Story Format, Completeness). The system transforms bug reports into well-structured User Stories.

## Technical Context

**Language/Version**: Python 3.9+
**Primary Dependencies**: LangChain, LangSmith, langchain-openai, langchain-google-genai, python-dotenv, PyYAML
**Storage**: Local YAML files in `prompts/` directory
**Testing**: pytest (6 mandatory test cases for prompt validation)
**Target Platform**: Local development (macOS/Linux/Windows with conda environment `desafio_02`)
**Project Type**: Single project (CLI scripts)
**Performance Goals**: All 4 evaluation metrics >= 0.9 (90%)
**Constraints**: 3-5 iterations expected to achieve threshold; Gemini free tier: 15 req/min, 1500 req/day
**Scale/Scope**: 15 bug examples in dataset (5 simple, 7 medium, 3 complex)

### LLM Provider Options

| Provider | Response Model | Evaluation Model | Cost |
|----------|---------------|------------------|------|
| OpenAI | gpt-4o-mini | gpt-4o | ~$1-5 |
| Gemini | gemini-2.5-flash | gemini-2.5-flash | Free (rate limited) |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Code Quality ✅

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Python 3.9+ compatible | ✅ | Using conda environment `desafio_02` |
| Proper error handling | ✅ | All scripts will include try/except with descriptive messages |
| Environment variables from .env | ✅ | Using python-dotenv for credentials |
| YAML validation | ✅ | PyYAML with schema validation |
| Single responsibility functions | ✅ | Modular design per script |
| No hardcoded credentials | ✅ | All API keys in .env file |
| Import ordering | ✅ | stdlib → third-party → local |
| **Docstrings on all code** | ✅ | **Required for teacher audit (FR-013)** |

### II. Testing Standards ✅

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| pytest framework | ✅ | `tests/test_prompts.py` |
| 6 mandatory test cases | ✅ | All tests defined in spec |
| Runnable via `pytest tests/test_prompts.py` | ✅ | Standard pytest execution |
| Actionable test failures | ✅ | Clear assertion messages |

### III. User Experience Consistency ✅

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Clear role definition | ✅ | System prompt with persona |
| System vs User prompt separation | ✅ | YAML structure with distinct fields |
| Output format specified | ✅ | User Story format with Markdown |
| Edge cases handled | ✅ | Instructions for empty/malformed input |
| Few-shot examples | ✅ | 2-3 examples in prompt |
| YAML format in prompts/ | ✅ | `prompts/bug_to_user_story_v2.yml` |

### IV. Performance Requirements ✅

| Metric | Target | Validation |
|--------|--------|------------|
| Tone Score | >= 0.9 | `python src/evaluate.py` |
| Acceptance Criteria Score | >= 0.9 | `python src/evaluate.py` |
| User Story Format Score | >= 0.9 | `python src/evaluate.py` |
| Completeness Score | >= 0.9 | `python src/evaluate.py` |
| All metrics pass individually | ✅ | Not just average |

**Constitution Check: PASSED** ✅

## Project Structure

### Documentation (this feature)

```text
specs/001-prompt-optimization/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (CLI contracts)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/
├── pull_prompts.py      # Pull from LangSmith Hub
├── push_prompts.py      # Push to LangSmith namespace
├── evaluate.py          # Run evaluation against metrics
├── metrics.py           # 4 metric implementations (provided, do not modify)
├── dataset.py           # 15 bug examples (provided, do not modify)
└── utils.py             # Helper functions

prompts/
├── bug_to_user_story_v1.yml    # Original prompt (from pull)
└── bug_to_user_story_v2.yml    # Optimized prompt (deliverable)

tests/
└── test_prompts.py      # 6 validation tests
```

**Structure Decision**: Single project structure with CLI scripts. No web/mobile components. All scripts are standalone Python modules executed via command line.

## Complexity Tracking

> No violations - all requirements align with Constitution principles.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Single project | Selected | CLI-only workflow, no frontend/backend split needed |
| File-based storage | Selected | YAML files sufficient for prompt management |
| No database | N/A | LangSmith handles cloud storage |

## Docstring Requirements

**IMPORTANT**: All Python code MUST include comprehensive docstrings for academic audit (FR-013):

```python
"""
Module docstring explaining the purpose of the file.

This module handles [specific functionality].
"""

def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description of what the function does.

    Args:
        param1: Description of first parameter
        param2: Description of second parameter

    Returns:
        Description of return value

    Raises:
        ExceptionType: When this exception is raised

    Example:
        >>> function_name("example", 42)
        "result"
    """
```

## Prompt Engineering Techniques

### Selected Techniques (minimum 2 required)

1. **Role Prompting**: Define a clear persona (Product Manager/Business Analyst)
   - Provides context and expertise framing
   - Helps maintain consistent tone and format

2. **Few-shot Learning**: Include 2-3 input/output examples
   - Demonstrates expected transformation
   - Reduces ambiguity in output format

3. **Chain of Thought (CoT)**: Step-by-step reasoning
   - Useful for complex bug analysis
   - Improves completeness of User Story

### Prompt Structure

```yaml
metadata:
  name: bug_to_user_story_v2
  description: Optimized prompt for converting bug reports to User Stories
  techniques:
    - role_prompting
    - few_shot_learning
    - chain_of_thought
  tags:
    - prompt-engineering
    - user-story
    - bug-report

system_prompt: |
  You are an experienced Product Manager...
  [Role definition with context]

  Follow these steps to transform the bug report:
  1. Analyze the bug report
  2. Identify the user type affected
  3. Extract the desired behavior
  4. Write acceptance criteria
  [Chain of Thought instructions]

user_prompt_template: |
  Bug Report:
  {bug_report}

  Transform this into a User Story following the format:
  - As a [user type]
  - I want [goal]
  - So that [benefit]

  Include:
  - Acceptance Criteria (Given/When/Then)
  - Priority suggestion
  - Technical notes if relevant

examples:
  - input: |
      Title: Login button not working
      Description: Users cannot click the login button on mobile
      Severity: High
    output: |
      ## User Story: Fix Mobile Login Button

      **As a** mobile user
      **I want** to click the login button successfully
      **So that** I can access my account on mobile devices

      ### Acceptance Criteria
      - Given I am on the login page on mobile
      - When I tap the login button
      - Then I should be logged in or see validation errors

      **Priority**: High
      **Technical Notes**: Check touch event handling on mobile browsers
```
