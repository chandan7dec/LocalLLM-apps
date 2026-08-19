# Local Chat Agent

A simple browser chat agent backed by Microsoft Foundry Local.

## Prerequisites

- Windows with Python 3.11 or newer.
- `uv` installed and available on `PATH`.
- Microsoft Foundry Local installed as the local runtime and CLI:

	```powershell
	winget install Microsoft.FoundryLocal
	```

Verify the installation and local service:

```powershell
foundry --version
foundry server status
```

## Development Setup

From the repository root, sync the `uv` environment. This installs the Microsoft Foundry
Local Python SDK, Streamlit, pytest, Ruff, and mypy from `pyproject.toml`:

```powershell
uv sync
```

The initial test model is `qwen2.5-0.5b`:

```powershell
foundry model load qwen2.5-0.5b
```

Start the browser application:

```powershell
uv run streamlit run app.py
```

Open the local URL printed by Streamlit, enter a question, and select Send. Exchanges remain
in the current browser session only; no chat history is persisted.

## Validation

Run deterministic tests:

```powershell
uv run pytest
```

Run formatting, linting, and type checks:

```powershell
uv run ruff format --check .
uv run ruff check .
uv run mypy app.py src tests
```

Run the real Foundry Local smoke test when the local runtime and model are available:

```powershell
$env:RUN_FOUNDRY_INTEGRATION = "1"
uv run pytest -m foundry_integration
```

This project uses Microsoft Foundry Local only. It does not install, call, or depend on Ollama.
