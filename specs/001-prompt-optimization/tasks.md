# Tasks: LangSmith Prompt Optimization Challenge

**Input**: Design documents from `/specs/001-prompt-optimization/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests ARE required for this feature (FR-012: 6 pytest validation tests mandatory)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/`, `prompts/` at repository root
- All Python files MUST include docstrings (FR-013: teacher audit requirement)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create directory structure: `src/`, `tests/`, `prompts/` per plan.md
- [x] T002 Create requirements.txt with dependencies: langchain, langsmith, langchain-openai, langchain-google-genai, python-dotenv, pyyaml, pytest
- [x] T003 Create .env.example template with placeholder credentials in project root
- [x] T004 [P] Create src/utils.py with helper functions (load_env, load_yaml, save_yaml) including docstrings

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create src/dataset.py with 15 bug examples (5 simple, 7 medium, 3 complex) including docstrings
- [x] T006 Create src/metrics.py with 4 metric implementations (Tone, Acceptance Criteria, User Story Format, Completeness) including docstrings

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Pull Initial Prompts (Priority: P1) 🎯 MVP

**Goal**: Download initial low-quality prompt from LangSmith Hub to local YAML file

**Independent Test**: Run `python src/pull_prompts.py` and verify `prompts/bug_to_user_story_v1.yml` exists with valid YAML

### Implementation for User Story 1

- [x] T007 [US1] Create src/pull_prompts.py with main() function including docstrings
- [x] T008 [US1] Implement load_credentials() function in src/pull_prompts.py to load .env using python-dotenv
- [x] T009 [US1] Implement pull_prompt() function in src/pull_prompts.py using langchain.hub.pull()
- [x] T010 [US1] Implement save_prompt_to_yaml() function in src/pull_prompts.py to save to prompts/bug_to_user_story_v1.yml
- [x] T011 [US1] Add error handling for authentication, network, and file write failures in src/pull_prompts.py
- [x] T012 [US1] Add CLI output messages per contracts/cli-interface.md in src/pull_prompts.py

**Checkpoint**: User Story 1 complete - can pull prompts from LangSmith Hub

---

## Phase 4: User Story 2 - Optimize Prompt with Engineering Techniques (Priority: P2)

**Goal**: Create optimized prompt with role definition, few-shot examples, and at least 2 techniques

**Independent Test**: Validate prompts/bug_to_user_story_v2.yml contains required elements (role, examples, techniques in metadata)

### Implementation for User Story 2

- [x] T013 [US2] Create prompts/bug_to_user_story_v2.yml with YAML structure per data-model.md schema
- [x] T014 [US2] Add metadata section with name, description, techniques list (>= 2), and tags
- [x] T015 [US2] Add system_prompt with Role Prompting technique: "You are an experienced Product Manager..."
- [x] T016 [US2] Add Chain of Thought instructions to system_prompt: numbered steps for analysis
- [x] T017 [US2] Add user_prompt_template with {bug_report} variable in prompts/bug_to_user_story_v2.yml
- [x] T018 [US2] Add examples section with 2-3 few-shot examples (simple, medium, complex bugs)
- [x] T019 [US2] Add edge case handling instructions in system_prompt (empty input, malformed data)
- [x] T020 [US2] Verify no [TODO] markers remain in prompts/bug_to_user_story_v2.yml

**Checkpoint**: User Story 2 complete - optimized prompt created with techniques applied

---

## Phase 5: User Story 3 - Push Optimized Prompts to LangSmith (Priority: P3)

**Goal**: Upload optimized prompt to LangSmith Hub with metadata and public visibility

**Independent Test**: Run `python src/push_prompts.py` and verify prompt appears in LangSmith dashboard

### Implementation for User Story 3

- [x] T021 [US3] Create src/push_prompts.py with main() function including docstrings
- [x] T022 [US3] Implement load_prompt_from_yaml() function in src/push_prompts.py to read prompts/bug_to_user_story_v2.yml
- [x] T023 [US3] Implement validate_prompt_structure() function in src/push_prompts.py per data-model.md schema
- [x] T024 [US3] Implement push_prompt() function in src/push_prompts.py using langchain.hub.push() with metadata
- [x] T025 [US3] Add new_repo_is_public=True parameter in push_prompt() for public visibility
- [x] T026 [US3] Add error handling for file not found, validation, authentication failures in src/push_prompts.py
- [x] T027 [US3] Add CLI output messages per contracts/cli-interface.md in src/push_prompts.py

**Checkpoint**: User Story 3 complete - can push prompts to LangSmith Hub

---

## Phase 6: User Story 4 - Evaluate Prompt Quality (Priority: P4)

**Goal**: Run automated evaluation against 4 metrics and display pass/fail status

**Independent Test**: Run `python src/evaluate.py` and receive scores for all 4 metrics

### Implementation for User Story 4

- [x] T028 [US4] Create src/evaluate.py with main() function including docstrings
- [x] T029 [US4] Implement get_llm_provider() function in src/evaluate.py to detect OpenAI or Gemini from .env
- [x] T030 [US4] Implement create_prompt_chain() function in src/evaluate.py using LangChain prompt template
- [x] T031 [US4] Implement run_evaluation() function in src/evaluate.py using langsmith.evaluation.evaluate
- [x] T032 [US4] Implement calculate_scores() function in src/evaluate.py to aggregate 4 metric results
- [x] T033 [US4] Implement display_results() function in src/evaluate.py with APPROVED/FAILED status
- [x] T034 [US4] Add error handling for missing provider, API failures in src/evaluate.py
- [x] T035 [US4] Add CLI output messages per contracts/cli-interface.md in src/evaluate.py

