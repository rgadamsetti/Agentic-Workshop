# Epic 1 Context: Triage Data Schema and Seed Loader

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Establish the two foundational contracts everything else in the system depends on: a validated `TriageDecision` schema that every triage output must conform to, and an idempotent seed loader that populates the local SQLite database from the CSV files in `seed/`. No network calls, no API keys — this epic is pure data modelling and local I/O.

## Stories

- Story 1.1: TriageDecision schema (Pydantic model with validation)
- Story 1.2: Seed loader (`load_seed.py` CSV → SQLite, idempotent)

## Requirements & Constraints

- Every triage decision must carry exactly: `category` (one of `billing`, `bug`, `access`, `performance`, `how-to`), `priority` (one of `P1`–`P4`), `route` (one of `billing-team`, `bug-team`, `access-team`, `performance-team`, `how-to-team`), and a one-sentence `rationale`. Any other shape must be rejected with a structured error.
- `load_seed.py` must load `seed/tickets.csv` and `seed/customers.csv` into `app.db` as tables `tickets` and `customers`. Column names must match the CSV headers exactly. Running the script twice must yield the same database (idempotent).
- Table and column names in `app.db` are locked to what `mcp/triage_server.py` already reads — do not rename them.
- Python 3.12+, `uv` only (no `pip`). `seed/` files are read-only. No network calls, no API keys.

## Technical Decisions

- `TriageDecision` is a Pydantic v2 model. Validation errors raise a structured `ValidationError`, not a bare exception.
- Idempotency in the loader is implemented via SQLite `INSERT OR REPLACE` (or equivalent upsert) — tables are never dropped and recreated.

## Cross-Story Dependencies

- Story 1.2 (loader) may import `TriageDecision` from Story 1.1 for type reference, but the loader's primary job is database population — the dependency is soft. Story 1.1 should be merged before Story 1.2 begins.
