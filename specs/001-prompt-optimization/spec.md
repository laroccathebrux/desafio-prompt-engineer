# Feature Specification: LangSmith Prompt Optimization Challenge

**Feature Branch**: `001-prompt-optimization`
**Created**: 2026-01-20
**Status**: Draft
**Input**: User description: "Build a system to pull, optimize, and evaluate prompts from LangSmith Prompt Hub, achieving >= 0.9 scores on all evaluation metrics"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Pull Initial Prompts (Priority: P1)

As a prompt engineer, I need to download the initial low-quality prompt from LangSmith Prompt Hub so I can analyze it and understand what needs improvement.

**Why this priority**: This is the foundation - without pulling the original prompt, no optimization work can begin. It establishes the baseline for comparison.

**Independent Test**: Can be fully tested by running the pull script and verifying the prompt file exists locally with valid YAML content.

**Acceptance Scenarios**:

1. **Given** valid LangSmith credentials in .env file, **When** I run the pull script, **Then** the prompt `leonanluppi/bug_to_user_story_v1` is downloaded and saved to `prompts/bug_to_user_story_v1.yml`
2. **Given** the pull script has executed successfully, **When** I open the saved file, **Then** I see valid YAML content with prompt instructions
3. **Given** invalid or missing credentials, **When** I run the pull script, **Then** I receive a clear error message indicating the authentication problem

---

### User Story 2 - Optimize Prompt with Engineering Techniques (Priority: P2)

As a prompt engineer, I need to refactor the initial prompt using advanced prompt engineering techniques to improve its quality and achieve better evaluation scores.

**Why this priority**: This is the core deliverable - the optimized prompt demonstrates mastery of prompt engineering techniques and directly impacts evaluation scores.

**Independent Test**: Can be tested by validating the optimized prompt contains required elements (role definition, few-shot examples, clear instructions) and passes structural validation tests.

**Acceptance Scenarios**:

1. **Given** the original prompt has been pulled, **When** I create the optimized version, **Then** it includes a clear role/persona definition (e.g., "You are a Product Manager")
2. **Given** I am optimizing the prompt, **When** I apply techniques, **Then** at least 2 prompt engineering techniques are applied and documented in YAML metadata
3. **Given** the optimized prompt is created, **When** it is validated, **Then** it contains few-shot examples demonstrating expected input/output
4. **Given** the optimized prompt is created, **When** it is validated, **Then** it specifies the required output format (User Story with Markdown)
5. **Given** the optimized prompt is created, **When** I check for incomplete work, **Then** no [TODO] placeholders remain in the text

---

### User Story 3 - Push Optimized Prompts to LangSmith (Priority: P3)

As a prompt engineer, I need to publish my optimized prompt to LangSmith Prompt Hub so it can be evaluated and shared publicly.

**Why this priority**: Publishing enables evaluation and fulfills the requirement of having a public prompt in the Hub.

**Independent Test**: Can be tested by running the push script and verifying the prompt appears in the LangSmith dashboard under the user's namespace.

**Acceptance Scenarios**:

1. **Given** an optimized prompt exists at `prompts/bug_to_user_story_v2.yml`, **When** I run the push script, **Then** the prompt is uploaded to LangSmith as `{username}/bug_to_user_story_v2`
2. **Given** the push is successful, **When** I check the LangSmith dashboard, **Then** the prompt is visible with metadata including tags, description, and techniques used
3. **Given** the prompt is published, **When** I set visibility, **Then** the prompt is made public for evaluation

---

### User Story 4 - Evaluate Prompt Quality (Priority: P4)

As a prompt engineer, I need to run automated evaluation against my optimized prompt to measure its quality across multiple metrics.

**Why this priority**: Evaluation provides objective feedback on prompt quality and determines whether the challenge requirements are met.

**Independent Test**: Can be tested by running the evaluation script and receiving metric scores for all four evaluation criteria.

**Acceptance Scenarios**:

1. **Given** an optimized prompt has been pushed to LangSmith, **When** I run the evaluation script, **Then** I receive scores for all 4 metrics: Tone Score, Acceptance Criteria Score, User Story Format Score, and Completeness Score
2. **Given** the evaluation completes, **When** I review results, **Then** each metric shows a score between 0.0 and 1.0 with clear pass/fail status
3. **Given** all metrics >= 0.9, **When** evaluation completes, **Then** the system displays "APPROVED" status
4. **Given** any metric < 0.9, **When** evaluation completes, **Then** the system displays "FAILED" status with details of which metrics need improvement

---

### User Story 5 - Validate Prompt Structure with Tests (Priority: P5)

As a prompt engineer submitting work for academic audit, I need automated tests to validate my prompt meets all structural requirements before submission.

**Why this priority**: Tests provide confidence that the prompt meets requirements and the code will pass teacher audit.

**Independent Test**: Can be tested by running pytest and verifying all 6 required tests pass.

**Acceptance Scenarios**:

