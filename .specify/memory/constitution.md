<!--
  SYNC IMPACT REPORT
  ===================
  Version change: N/A (initial) → 1.0.0

  Added sections:
  - Core Principles (4 new principles)
  - Evaluation Standards
  - Development Workflow
  - Governance

  Removed sections: None (initial version)

  Templates requiring updates:
  - ✅ plan-template.md - Compatible (Constitution Check section present)
  - ✅ spec-template.md - Compatible (User Scenarios and Requirements sections present)
  - ✅ tasks-template.md - Compatible (Test phases and checkpoints present)

  Follow-up TODOs: None
-->

# Desafio Prompt Engineer Constitution

## Core Principles

### I. Code Quality

All Python code MUST adhere to these non-negotiable standards:

- Code MUST be compatible with Python 3.9+
- All scripts MUST use proper error handling with descriptive error messages
- Environment variables MUST be loaded from `.env` files using python-dotenv
- YAML files MUST be validated before processing
- All functions MUST have clear, single responsibilities
- No hardcoded credentials or API keys in source code
- Imports MUST follow the pattern: standard library → third-party → local modules

**Rationale**: LangChain/LangSmith integration requires reliable, maintainable code that properly handles API interactions and prompt management.

### II. Testing Standards

Testing is mandatory and MUST follow these requirements:

- All tests MUST use pytest framework
- Minimum 6 test cases required for prompt validation:
  - `test_prompt_has_system_prompt`: Verify system prompt exists and is non-empty
  - `test_prompt_has_role_definition`: Verify persona definition is present
  - `test_prompt_mentions_format`: Verify Markdown/User Story format requirement
  - `test_prompt_has_few_shot_examples`: Verify few-shot examples are included
  - `test_prompt_no_todos`: Verify no `[TODO]` placeholders remain
  - `test_minimum_techniques`: Verify at least 2 prompt engineering techniques in metadata
- Tests MUST be runnable via `pytest tests/test_prompts.py`
- Test failures MUST provide actionable feedback

**Rationale**: Prompt quality is validated through automated tests before evaluation, ensuring consistent quality gates.

### III. User Experience Consistency

All prompts and outputs MUST maintain consistent user experience:

- Prompts MUST include clear role definition (persona)
- Prompts MUST use System vs User prompt separation appropriately
- Output format MUST be specified (Markdown, User Story format)
- Edge cases MUST be explicitly handled in prompt instructions
- Few-shot examples MUST demonstrate expected input/output patterns
- All prompts MUST be stored in YAML format in `prompts/` directory

**Rationale**: Consistent prompt structure ensures predictable LLM behavior and reproducible evaluation results.

### IV. Performance Requirements

All evaluation metrics MUST meet minimum thresholds:

- Tone Score MUST be >= 0.9
- Acceptance Criteria Score MUST be >= 0.9
- User Story Format Score MUST be >= 0.9
- Completeness Score MUST be >= 0.9
- Average of all 4 metrics MUST be >= 0.9
- ALL metrics MUST pass individually (not just average)

Iteration expectations:
- 3-5 iterations are typical to achieve all thresholds
- Each iteration MUST: analyze low metrics → modify prompt → push → evaluate
- Datasets MUST NOT be modified to achieve scores

**Rationale**: The challenge requires demonstrable prompt engineering skill measured through objective, automated evaluation.

## Evaluation Standards

### Metrics Definition

| Metric | Evaluates | Pass Threshold |
|--------|-----------|----------------|
| Tone Score | Language appropriateness and professionalism | >= 0.9 |
| Acceptance Criteria Score | Quality of acceptance criteria in User Story | >= 0.9 |
| User Story Format Score | Adherence to User Story standard format | >= 0.9 |
| Completeness Score | Coverage of all bug aspects in transformation | >= 0.9 |

### Prompt Engineering Techniques

At least 2 of the following MUST be applied and documented:

- Few-shot Learning: Provide 2-3 clear input/output examples
- Chain of Thought (CoT): "Think step by step" instructions
- Tree of Thought: Multiple reasoning paths
- Skeleton of Thought: Structured response steps
- ReAct: Reasoning + Action pattern
- Role Prompting: Detailed persona and context

## Development Workflow

### Execution Order

1. `python src/pull_prompts.py` - Pull initial prompts from LangSmith
2. Edit `prompts/bug_to_user_story_v2.yml` - Apply prompt engineering techniques
3. `python src/push_prompts.py` - Push optimized prompts to LangSmith
4. `python src/evaluate.py` - Run evaluation
5. `pytest tests/test_prompts.py` - Validate prompt structure
6. Iterate until all metrics >= 0.9

### File Structure Compliance

```
prompts/
├── bug_to_user_story_v1.yml    # Original prompt (read-only after pull)
└── bug_to_user_story_v2.yml    # Optimized prompt (your work)

src/
├── pull_prompts.py             # Pull from LangSmith Hub
├── push_prompts.py             # Push to your LangSmith namespace
├── evaluate.py                 # Run evaluation against metrics
├── metrics.py                  # Metric implementations (do not modify)
├── dataset.py                  # Bug examples (do not modify)
└── utils.py                    # Helper functions

tests/
└── test_prompts.py             # Prompt validation tests
```

## Governance

- This Constitution supersedes ad-hoc practices for this project
- Amendments require documentation of rationale and impact
- All code changes MUST maintain compliance with principles
- PRs/commits MUST verify: tests pass, metrics meet thresholds, no secrets exposed
- Use CLAUDE.md for runtime development guidance

**Version**: 1.0.0 | **Ratified**: 2026-01-20 | **Last Amended**: 2026-01-20
