# Quickstart Guide: LangSmith Prompt Optimization Challenge

**Feature**: 001-prompt-optimization
**Date**: 2026-01-20

## Prerequisites

1. **Python Environment**: Conda environment `desafio_02` active
2. **API Keys** (at least one):
   - LangSmith API key (required)
   - OpenAI API key OR Google Gemini API key

## Setup

### 1. Configure Environment Variables

Create a `.env` file in the project root:

```env
# LangSmith (Required)
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=desafio-prompt-engineer

# Choose ONE LLM Provider:

# Option A: OpenAI (Paid, ~$1-5)
OPENAI_API_KEY=your_openai_api_key

# Option B: Gemini (Free, rate limited)
GOOGLE_API_KEY=your_google_api_key
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Workflow

### Step 1: Pull Initial Prompt

Download the low-quality prompt from LangSmith Hub:

```bash
python src/pull_prompts.py
```

**Expected output**:
```
Pulling prompt from LangSmith Hub...
Prompt: leonanluppi/bug_to_user_story_v1
Saved to: prompts/bug_to_user_story_v1.yml
Pull completed successfully!
```

**Verify**: Check that `prompts/bug_to_user_story_v1.yml` exists.

### Step 2: Create Optimized Prompt

Create `prompts/bug_to_user_story_v2.yml` with your optimized prompt.

**Required structure**:
```yaml
metadata:
  name: bug_to_user_story_v2
  description: Optimized prompt for converting bug reports to User Stories
  techniques:
    - role_prompting
    - few_shot_learning
    # Add at least 2 techniques total
  tags:
    - prompt-engineering
    - user-story

system_prompt: |
  You are an experienced Product Manager with expertise in Agile methodologies.
  Your task is to transform bug reports into well-structured User Stories.

  Follow these steps:
  1. Analyze the bug report carefully
  2. Identify the affected user type
  3. Extract the desired behavior (what should work)
  4. Write clear acceptance criteria

  Output format: Markdown User Story with acceptance criteria.

user_prompt_template: |
  Bug Report:
  {bug_report}

  Transform this into a User Story.

examples:
  - input: |
      Title: Login button broken
      Description: Cannot click login on mobile
      Severity: High
    output: |
      ## User Story: Fix Mobile Login Button

      **As a** mobile user
      **I want** to successfully click the login button
      **So that** I can access my account

      ### Acceptance Criteria
      - Given I am on the login page on mobile
      - When I tap the login button
      - Then I should be logged in

      **Priority**: High
```

### Step 3: Validate Prompt Structure

Run tests to ensure your prompt meets all requirements:

```bash
pytest tests/test_prompts.py
```

**Expected output** (all pass):
```
======================== 6 passed ========================
```

**If tests fail**: Fix the issues indicated in the error messages.

### Step 4: Push to LangSmith

Upload your optimized prompt:

```bash
python src/push_prompts.py
```

**Expected output**:
```
Reading optimized prompt from prompts/bug_to_user_story_v2.yml...
Pushing to LangSmith Hub...
Prompt published: {your_username}/bug_to_user_story_v2
Push completed successfully!
```

### Step 5: Evaluate

Run the evaluation to check your scores:

```bash
python src/evaluate.py
```

**Target output** (APPROVED):
```
================================
Prompt: {your_username}/bug_to_user_story_v2
- Tone Score: >= 0.9
- Acceptance Criteria Score: >= 0.9
- User Story Format Score: >= 0.9
- Completeness Score: >= 0.9
================================
Status: APROVADO ✓
```

### Step 6: Iterate (if needed)

If evaluation shows FAILED:

1. **Analyze**: Identify which metrics are below 0.9
2. **Modify**: Edit `prompts/bug_to_user_story_v2.yml`
3. **Validate**: `pytest tests/test_prompts.py`
4. **Push**: `python src/push_prompts.py`
5. **Evaluate**: `python src/evaluate.py`
6. **Repeat**: Until all metrics >= 0.9

**Typical iterations**: 3-5

## Iteration Checklist

Use this checklist for each iteration cycle:

```
□ Analyze evaluation output - which metrics need improvement?
□ Review the improvement delta (e.g., "precisa +0.12")
□ Modify prompts/bug_to_user_story_v2.yml based on tips below
□ Run pytest tests/test_prompts.py - ensure all tests pass
□ Run python src/push_prompts.py - push updated prompt
□ Run python src/evaluate.py - check new scores
□ Document changes made for this iteration
```

## Iteration Tips by Metric

### Low Tone Score (< 0.9)

**Symptoms**: Casual language, poor structure, negative framing

**Fixes**:
- Remove casual words (stuff, thing, kinda, gonna)
- Ensure proper sentence capitalization
- Add markdown headers and bold formatting
- Frame solutions positively ("I want to be able to...")
- Keep response between 50-500 words

### Low Acceptance Criteria Score (< 0.9)

**Symptoms**: Missing Given/When/Then, vague conditions

**Fixes**:
- Add explicit "Acceptance Criteria" section header
- Use Given/When/Then format for each scenario
- Include at least 2-3 criteria bullets
- Use testable verbs: "should display", "must return", "receives"
- Add expected outcomes explicitly

### Low User Story Format Score (< 0.9)

**Symptoms**: Missing As a/I want/So that structure

**Fixes**:
- Include clear "As a [user type]" statement
- Add "I want [goal/action]" clause
- Add "So that [benefit]" clause
- Start with a clear title using markdown header
- Use proper markdown structure throughout

### Low Completeness Score (< 0.9)

**Symptoms**: Too short, missing context, no priority

**Fixes**:
- Ensure response is at least 75+ words
- Add Priority section (High/Medium/Low)
- Include Technical Notes section when relevant
- Use at least 2 markdown headers (##, ###)
- Mention user impact and benefit explicitly

## Quick Commands Reference

| Action | Command |
|--------|---------|
| Pull initial prompt | `python src/pull_prompts.py` |
| Validate structure | `pytest tests/test_prompts.py` |
| Push optimized prompt | `python src/push_prompts.py` |
| Evaluate prompt | `python src/evaluate.py` |

## Troubleshooting

### "Authentication failed"
- Check `LANGCHAIN_API_KEY` in `.env`
- Ensure no extra spaces or quotes around the key

### "No LLM provider configured"
- Add either `OPENAI_API_KEY` or `GOOGLE_API_KEY` to `.env`

### "Rate limit exceeded" (Gemini)
- Wait 1 minute between evaluation runs
- Or switch to OpenAI for faster iteration

### Tests fail with "role definition missing"
- Add "You are [role]" to your system_prompt

### Tests fail with "techniques count"
- Add at least 2 techniques to metadata.techniques list

## Success Criteria Checklist

Before submitting, verify:

- [ ] All 4 metrics >= 0.9
- [ ] All 6 tests pass
- [ ] Prompt is public on LangSmith Hub
- [ ] README.md updated with techniques applied
- [ ] README.md has results comparison table
- [ ] All code has docstrings (teacher audit)
