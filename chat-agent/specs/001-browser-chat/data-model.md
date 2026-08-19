# Data Model: Browser Local Chat

## Question

Represents text entered and submitted by the browser user.

| Field | Type | Rules |
| --- | --- | --- |
| `content` | string | Required after trimming; MUST NOT be empty or whitespace-only. |
| `submitted_at` | local timestamp | Optional diagnostic metadata; MUST NOT be shown as a requirement of the v1 UI. |

## Model Response

Represents the local model result associated with a question.

| Field | Type | Rules |
| --- | --- | --- |
| `content` | string | Required for a completed response; MUST be non-empty. |
| `status` | enum | `pending`, `completed`, or `failed`. |
| `error_category` | enum or null | `unavailable`, `timeout`, `invalid_response`, or null when completed. |

## Chat Exchange

Represents one ordered question and its response state during the current browser session.

| Field | Type | Rules |
| --- | --- | --- |
| `question` | Question | Required. |
| `response` | Model Response | Required; starts as `pending`, then becomes `completed` or `failed`. |
| `sequence` | positive integer | Monotonically increases for each accepted submission in the session. |

## Relationships and State

- One browser session contains an ordered list of zero or more Chat Exchanges.
- Each Chat Exchange contains exactly one Question and one Model Response state.
- A valid submission transitions `new input -> pending -> completed` or `new input -> pending -> failed`.
- Empty input does not create a Chat Exchange or call the model.
- Completed exchanges remain in session state until the browser session ends or is refreshed; no durable storage or restoration exists in v1.
- Only one exchange may be `pending` at a time.
