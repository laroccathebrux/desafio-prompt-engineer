# Data Model: LangSmith Prompt Optimization Challenge

**Feature**: 001-prompt-optimization
**Date**: 2026-01-20

## Overview

This feature uses file-based data storage (YAML) and relies on LangSmith for cloud-based prompt management. No database is required.

## Entity Definitions

### 1. Prompt

A structured instruction set for LLM bug-to-user-story transformation.

**Storage**: `prompts/*.yml` (local) + LangSmith Prompt Hub (cloud)

**Schema**:
```yaml
metadata:
  name: string              # Required: Unique identifier (e.g., "bug_to_user_story_v2")
  description: string       # Required: Purpose description
  techniques: list[string]  # Required: At least 2 techniques
  tags: list[string]        # Optional: Searchable tags

system_prompt: string       # Required: Non-empty system message with role definition

user_prompt_template: string  # Required: User message template with {bug_report} variable

examples: list[Example]     # Required: At least 1 few-shot example
```

**Validation Rules**:
- `metadata.name` must be non-empty
- `metadata.techniques` must have length >= 2
- `system_prompt` must be non-empty and contain role definition pattern
- `system_prompt` must mention output format (Markdown, User Story)
- `examples` must have at least 1 item
- No `[TODO]` markers allowed in any string field

### 2. Example (Few-shot)

A single input/output pair demonstrating expected transformation.

**Schema**:
```yaml
input: string   # Required: Sample bug report
output: string  # Required: Expected User Story output
```

**Validation Rules**:
- Both `input` and `output` must be non-empty
- `output` should follow User Story format

### 3. Bug Report (Input)

Input data representing a software defect.

**Storage**: `src/dataset.py` (provided, read-only)

**Schema** (from dataset):
```python
{
    "id": string,           # Unique bug identifier
    "title": string,        # Bug title
    "description": string,  # Detailed description
    "severity": string,     # "Low" | "Medium" | "High" | "Critical"
    "category": string,     # "simple" | "medium" | "complex"
    "steps_to_reproduce": list[string],  # Optional
    "expected_behavior": string,         # Optional
    "actual_behavior": string            # Optional
}
```

**Dataset Distribution**:
- 5 simple bugs
- 7 medium bugs
- 3 complex bugs

### 4. User Story (Output)

Transformed output following standard User Story format.

**Schema** (expected in prompt output):
```markdown
## User Story: [Title]

**As a** [user type]
**I want** [goal/action]
**So that** [benefit/reason]

### Acceptance Criteria
- Given [initial state]
- When [action]
- Then [expected outcome]

**Priority**: [High/Medium/Low]
**Technical Notes**: [Optional implementation hints]
```

### 5. Evaluation Result

Metric scores from LangSmith evaluation.

**Schema** (from evaluate.py output):
```python
{
    "prompt_name": string,
    "metrics": {
        "tone_score": float,              # 0.0 - 1.0
        "acceptance_criteria_score": float,
        "user_story_format_score": float,
        "completeness_score": float
    },
    "average": float,
    "status": "APPROVED" | "FAILED",
    "timestamp": datetime
}
```

**Validation Rules**:
- All metrics must be >= 0.9 for APPROVED status
- Average must also be >= 0.9

### 6. Environment Configuration

Credentials and settings loaded from `.env`.

**Schema**:
```env
# LangSmith (Required)
LANGCHAIN_API_KEY=lsv2_...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=desafio-prompt-engineer

# LLM Provider (Choose one)
OPENAI_API_KEY=sk-...
# OR
GOOGLE_API_KEY=AI...
```

## Entity Relationships

```
┌─────────────────┐
│  Environment    │
│  (.env file)    │
└────────┬────────┘
         │ loads
         ▼
┌─────────────────┐        ┌─────────────────┐
│  pull_prompts   │───────▶│    Prompt       │
│    (script)     │ saves  │  (YAML file)    │
└─────────────────┘        └────────┬────────┘
                                    │ contains
                                    ▼
                           ┌─────────────────┐
                           │    Examples     │
                           │  (Few-shot)     │
                           └─────────────────┘

┌─────────────────┐        ┌─────────────────┐
│   Bug Report    │───────▶│   User Story    │
│   (dataset)     │  LLM   │   (output)      │
└─────────────────┘        └─────────────────┘
         │                          │
         │                          │
         ▼                          ▼
┌─────────────────────────────────────────────┐
│              Evaluation                      │
│  (metrics.py + evaluate.py)                 │
└─────────────────────────────────────────────┘
                    │
                    ▼
         ┌─────────────────┐
         │ Evaluation      │
         │ Result          │
         └─────────────────┘
```

## File Locations

| Entity | Location | Read/Write |
|--------|----------|------------|
| Prompt (v1) | `prompts/bug_to_user_story_v1.yml` | Read-only (after pull) |
| Prompt (v2) | `prompts/bug_to_user_story_v2.yml` | Read/Write |
| Bug Reports | `src/dataset.py` | Read-only |
| Metrics | `src/metrics.py` | Read-only |
| Configuration | `.env` | Read-only |
| Test Results | Console output + LangSmith dashboard | Write |

## State Transitions

### Prompt Lifecycle

```
┌──────────┐    pull    ┌──────────┐   optimize   ┌──────────┐
│  Remote  │──────────▶│  Local   │─────────────▶│ Optimized│
│  (Hub)   │           │  (v1)    │              │  (v2)    │
└──────────┘           └──────────┘              └────┬─────┘
                                                      │
                                                      │ push
                                                      ▼
┌──────────┐  evaluate  ┌──────────┐              ┌──────────┐
│ Approved │◀──────────│Evaluating│◀─────────────│  Remote  │
│  >=0.9   │           │          │              │  (Hub)   │
└──────────┘           └────┬─────┘              └──────────┘
                            │
                            │ if < 0.9
                            ▼
                       ┌──────────┐
                       │  Iterate │───────┐
                       │          │       │ modify
                       └──────────┘       │
                            ▲             │
                            └─────────────┘
```

### Evaluation Workflow

1. Load optimized prompt from YAML
2. Create LangChain prompt template
3. For each bug in dataset:
   - Generate User Story via LLM
   - Score with 4 metrics
4. Calculate average
5. Return APPROVED/FAILED status