**Checkpoint**: User Story 4 complete - can evaluate prompts and see metric scores

---

## Phase 7: User Story 5 - Validate Prompt Structure with Tests (Priority: P5)

**Goal**: Implement 6 pytest tests to validate prompt structure before evaluation

**Independent Test**: Run `pytest tests/test_prompts.py` and all 6 tests pass

### Implementation for User Story 5

- [x] T036 [US5] Create tests/test_prompts.py with module docstring and imports
- [x] T037 [US5] Implement test_prompt_has_system_prompt() in tests/test_prompts.py to verify system_prompt exists and is non-empty
- [x] T038 [US5] Implement test_prompt_has_role_definition() in tests/test_prompts.py to verify "You are" or "Você é" pattern
- [x] T039 [US5] Implement test_prompt_mentions_format() in tests/test_prompts.py to verify "User Story" or "Markdown" mention
- [x] T040 [US5] Implement test_prompt_has_few_shot_examples() in tests/test_prompts.py to verify examples list has >= 1 item
- [x] T041 [US5] Implement test_prompt_no_todos() in tests/test_prompts.py to verify no "[TODO]" markers
- [x] T042 [US5] Implement test_minimum_techniques() in tests/test_prompts.py to verify metadata.techniques has >= 2 items
- [x] T043 [US5] Add clear assertion messages with hints for each test failure

**Checkpoint**: User Story 5 complete - can validate prompt structure before evaluation

---

## Phase 8: User Story 6 - Iterate Until All Metrics Pass (Priority: P6)

**Goal**: Support iterative workflow to achieve >= 0.9 on all 4 metrics

**Independent Test**: Run push-evaluate cycle multiple times, tracking metric improvements

### Implementation for User Story 6

- [x] T044 [US6] Enhance display_results() in src/evaluate.py to show which metrics need improvement
- [x] T045 [US6] Add improvement delta calculation in src/evaluate.py (e.g., "needs +0.12")
- [x] T046 [US6] Create iteration checklist in quickstart.md: analyze → modify → push → evaluate
- [x] T047 [US6] Document iteration tips based on metric feedback in quickstart.md

**Checkpoint**: User Story 6 complete - clear guidance for iterative improvement

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and final validation

- [x] T048 [P] Update README.md with "Técnicas Aplicadas (Fase 2)" section
- [x] T049 [P] Update README.md with "Resultados Finais" section with comparison table
- [x] T050 [P] Update README.md with "Como Executar" section with all commands
- [x] T051 Verify all Python files have module-level and function-level docstrings (FR-013)
- [ ] T052 Run full workflow validation per quickstart.md
- [ ] T053 Verify all 6 pytest tests pass
- [ ] T054 Run final evaluation and verify all metrics >= 0.9

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1 (Pull) → US2 (Optimize) → US3 (Push) → US4 (Evaluate) → US5 (Test) → US6 (Iterate)
  - Sequential order required: each story builds on previous
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies
- **User Story 2 (P2)**: Depends on US1 (needs pulled prompt to analyze)
- **User Story 3 (P3)**: Depends on US2 (needs optimized prompt to push)
- **User Story 4 (P4)**: Depends on US3 (needs pushed prompt to evaluate)
- **User Story 5 (P5)**: Depends on US2 (needs optimized prompt to test)
- **User Story 6 (P6)**: Depends on US3, US4 (needs push and evaluate working)

### Within Each User Story

- Core functions before error handling
- Error handling before CLI output
- All code must include docstrings

### Parallel Opportunities

- T004 can run in parallel with T001-T003
- T048, T049, T050 can run in parallel
- T037-T042 test implementations can run in parallel

---

## Parallel Example: User Story 5 Tests

```bash
# Launch all test implementations together:
Task: "Implement test_prompt_has_system_prompt() in tests/test_prompts.py"
Task: "Implement test_prompt_has_role_definition() in tests/test_prompts.py"
Task: "Implement test_prompt_mentions_format() in tests/test_prompts.py"
Task: "Implement test_prompt_has_few_shot_examples() in tests/test_prompts.py"
Task: "Implement test_prompt_no_todos() in tests/test_prompts.py"
Task: "Implement test_minimum_techniques() in tests/test_prompts.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (dataset.py, metrics.py)
3. Complete Phase 3: User Story 1 (pull_prompts.py)
4. **STOP and VALIDATE**: Run `python src/pull_prompts.py` and verify output

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 (Pull) → Can download prompts from Hub
3. US2 (Optimize) → Optimized prompt created
4. US3 (Push) → Can upload prompts to Hub
5. US4 (Evaluate) → Can measure prompt quality
6. US5 (Test) → Can validate prompt structure
7. US6 (Iterate) → Can achieve >= 0.9 on all metrics

### Sequential Flow Required

Unlike typical projects, this feature requires **sequential execution** of user stories because each story builds on the previous:

```
Pull (US1) → Optimize (US2) → Push (US3) → Evaluate (US4)
                    ↓
               Test (US5)
                    ↓
              Iterate (US6)
```

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- All Python code MUST have docstrings (FR-013: teacher audit)
- 6 pytest tests are MANDATORY (FR-012)
- Target: All 4 metrics >= 0.9 (typically 3-5 iterations)
- Commit after each task or logical group
