---

description: "Task list for Browser Local Chat"
---

# Tasks: Browser Local Chat

**Input**: Design documents from `/specs/001-browser-chat/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md)

**Tests**: Included because the constitution and implementation plan require automated behavior tests and an opt-in Microsoft Foundry Local integration check.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it uses different files and has no dependency on incomplete tasks.
- **[Story]**: Maps a task to a user story from `spec.md`.
- Every task includes the exact file path it creates or changes.

## Path Conventions

- Single Python project: `src/`, `tests/`, and `app.py` at repository root.
- Application package: `src/chat_agent/`.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize the standard Python project and local runtime dependency workflow.

- [X] T001 Create the Python project metadata and `uv` configuration in `pyproject.toml` with Python 3.11+, Streamlit, the Microsoft Foundry Local Python SDK, pytest, and pytest marker configuration.
- [X] T002 Create the application package and test directory structure in `src/chat_agent/__init__.py`, `app.py`, `tests/unit/`, `tests/contract/`, and `tests/integration/`.
- [X] T003 Install Microsoft Foundry Local runtime and CLI prerequisites on Windows with `winget install Microsoft.FoundryLocal`, then document the verified runtime commands in `specs/001-browser-chat/quickstart.md`.
- [X] T004 Resolve and lock Python dependencies with `uv sync`, committing the generated dependency lockfile in `uv.lock`.

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish shared configuration, domain state, model contract, and safe failure boundaries before any user story work.

**CRITICAL**: No user story implementation begins until this phase is complete.

- [X] T005 [P] Define application configuration fields and environment-variable defaults for the Foundry Local model alias, defaulting to `qwen2.5-0.5b`, in `src/chat_agent/config.py`.
- [X] T006 [P] Define `Question`, `ModelResponse`, `ChatExchange`, response statuses, and safe error categories in `src/chat_agent/domain.py` according to `specs/001-browser-chat/data-model.md`.
- [X] T007 [P] Define the `ChatModel` protocol and `ModelResult` contract in `src/chat_agent/model_protocol.py` according to `specs/001-browser-chat/contracts/chat-model.md`.
- [X] T008 Implement input normalization, non-empty validation, exchange state transitions, and one-pending-exchange protection in `src/chat_agent/domain.py`.
- [X] T009 Implement safe model failure categories and metadata-only logging in `src/chat_agent/chat_service.py`, excluding prompts, responses, credentials, and raw local diagnostics from logs.
- [X] T010 [P] Add unit and contract coverage for domain invariants and the model protocol in `tests/unit/test_domain.py` and `tests/contract/test_model_protocol.py`.

**Checkpoint**: Foundation ready; user story implementation can now begin.

## Phase 3: User Story 1 - Ask a Question (Priority: P1) MVP

**Goal**: Let a user submit one valid browser question and see its local model answer below it with pending and recoverable failure states.

**Independent Test**: Start Streamlit with Foundry Local available, submit one non-empty question, and verify the question, pending state, and corresponding answer or safe error appear in order.

### Tests for User Story 1

- [X] T011 [P] [US1] Add fake-model service tests for valid submission, pending-to-completed transition, model failure translation, and exactly-once exchange creation in `tests/unit/test_chat_service.py`.
- [X] T012 [P] [US1] Add an opt-in Foundry Local smoke test that loads the configured model alias and verifies a non-empty response in `tests/integration/test_foundry_local.py`.

### Implementation for User Story 1

- [X] T013 [US1] Implement the Microsoft Foundry Local SDK adapter, model alias resolution, model loading, completion call, non-empty response extraction, and safe exception translation in `src/chat_agent/foundry_adapter.py`.
- [X] T014 [US1] Implement serialized question submission through the `ChatModel` protocol and `ChatExchange` state updates in `src/chat_agent/chat_service.py`.
- [X] T015 [US1] Implement the Streamlit page title, question input, Send submission, user message rendering, pending indicator, model response rendering, and safe error display in `app.py`.
- [X] T016 [US1] Cache the Foundry Local model adapter lifecycle in the Streamlit process or session so each question does not reload or redownload the model in `src/chat_agent/foundry_adapter.py`.
- [X] T017 [US1] Run the User Story 1 unit tests and the manual single-question smoke flow from `specs/001-browser-chat/quickstart.md`, recording any setup corrections in `specs/001-browser-chat/quickstart.md`.

**Checkpoint**: User Story 1 is independently functional and is the recommended MVP release slice.

## Phase 4: User Story 2 - Continue the Conversation (Priority: P2)

**Goal**: Preserve completed question-and-answer exchanges in order and allow repeated questions during one browser session.

**Independent Test**: Submit at least 10 valid questions sequentially and verify every completed exchange remains visible in submission order without durable persistence.

### Tests for User Story 2

- [X] T018 [P] [US2] Add repeated-submission tests proving at least 10 completed exchanges preserve sequence and earlier content in `tests/unit/test_chat_service.py`.
- [X] T019 [P] [US2] Add Streamlit session-state tests or a deterministic UI orchestration harness proving completed exchanges are rendered once and in order in `tests/unit/test_app.py`.

### Implementation for User Story 2

- [X] T020 [US2] Store ordered `ChatExchange` objects in Streamlit session state without adding files, databases, cookies, or history restoration in `app.py`.
- [X] T021 [US2] Render each stored exchange with distinct user and assistant message roles and readable wrapping for long question or response content in `app.py`.
- [X] T022 [US2] Gate the question input while one request is pending and clear or reset the input only after a submission is accepted in `app.py` and `src/chat_agent/chat_service.py`.
- [X] T023 [US2] Run the repeated-session validation for 10 sequential questions and confirm no exchange replacement, reordering, or durable history behavior in `specs/001-browser-chat/quickstart.md`.

**Checkpoint**: User Stories 1 and 2 work independently, with repeated in-session exchanges preserved in order.

## Phase 5: User Story 3 - Recover From Invalid Submission (Priority: P3)

**Goal**: Prevent empty submissions from reaching the model and provide clear correction feedback.

**Independent Test**: Submit empty and whitespace-only input, verify no exchange or model call is created, then submit valid input and verify normal processing resumes.

### Tests for User Story 3

- [X] T024 [P] [US3] Add validation tests for empty, whitespace-only, trimmed, and valid questions proving invalid input never reaches the model in `tests/unit/test_domain.py`.
- [X] T025 [P] [US3] Add UI validation tests proving the validation message is shown without an empty exchange and clears on valid submission in `tests/unit/test_app.py`.

### Implementation for User Story 3

- [X] T026 [US3] Implement user-facing validation feedback and prevent model invocation for empty or whitespace-only input in `app.py`.
- [X] T027 [US3] Ensure normalized question content and validation errors are represented consistently in `src/chat_agent/domain.py` and `src/chat_agent/chat_service.py`.
- [X] T028 [US3] Verify model failures, timeouts, malformed empty responses, and retry availability use safe user-facing messages without sensitive diagnostics in `app.py` and `src/chat_agent/foundry_adapter.py`.
- [X] T029 [US3] Run the invalid-input and model-unavailable scenarios from `specs/001-browser-chat/quickstart.md` and confirm another question can be submitted after each failure.

**Checkpoint**: All three user stories are independently functional and satisfy the primary acceptance flows.

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Complete documentation, quality gates, and end-to-end validation without expanding v1 scope.

- [X] T030 [P] Add Python formatting, linting, and type-checking configuration appropriate for the project in `pyproject.toml` without introducing unnecessary runtime dependencies.
- [X] T031 [P] Add concise project setup and run instructions, including both Foundry Local installation commands and the no-Ollama boundary, in `README.md`.
- [X] T032 [P] Review `app.py` and `src/chat_agent/` for sensitive logging, accidental persistence, remote-provider calls, and unhandled error leakage.
- [X] T033 Run the complete default test suite with `uv run pytest` and the opt-in local integration suite with `uv run pytest -m foundry_integration`, recording expected prerequisites in `specs/001-browser-chat/quickstart.md`.
- [X] T034 Run all quickstart manual validation scenarios and confirm the success criteria in `specs/001-browser-chat/quickstart.md` are testable and current.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; T001 and T002 can begin in parallel, while T003 requires Windows package installation and T004 requires `pyproject.toml` from T001.
- **Foundational (Phase 2)**: Depends on Setup completion; T005, T006, and T007 can begin in parallel, then T008 and T009 depend on the domain and contract definitions, and T010 validates them.
- **User Story 1 (Phase 3)**: Depends on Foundational completion; T011 and T012 can begin in parallel, while T013-T016 implement the story and T017 validates the complete slice.
- **User Story 2 (Phase 4)**: Depends on Foundational completion and the working Streamlit path from User Story 1; T018 and T019 can begin in parallel, followed by T020-T023.
- **User Story 3 (Phase 5)**: Depends on Foundational completion and the input path from User Story 1; T024 and T025 can begin in parallel, followed by T026-T029.
- **Polish (Phase 6)**: Depends on all desired user stories; T030-T032 can begin in parallel, followed by T033-T034.

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Phase 2; no dependency on another user story and is the MVP.
- **User Story 2 (P2)**: Starts after Phase 2 and uses the US1 rendering/submission path; it must preserve US1 behavior.
- **User Story 3 (P3)**: Starts after Phase 2 and hardens the US1 input path; it must preserve successful submission behavior.

### Parallel Opportunities

- Setup: T001 and T002 can run in parallel; T003 is independent of source structure but requires the Windows environment.
- Foundation: T005, T006, T007, and T010 can be split by file after their direct prerequisites are available.
- US1: T011 and T012 can run in parallel; adapter work in T013 and service work in T014 can proceed after the protocol/domain tasks.
- US2: T018 and T019 can run in parallel; session rendering and repeated-submission service work can be split by file.
- US3: T024 and T025 can run in parallel; validation implementation and safe failure UI can be split between domain/service and UI files.
- Polish: T030, T031, and T032 can run in parallel before the final validation tasks.

## Parallel Example: User Story 1

```text
Task: T011 [US1] Fake-model service tests in tests/unit/test_chat_service.py
Task: T012 [US1] Foundry Local smoke test in tests/integration/test_foundry_local.py
```

## Parallel Example: User Story 2

```text
Task: T018 [US2] Repeated-submission tests in tests/unit/test_chat_service.py
Task: T019 [US2] Streamlit session-state tests in tests/unit/test_app.py
```

## Parallel Example: User Story 3

```text
Task: T024 [US3] Input validation tests in tests/unit/test_domain.py
Task: T025 [US3] UI validation tests in tests/unit/test_app.py
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 Setup.
2. Complete Phase 2 Foundational prerequisites.
3. Complete Phase 3 User Story 1.
4. Run `uv run pytest` and the single-question Foundry Local smoke flow.
5. Stop and validate the browser chat MVP before adding repeated-session behavior.

### Incremental Delivery

1. Add User Story 1 and demonstrate one valid question and response.
2. Add User Story 2 and demonstrate ordered repeated exchanges.
3. Add User Story 3 and demonstrate invalid-input recovery.
4. Complete Phase 6 quality, documentation, security, and quickstart validation.

## Notes

- Every task starts with `- [ ]`, has a sequential task ID, and includes a concrete file path.
- `[P]` marks only tasks that can be worked on independently without incomplete-file dependencies.
- `[US1]`, `[US2]`, and `[US3]` map directly to the prioritized stories in `spec.md`.
- Microsoft Foundry Local runtime/CLI installation and Python SDK installation are both required; Ollama is excluded.
