# Chat Model Contract

## Purpose

Define the boundary between the Streamlit chat orchestration and Microsoft Foundry Local.
The UI and session-state code MUST depend on this contract rather than SDK-specific calls.

## Application Interface

The application-level model adapter exposes one operation:

```text
answer(question: NonEmptyText) -> ModelResult
```

### Input

- `question` is trimmed text with at least one non-whitespace character.
- The adapter MUST NOT receive an empty or whitespace-only question.
- The adapter receives the configured model alias through initialization, not from browser input.

### Successful Result

```text
ModelResult(
  status="completed",
  content=<non-empty generated text>,
  error_category=null,
)
```

### Failure Result

```text
ModelResult(
  status="failed",
  content=null,
  error_category=<unavailable | timeout | invalid_response>,
)
```

Failure details MAY be logged as a category and duration, but raw prompts, responses,
credentials, and local diagnostic payloads MUST NOT be logged or displayed.

## Foundry Local Mapping

`FoundryLocalAdapter` maps the contract to the Microsoft Foundry Local Python SDK:

1. Initialize the local manager.
2. Resolve the configured model alias, defaulting to `qwen2.5-0.5b`.
3. Ensure the model is available and loaded.
4. Submit the user message through the SDK chat client.
5. Extract non-empty response text into `ModelResult`.
6. Translate SDK/runtime failures into the contract's safe error categories.

Model lifecycle initialization SHOULD be cached per Streamlit session or application process
so each question does not redownload or reload the model.

## UI Contract

The browser interface MUST expose:

- A question input area.
- A Send control.
- Ordered user and assistant message displays.
- A visible pending state during model work.
- A safe validation or model error state.

The UI MUST gate submissions while one request is pending and MUST append each exchange only
once. Refreshing the browser is not required to restore exchanges.
