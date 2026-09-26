---
id: SPEC-epic-1
companions: []
sources:
  - ../../../../INTENT.md
---

> **Canonical contract.** This SPEC and the files in `companions:` are the complete, preservation-validated contract for what to build, test, and validate. Source documents listed in frontmatter are for traceability — consult them only if you need narrative rationale or prose color this contract intentionally omits.

# Epic 1: Triage Data Schema and Seed Loader

## Why

The triage agent (built in Epic 2) must produce decisions in a known shape and read ticket data from a local database. Before any agent code exists, the decision schema and the data layer must be pinned: every downstream consumer — the MCP server, the eval harness, and the agent itself — depends on these contracts being stable and correct. This epic establishes both.

## Capabilities

- **CAP-1**
  - **intent:** The system can validate that a triage decision carries a category, a priority, a route, and a one-sentence rationale — and rejects anything that does not with a clear, structured error.
  - **success:** A `TriageDecision` constructed with all valid fields passes validation. A `TriageDecision` missing any field, or carrying a value outside the allowed set, raises a structured validation error (not a bare exception) with a message naming the violation.

- **CAP-2**
  - **intent:** A single command loads `seed/tickets.csv` and `seed/customers.csv` into `app.db` as the tables `tickets` and `customers`, with columns matching the CSV headers exactly.
  - **success:** `uv run python load_seed.py` completes without error on a fresh machine. Running it a second time yields a database with the same row count and content as the first run (idempotent). `mcp/triage_server.py` can query both tables without modification.

## Constraints

- Python 3.12 or newer; all packages managed with `uv add`, never `pip`.
- `seed/` files are read-only; `load_seed.py` reads them only, never writes them.
- No network calls and no API keys anywhere in this epic.
- Table names (`tickets`, `customers`) and all column names in `app.db` must match what `mcp/triage_server.py` already expects; do not rename them.

## Non-goals

- The LangChain agent, MCP tool wiring, MLflow tracing, evals, and any user interface are out of scope.

## Success signal

- `uv run python load_seed.py` loads both CSVs into `app.db` idempotently, and a `TriageDecision` with valid fields is accepted while one with an invalid or missing field is rejected with a clear error.

## Assumptions

- `mcp/triage_server.py` column expectations can be inferred by reading that file; no separate schema document exists.
- Idempotency is implemented via `INSERT OR REPLACE` or equivalent SQLite upsert, not by dropping and recreating tables.
