---
title: 'TriageDecision schema'
type: 'feature'
created: '2026-09-26'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - _bmad-output/specs/spec-epic-1/SPEC.md
  - TRIAGE_POLICY.md
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The triage agent (Epic 2) and the eval harness (Epic 3) both need a single, validated shape for a triage decision. Without it, each caller invents its own structure and there is no shared rejection contract.

**Approach:** Create a Pydantic v2 `TriageDecision` model in `schema.py` at the project root. The model enforces the five categories, four priorities, five routes, and a non-empty rationale string. Invalid input raises a structured `ValidationError`.

</frozen-after-approval>

## Implementation Notes

Created `schema.py` at project root. Added `@model_validator(mode="after")` to enforce that `route` matches `category` (e.g. `billing` → `billing-team`); patched from Blind Hunter finding.

## Review Triage Log

- `false` — no docstring: project instructions say write no comments by default.
- `false` — explicit Literal validators: Pydantic already emits structured errors; extra validators add no value.
- `patch` (applied) — category/route mismatch: real gap, added `route_matches_category` model_validator.
- `low` (rejected) — min-length on rationale: spec says non-empty; 1-char string is contrived and won't occur in practice.
- `low` (rejected) — `__all__` missing: no downstream `import *` in this repo; not user-visible.

