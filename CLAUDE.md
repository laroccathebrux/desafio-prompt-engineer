# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LangChain/LangSmith prompt engineering challenge. The goal is to pull low-quality prompts from LangSmith Prompt Hub, optimize them using advanced prompt engineering techniques, push the optimized versions back, and achieve >= 0.9 scores on all evaluation metrics.

## Commands

### Setup
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Execution Flow
```bash
# 1. Pull initial prompts from LangSmith
python src/pull_prompts.py

# 2. Push optimized prompts to LangSmith
python src/push_prompts.py

# 3. Run evaluation
python src/evaluate.py
```

### Iteration Workflow (3-5 iterations expected)
```bash
# 1. Edit the prompt
# Edit prompts/bug_to_user_story_v2.yml

# 2. Commit changes (IMPORTANT: always commit before evaluating)
git add prompts/ && git commit -m "Iteração N: melhorias no prompt"

# 3. Push to LangSmith
python src/push_prompts.py

# 4. Run evaluation (results are saved automatically)
python src/evaluate.py

# 5. Repeat until ALL metrics >= 0.9
```

### Testing
```bash
pytest tests/test_prompts.py
```

## Architecture

### Key Files
- `src/pull_prompts.py` - Downloads prompts from LangSmith Hub (leonanluppi/bug_to_user_story_v1)
- `src/push_prompts.py` - Uploads optimized prompts to LangSmith with metadata
- `src/evaluate.py` - Runs automated evaluation against metrics
- `src/metrics.py` - Contains 4 custom metrics (Tone, Acceptance Criteria, User Story Format, Completeness)
- `src/dataset.py` - Contains 15 bug examples (5 simple, 7 medium, 3 complex)
- `src/utils.py` - Helper functions

### Prompts Directory
- `prompts/bug_to_user_story_v1.yml` - Original low-quality prompt (from pull)
- `prompts/bug_to_user_story_v2.yml` - Optimized prompt (your work)

### Evaluations Directory
- `evaluations/history.json` - Automatically saved evaluation history (tracks all iterations with scores and comparisons)

## Evaluation Criteria

All 4 metrics must be >= 0.9:
- Tone Score
- Acceptance Criteria Score
- User Story Format Score
- Completeness Score

## Required Prompt Engineering Techniques

Apply at least 2 of:
- Few-shot Learning
- Chain of Thought (CoT)
- Tree of Thought
- Skeleton of Thought
- ReAct
- Role Prompting

## Providers

- **OpenAI**: gpt-4o-mini (responses), gpt-4o (evaluation)
- **Gemini**: gemini-2.5-flash (both) - Free tier: 15 req/min, 1500 req/day

## Environment Variables

Required in `.env`:
- `LANGCHAIN_API_KEY` - LangSmith API key
- `LANGCHAIN_TRACING_V2=true`
- `OPENAI_API_KEY` or `GOOGLE_API_KEY`

## Active Technologies
- Python 3.9+ + LangChain, LangSmith, langchain-openai, langchain-google-genai, python-dotenv, PyYAML (001-prompt-optimization)
- Local YAML files in `prompts/` directory (001-prompt-optimization)

## Recent Changes
- 001-prompt-optimization: Added Python 3.9+ + LangChain, LangSmith, langchain-openai, langchain-google-genai, python-dotenv, PyYAML
