# CLI Interface Contracts

**Feature**: 001-prompt-optimization
**Date**: 2026-01-20

## Overview

This document defines the command-line interface contracts for all scripts in the prompt optimization workflow.

## Scripts

### 1. pull_prompts.py

**Purpose**: Download prompts from LangSmith Prompt Hub to local YAML files.

**Command**:
```bash
python src/pull_prompts.py
```

**Environment Variables Required**:
- `LANGCHAIN_API_KEY` - LangSmith API key

**Input**: None (prompt identifier hardcoded: `leonanluppi/bug_to_user_story_v1`)

**Output**:
- **Success**:
  ```
  Pulling prompt from LangSmith Hub...
  Prompt: leonanluppi/bug_to_user_story_v1
  Saved to: prompts/bug_to_user_story_v1.yml
  Pull completed successfully!
  ```
- **Failure** (authentication):
  ```
  Error: Authentication failed. Please check your LANGCHAIN_API_KEY in .env
  ```
- **Failure** (network):
  ```
  Error: Unable to connect to LangSmith Hub. Please check your internet connection.
  ```

**Exit Codes**:
- `0`: Success
- `1`: Error (authentication, network, or file write failure)

**Side Effects**:
- Creates/overwrites `prompts/bug_to_user_story_v1.yml`

---

### 2. push_prompts.py

**Purpose**: Upload optimized prompt to LangSmith Prompt Hub with metadata.

**Command**:
```bash
python src/push_prompts.py
```

**Environment Variables Required**:
- `LANGCHAIN_API_KEY` - LangSmith API key

**Input**: Reads from `prompts/bug_to_user_story_v2.yml`

**Output**:
- **Success**:
  ```
  Reading optimized prompt from prompts/bug_to_user_story_v2.yml...
  Pushing to LangSmith Hub...
  Prompt published: {username}/bug_to_user_story_v2
  Visibility: Public
  Tags: prompt-engineering, user-story, bug-report
  Techniques: role_prompting, few_shot_learning, chain_of_thought
  Push completed successfully!
  ```
- **Failure** (file not found):
  ```
  Error: Optimized prompt file not found at prompts/bug_to_user_story_v2.yml
  Please create the optimized prompt first.
  ```
- **Failure** (validation):
  ```
  Error: Invalid prompt structure. Missing required field: system_prompt
  ```
- **Failure** (authentication):
  ```
  Error: Authentication failed. Please check your LANGCHAIN_API_KEY in .env
  ```

**Exit Codes**:
- `0`: Success
- `1`: Error

**Side Effects**:
- Creates/updates prompt in LangSmith Hub
- Sets prompt visibility to public

---

### 3. evaluate.py

**Purpose**: Run automated evaluation of prompts against 4 quality metrics.

**Command**:
```bash
python src/evaluate.py
```

**Environment Variables Required**:
- `LANGCHAIN_API_KEY` - LangSmith API key
- `OPENAI_API_KEY` or `GOOGLE_API_KEY` - LLM provider

**Input**: Uses dataset from `src/dataset.py` and prompt from LangSmith Hub

**Output**:
- **Success** (Approved):
  ```
  Executando avaliação dos prompts...
  ================================
  Prompt: {username}/bug_to_user_story_v2
  - Tone Score: 0.94
  - Acceptance Criteria Score: 0.92
  - User Story Format Score: 0.95
  - Completeness Score: 0.91
  ================================
  Average: 0.93
  Status: APROVADO ✓ - Todas as métricas atingiram o mínimo de 0.9
  ```
- **Success** (Failed):
  ```
  Executando avaliação dos prompts...
  ================================
  Prompt: {username}/bug_to_user_story_v2
  - Tone Score: 0.85
  - Acceptance Criteria Score: 0.78
  - User Story Format Score: 0.88
  - Completeness Score: 0.72
  ================================
  Average: 0.81
  Status: FALHOU - Métricas abaixo do mínimo de 0.9

  Métricas que precisam melhorar:
  - Acceptance Criteria Score: 0.78 (precisa +0.12)
  - Completeness Score: 0.72 (precisa +0.18)
  ```
- **Failure** (provider not configured):
  ```
  Error: No LLM provider configured. Set OPENAI_API_KEY or GOOGLE_API_KEY in .env
  ```

**Exit Codes**:
- `0`: Evaluation completed (regardless of pass/fail)
- `1`: Error (missing configuration, API failure)

**Side Effects**:
- Creates evaluation traces in LangSmith dashboard
- Logs detailed results for debugging

---

### 4. test_prompts.py (pytest)

**Purpose**: Validate prompt structure meets requirements.

**Command**:
```bash
pytest tests/test_prompts.py
```

**Input**: Reads from `prompts/bug_to_user_story_v2.yml`

**Output**:
- **All tests pass**:
  ```
  ======================== test session starts ========================
  tests/test_prompts.py::test_prompt_has_system_prompt PASSED
  tests/test_prompts.py::test_prompt_has_role_definition PASSED
  tests/test_prompts.py::test_prompt_mentions_format PASSED
  tests/test_prompts.py::test_prompt_has_few_shot_examples PASSED
  tests/test_prompts.py::test_prompt_no_todos PASSED
  tests/test_prompts.py::test_minimum_techniques PASSED
  ======================== 6 passed in 0.15s ==========================
  ```
- **Test failure example**:
  ```
  tests/test_prompts.py::test_prompt_has_role_definition FAILED

  AssertionError: System prompt must contain role definition.
  Expected pattern: "You are" or "Você é"
  Found: System prompt does not define a persona.

  Hint: Add a clear role definition like "You are an experienced Product Manager"
  ```

**Exit Codes**:
- `0`: All tests pass
- `1`: One or more tests fail

---

## Complete Workflow

```bash
# Step 1: Pull initial prompt
python src/pull_prompts.py

# Step 2: Create/edit optimized prompt
# (manual editing of prompts/bug_to_user_story_v2.yml)

# Step 3: Validate structure
pytest tests/test_prompts.py

# Step 4: Push to LangSmith
python src/push_prompts.py

# Step 5: Evaluate
python src/evaluate.py

# Step 6: If FAILED, iterate (repeat steps 2-5)
```

## Error Handling Patterns

All scripts follow this error handling pattern:

```python
def main():
    """Main entry point with comprehensive error handling."""
    try:
        # ... main logic ...
        return 0
    except AuthenticationError as e:
        print(f"Error: Authentication failed. {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"Error: File not found. {e}", file=sys.stderr)
        return 1
    except ValidationError as e:
        print(f"Error: Validation failed. {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: Unexpected error. {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
```
