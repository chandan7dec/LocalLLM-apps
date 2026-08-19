# Research: Browser Local Chat

## Decision 1: Use a single uv-managed Python project

- **Decision**: Use Python 3.11 or newer with `pyproject.toml`, a committed `uv.lock`, and a project-local virtual environment managed by `uv`.
- **Rationale**: This matches the requested standard Python workflow and gives repeatable dependency resolution and runnable commands such as `uv run streamlit run app.py` and `uv run pytest`.
- **Alternatives considered**: A manually managed `venv` with `requirements.txt` was rejected because it does not provide the requested lockfile-oriented project workflow. Multiple language services were rejected because the constitution requires a small, understandable v1.

## Decision 2: Use Streamlit for the browser interface

- **Decision**: Render the chat with Streamlit chat primitives and keep completed exchanges in Streamlit session state only.
- **Rationale**: Streamlit directly provides browser UI, chat message rendering, input submission, and rerun-aware session state without introducing a separate frontend language or server layer. This satisfies the one-language constraint and the v1 no-history boundary.
- **Alternatives considered**: A JavaScript frontend with a Python API would add a second language and an unnecessary integration boundary. A custom HTML server would require more UI and request lifecycle code than this feature needs.

## Decision 3: Use the Microsoft Foundry Local Python SDK

- **Decision**: Put all local-model lifecycle and completion calls behind a `FoundryLocalAdapter` implementing a small application-level `ChatModel` protocol. Use the Foundry Local Python SDK, with the Windows SDK package selected for Windows where required by the official installation guidance.
- **Rationale**: Microsoft documents a Python 3.11+ native chat-completions flow using `FoundryLocalManager`, a catalog model alias such as `qwen2.5-0.5b`, model loading, and chat completion. An adapter prevents Streamlit code from depending on SDK details and allows a future local model or SDK revision without changing the UI.
- **Alternatives considered**: The OpenAI-compatible local endpoint was considered as a fallback boundary, but direct SDK use keeps the v1 integration explicitly Foundry Local and avoids managing a separate endpoint/client configuration. Ollama is explicitly excluded.

## Decision 4: Select a small Qwen model by configurable alias

- **Decision**: Default the model alias to `qwen2.5-0.5b` and allow the alias to be changed through local project configuration without changing application logic.
- **Rationale**: Microsoft Foundry Local documents this alias in its Python quickstart, and it is appropriate for an initial local test. Foundry Local can resolve an alias to a hardware-appropriate variant.
- **Alternatives considered**: Hard-coding a model ID was rejected because model variants differ by hardware. A larger model was rejected for the initial responsiveness and setup goal.

## Decision 5: Require Foundry Local as a local runtime prerequisite

- **Decision**: The quickstart requires the Foundry Local installation, a reachable local service, and an available model before starting Streamlit. The application translates startup, loading, timeout, and completion failures into safe user-facing error categories.
- **Rationale**: Foundry Local is a separate local runtime and first-run model or execution-provider downloads can be slow. Treating it as a prerequisite makes the app lifecycle predictable and keeps the application focused on chat behavior.
- **Alternatives considered**: Automatically starting the Foundry daemon from Streamlit was rejected for v1 because subprocess ownership and platform-specific startup behavior would increase complexity and make failures less transparent.

## Decision 6: Serialize one active request per browser session

- **Decision**: Disable or gate new submission while a request is active; append a completed or failed exchange only once the request resolves.
- **Rationale**: Streamlit reruns the script on interaction. A single active request prevents duplicate submissions and preserves the spec's deterministic exchange ordering.
- **Alternatives considered**: Concurrent requests were rejected because v1 does not define ordering, cancellation, or queue semantics.

## Decision 7: Test the model boundary without requiring a model for every test

- **Decision**: Unit-test UI orchestration and validation with a fake `ChatModel`; add a separate opt-in integration smoke test that requires a running Foundry Local installation and the configured model.
- **Rationale**: Most behavior can be tested quickly and deterministically without downloading a model, while one real integration check verifies the request and response contract required by the constitution.
- **Alternatives considered**: Requiring Foundry Local for the full test suite was rejected because first-run downloads and device availability would make ordinary validation slow and unreliable.

## Sources

- Microsoft Foundry Local Python quickstart: https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-local/get-started
- Microsoft Foundry Local CLI reference: https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-local/reference/reference-cli
- Streamlit chat API: https://docs.streamlit.io/develop/api-reference/chat
- uv project documentation: https://docs.astral.sh/uv/concepts/projects/
