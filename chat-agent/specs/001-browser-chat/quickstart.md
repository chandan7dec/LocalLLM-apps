# Quickstart: Browser Local Chat

## Prerequisites

- Windows with Python 3.11 or newer.
- `uv` installed and available on `PATH`.
- Microsoft Foundry Local installed. On Windows, the documented installer is:

  ```powershell
  winget install Microsoft.FoundryLocal
  ```

- A Foundry Local model alias available for the test, initially `qwen2.5-0.5b`.

Verify the runtime and model catalog:

```powershell
foundry --version
foundry server status
foundry model list --type chat --search qwen
```

If the local server is not reachable, restart it:

```powershell
foundry server restart
```

## Install the Project

From the repository root:

```powershell
uv sync
```

The project MUST declare runtime and development dependencies in `pyproject.toml` and commit
`uv.lock`. Do not install Ollama or add Ollama-compatible application code.

## Start the Application

Ensure Foundry Local can load the selected model, then run Streamlit:

```powershell
foundry model load qwen2.5-0.5b
uv run streamlit run app.py
```

Open the local URL printed by Streamlit in a browser.

## Manual Validation

1. Enter a non-empty question and select Send.
2. Confirm the question appears as a user message, a pending state is visible while work is in progress, and the model response appears below it.
3. Submit at least 10 questions sequentially and confirm all completed exchanges remain in order without replacing earlier exchanges.
4. Submit empty and whitespace-only input and confirm no exchange is added and a validation message is shown.
5. Stop or disconnect Foundry Local, submit a question, and confirm a safe recoverable error appears without credentials or raw diagnostics.
6. Enter a long question and verify readable wrapping and access to earlier exchanges.

## Automated Validation

```powershell
uv run pytest
```

The default suite uses a fake model adapter and does not require a downloaded model.

Run the real local integration smoke test only when Foundry Local is installed, reachable,
and the configured model is available:

```powershell
$env:RUN_FOUNDRY_INTEGRATION = "1"
uv run pytest -m foundry_integration
```

Expected outcome: the integration test receives a non-empty response from the configured local
model, and the regular suite verifies validation, pending/error handling, repeated exchanges,
and ordering without remote network calls.
