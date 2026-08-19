<!--
Sync Impact Report
- Version change: scaffold -> 1.0.0
- Modified principles: none; established all five project principles
- Added sections: Product Boundaries and Safety; Development Workflow
- Removed sections: none
- Follow-up TODOs: Confirm the original ratification date when the project adopts this constitution.
-->

# Local Chat Agent Constitution

## Core Principles

### I. User-First Simplicity
The product MUST optimize for one clear flow: a user submits a question and receives an
answer from the configured local language model. Version 1 MUST avoid features that do not
directly support this flow, including conversation history, accounts, social features, and
decorative interface complexity. Every addition MUST identify the user outcome it improves.

### II. Local-First Data Handling
User questions and model responses MUST remain on the local environment by default. The
application MUST NOT transmit chat content to third-party services unless a future change
explicitly defines that behavior, its user consent, and its privacy implications. Logs MUST
exclude message content and credentials unless a documented exception is approved.

### III. Observable, Honest Responses
The interface MUST clearly distinguish user messages, model responses, loading states, and
errors. The application MUST never present an unavailable, incomplete, or failed model result
as a successful answer. When the local model cannot respond, the user MUST receive a concise,
actionable error and the interface MUST remain usable for another attempt.

### IV. Behavior-First Quality
Each user-visible behavior MUST have an automated test or a documented manual verification
step. Tests MUST cover successful question-and-answer flow, empty or invalid input, model
unavailability, and repeated submissions. Changes to the local-model boundary MUST include
an integration check that verifies the request and response contract.

### V. Small, Reversible Changes
The codebase MUST favor the smallest design that satisfies the current requirement. New
dependencies, persistent storage, background services, and cross-cutting abstractions require
explicit justification. Features MUST be separable and reversible where practical so the v1
chat experience remains easy to understand, test, and operate.

## Product Boundaries and Safety

The v1 product is a simple chat application for questions answered by a locally running
language model. It includes message entry, submission, response display, loading feedback, and
recoverable error feedback. It excludes chat history, user accounts, multi-user collaboration,
model training, remote model providers, and long-term storage.

The application MUST treat model output as generated content rather than verified fact. It
MUST avoid claiming that an answer is authoritative when the model is uncertain or unavailable.
Credentials, local model configuration, and personal message content MUST be handled as
sensitive data and MUST NOT be exposed in client-visible diagnostics.

## Development Workflow

Every feature or bug fix MUST state its user-facing behavior, acceptance checks, and effect on
the local-model boundary. Before integration, contributors MUST run the narrowest relevant
automated tests and perform a manual smoke test of submitting a question and receiving a
response. A change is not complete while it introduces unhandled errors, exposes sensitive
content, or leaves the primary chat flow unusable.

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

This constitution supersedes conflicting project practices for the local chat agent. Amendments
MUST document the affected principles, rationale, scope, and migration impact. Versioning uses
Semantic Versioning: MAJOR for incompatible governance changes, MINOR for new or materially
expanded principles, and PATCH for clarifications or wording-only changes. Each implementation
plan and review MUST verify compliance with the principles above; any exception MUST be written
down with an owner and an expiry or revisit condition.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): confirm initial adoption date | **Last Amended**: 2026-08-19
