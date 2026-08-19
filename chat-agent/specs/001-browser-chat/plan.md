# Implementation Plan: Browser Local Chat

**Branch**: `001-browser-chat` | **Date**: 2026-08-19 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Provide a single-language browser chat experience in Python. Streamlit owns the browser
interaction and temporary session display, while a small model boundary delegates valid
questions to Microsoft Foundry Local. The default local model alias is `qwen2.5-0.5b`, and
the model adapter is replaceable without changing the UI orchestration. The project uses `uv`,
`pyproject.toml`, and `uv.lock` for standard Python dependency and environment management.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+

**Primary Dependencies**: Streamlit; Microsoft Foundry Local Python SDK; pytest; uv for project management

**Storage**: Streamlit session state only; no durable storage or history restoration

**Testing**: pytest unit/contract tests with a fake model adapter; opt-in Foundry Local integration test

**Target Platform**: Windows development machine with a modern web browser and Microsoft Foundry Local

**Project Type**: Streamlit web application with local model integration

**Performance Goals**: Show a pending state immediately; show a safe failure within 5 seconds after failure detection; avoid model reload for each question

**Constraints**: Local-only inference; no Ollama; no remote providers; no message persistence; one active request per browser session; first-run model/provider download may be slow

**Scale/Scope**: One simple chat screen, one active user session, at least 10 sequential exchanges in a session, one swappable model adapter

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **User-first simplicity**: PASS. The design contains one chat screen and no history, accounts,
  social features, or decorative product scope.
- **Local-first data handling**: PASS. Inference uses Microsoft Foundry Local on the same
  environment; no remote provider or durable message store is introduced.
- **Observable, honest responses**: PASS. The UI contract includes distinct user, pending,
  completed, and safe failed states.
- **Behavior-first quality**: PASS. pytest fake-adapter tests cover validation, success,
  failure, repeated exchanges, and ordering; a marked integration test checks Foundry Local.
- **Small, reversible changes**: PASS. Streamlit and one model adapter are the only application
  boundaries; model selection is configuration-driven and no persistence layer is added.

No constitution violations require a complexity exception.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
app.py
pyproject.toml
uv.lock
src/
└── chat_agent/
  ├── __init__.py
  ├── config.py
  ├── domain.py
  ├── model_protocol.py
  ├── foundry_adapter.py
  └── chat_service.py
tests/
├── unit/
│   ├── test_domain.py
│   └── test_chat_service.py
├── contract/
│   └── test_model_protocol.py
└── integration/
  └── test_foundry_local.py
```

**Structure Decision**: Use one Python project with a thin `app.py` Streamlit entry point and
an importable `src/chat_agent` package. Domain validation and exchange state stay independent
from UI rendering. `foundry_adapter.py` owns the Microsoft Foundry Local SDK boundary, while
`chat_service.py` owns serialized submission and safe error translation. Tests are split by
unit, application contract, and opt-in local-runtime integration concerns.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | The selected single-project structure satisfies the constitution without an exception. |