1. **Given** the optimized prompt exists, **When** I run `pytest tests/test_prompts.py`, **Then** all 6 required tests execute
2. **Given** the test suite runs, **When** `test_prompt_has_system_prompt` executes, **Then** it verifies the system prompt field exists and is non-empty
3. **Given** the test suite runs, **When** `test_prompt_has_role_definition` executes, **Then** it verifies a persona is defined
4. **Given** the test suite runs, **When** `test_prompt_mentions_format` executes, **Then** it verifies output format requirements are specified
5. **Given** the test suite runs, **When** `test_prompt_has_few_shot_examples` executes, **Then** it verifies few-shot examples are present
6. **Given** the test suite runs, **When** `test_prompt_no_todos` executes, **Then** it verifies no [TODO] markers remain
7. **Given** the test suite runs, **When** `test_minimum_techniques` executes, **Then** it verifies at least 2 techniques are listed in metadata

---

### User Story 6 - Iterate Until All Metrics Pass (Priority: P6)

As a prompt engineer, I need to iterate on my prompt (modify, push, evaluate) until all 4 metrics achieve >= 0.9.

**Why this priority**: Iteration is essential to achieving the required quality threshold - typically 3-5 iterations are needed.

**Independent Test**: Can be tested by repeating the push-evaluate cycle and tracking metric improvements across iterations.

**Acceptance Scenarios**:

1. **Given** evaluation shows metrics below 0.9, **When** I analyze the results, **Then** I can identify which aspects of the prompt need improvement
2. **Given** I modify the prompt based on feedback, **When** I push and re-evaluate, **Then** metrics should improve or the system provides guidance on what to change
3. **Given** multiple iterations, **When** all 4 metrics reach >= 0.9, **Then** the challenge is complete and ready for submission

---

### Edge Cases

- What happens when LangSmith API is unavailable or rate-limited? System displays clear error message with retry guidance.
- What happens when the bug report input is malformed or empty? Prompt handles gracefully with appropriate error message.
- What happens when evaluation dataset contains edge case bugs (very short, very long, missing fields)? Prompt must handle all 15 bug examples including edge cases.
- What happens when credentials expire mid-session? Clear re-authentication guidance is provided.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST pull prompts from LangSmith Prompt Hub using the `langchain.hub` interface
- **FR-002**: System MUST save pulled prompts locally in YAML format to `prompts/` directory
- **FR-003**: System MUST load environment variables from `.env` file for credentials
- **FR-004**: System MUST create optimized prompts with role/persona definition
- **FR-005**: System MUST include at least 2 prompt engineering techniques in the optimized prompt
- **FR-006**: System MUST include few-shot examples demonstrating input/output patterns
- **FR-007**: System MUST specify output format requirements (User Story format with Markdown)
- **FR-008**: System MUST push optimized prompts to LangSmith with versioned naming `{username}/bug_to_user_story_v2`
- **FR-009**: System MUST include metadata (tags, description, techniques) when pushing prompts
- **FR-010**: System MUST evaluate prompts against 4 metrics: Tone, Acceptance Criteria, User Story Format, Completeness
- **FR-011**: System MUST display clear pass/fail status with >= 0.9 threshold for each metric
- **FR-012**: System MUST implement 6 pytest validation tests for prompt structure
- **FR-013**: All code MUST include docstrings for functions and modules (academic audit requirement)
- **FR-014**: System MUST handle edge cases in prompt (empty input, malformed data, very long/short bugs)

### Key Entities

- **Prompt**: A structured instruction set containing system message, user message template, few-shot examples, and metadata (techniques, tags, description)
- **Bug Report**: Input data describing a software defect with fields like title, description, severity, steps to reproduce
- **User Story**: Output format following "As a [user], I want [goal], so that [benefit]" pattern with acceptance criteria
- **Evaluation Metric**: A scoring function that rates prompt output quality on a 0.0-1.0 scale
- **Dataset**: Collection of 15 bug examples (5 simple, 7 medium, 3 complex) used for evaluation

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Tone Score achieves >= 0.9 (90% quality threshold)
- **SC-002**: Acceptance Criteria Score achieves >= 0.9 (90% quality threshold)
- **SC-003**: User Story Format Score achieves >= 0.9 (90% quality threshold)
- **SC-004**: Completeness Score achieves >= 0.9 (90% quality threshold)
- **SC-005**: Average of all 4 metrics is >= 0.9
- **SC-006**: All 6 pytest validation tests pass successfully
- **SC-007**: Prompt optimization achieved within 3-5 iterations
- **SC-008**: All code passes teacher audit with proper docstrings on all functions and modules
- **SC-009**: Optimized prompt is publicly accessible on LangSmith Prompt Hub
- **SC-010**: README documentation includes: techniques applied with justification, comparative results table, execution instructions

## Assumptions

- LangSmith account is already created and API key is available
- Either OpenAI or Google Gemini API key is available for LLM operations
- The conda environment `desafio_02` is active with required dependencies
- The evaluation dataset (15 bugs) and metrics implementation are provided and should not be modified
- The user has basic familiarity with prompt engineering techniques from the course
