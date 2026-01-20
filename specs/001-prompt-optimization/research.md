# Research: LangSmith Prompt Optimization Challenge

**Feature**: 001-prompt-optimization
**Date**: 2026-01-20
**Status**: Complete

## Research Areas

### 1. LangChain Hub API for Prompt Management

**Decision**: Use `langchain.hub` module for pull/push operations

**Rationale**:
- Official LangChain interface for LangSmith Prompt Hub
- Simplified authentication via environment variables
- Built-in version management and metadata support

**Alternatives Considered**:
- Direct LangSmith REST API: More complex, requires manual HTTP handling
- Custom YAML file management: Wouldn't integrate with LangSmith Hub

**Implementation Pattern**:
```python
from langchain import hub

# Pull prompt
prompt = hub.pull("leonanluppi/bug_to_user_story_v1")

# Push prompt (requires authentication)
hub.push("username/bug_to_user_story_v2", prompt, new_repo_is_public=True)
```

### 2. LangSmith Evaluation Framework

**Decision**: Use `langsmith.evaluation.evaluate` for metric assessment

**Rationale**:
- Native integration with LangSmith tracing
- Supports custom evaluators (metrics.py)
- Provides detailed scoring and feedback

**Alternatives Considered**:
- Manual evaluation: Not scalable, subjective
- Third-party evaluation tools: Lack LangSmith integration

**Key Components**:
- Dataset: 15 bug examples (provided in dataset.py)
- Evaluators: 4 metrics (Tone, Acceptance Criteria, User Story Format, Completeness)
- Target function: Prompt + LLM chain

### 3. LLM Provider Selection

**Decision**: Support both OpenAI and Gemini providers

**Rationale**:
- OpenAI: Better quality but costs $1-5
- Gemini: Free tier available (15 req/min, 1500 req/day)
- User choice based on budget and rate limits

**Implementation**:
```python
# OpenAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")  # responses
evaluator_llm = ChatOpenAI(model="gpt-4o")  # evaluation

# Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
```

### 4. Prompt Engineering Techniques for Bug-to-User-Story Transformation

**Decision**: Apply Role Prompting + Few-shot Learning + Chain of Thought

**Rationale**:
- **Role Prompting**: Establishes Product Manager persona for consistent business language
- **Few-shot Learning**: Provides concrete examples of expected transformation quality
- **Chain of Thought**: Guides systematic analysis of bug reports

**Research Findings**:

| Technique | Impact on Metric | Recommended For |
|-----------|------------------|-----------------|
| Role Prompting | Tone Score, Format | All prompts |
| Few-shot Learning | All metrics | High-impact |
| Chain of Thought | Completeness, Acceptance Criteria | Complex bugs |
| Skeleton of Thought | Format Score | Structured output |

**Best Practices**:
1. Start with Role Prompting to set context
2. Add 2-3 few-shot examples covering simple, medium, complex bugs
3. Include explicit Chain of Thought steps for analysis
4. Specify exact output format with Markdown

### 5. YAML Prompt Structure

**Decision**: Use structured YAML with metadata, system_prompt, user_prompt_template, examples

**Rationale**:
- Metadata enables test validation (techniques list)
- Separation of system/user prompts follows LLM best practices
- Examples section supports few-shot learning

**Schema**:
```yaml
metadata:
  name: string          # Prompt identifier
  description: string   # Purpose description
  techniques: list      # Applied techniques (for test_minimum_techniques)
  tags: list           # Searchable tags

system_prompt: string   # System message with role definition

user_prompt_template: string  # User message with {variables}

examples:              # Few-shot examples
  - input: string
    output: string
```

### 6. pytest Validation Tests

**Decision**: Implement 6 specific tests as required by spec

**Rationale**:
- Automated quality gate before evaluation
- Ensures prompt structure meets requirements
- Catches common issues (missing persona, no examples, leftover TODOs)

**Test Implementation Strategy**:

| Test | What It Validates | How |
|------|-------------------|-----|
| `test_prompt_has_system_prompt` | System prompt exists | Check YAML key, non-empty |
| `test_prompt_has_role_definition` | Persona defined | Search for "You are" pattern |
| `test_prompt_mentions_format` | Output format specified | Search for "User Story", "Markdown" |
| `test_prompt_has_few_shot_examples` | Examples present | Check examples list length >= 1 |
| `test_prompt_no_todos` | No incomplete work | Search for "[TODO]" pattern |
| `test_minimum_techniques` | 2+ techniques | Check metadata.techniques length |

### 7. Error Handling Best Practices

**Decision**: Implement comprehensive error handling with clear messages

**Rationale**:
- API calls can fail (network, auth, rate limits)
- Clear messages help debugging
- Constitution requires descriptive error messages

**Error Categories**:
1. **Authentication**: Missing/invalid API keys
2. **Network**: LangSmith API unreachable
3. **Rate Limits**: Gemini 15 req/min exceeded
4. **Validation**: Invalid YAML structure
5. **Evaluation**: Metric calculation failures

## Dependencies Resolved

| Package | Version | Purpose |
|---------|---------|---------|
| langchain | latest | Hub operations, prompt templates |
| langsmith | latest | Evaluation, tracing, client |
| langchain-openai | latest | OpenAI LLM integration |
| langchain-google-genai | latest | Gemini LLM integration |
| python-dotenv | latest | Environment variable loading |
| pyyaml | latest | YAML parsing and validation |
| pytest | latest | Test framework |

## Open Questions Resolved

1. **Q**: Which prompt engineering techniques to prioritize?
   **A**: Role Prompting + Few-shot Learning (mandatory) + Chain of Thought (recommended)

2. **Q**: How to handle Gemini rate limits?
   **A**: Implement retry logic with exponential backoff; consider OpenAI for faster iteration

3. **Q**: What YAML structure supports both prompts and tests?
   **A**: Metadata section with techniques list enables test_minimum_techniques validation

4. **Q**: How to ensure docstrings for teacher audit?
   **A**: Document module-level, function-level docstrings with Args, Returns, Example sections

## Next Steps

1. Create data-model.md with entity definitions
2. Create contracts/ with CLI interface specifications
3. Create quickstart.md with execution guide
4. Proceed to /speckit.tasks for task generation
