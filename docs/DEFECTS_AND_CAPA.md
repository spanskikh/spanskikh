# Cluster Defect Log & Process Improvements (CAPA Registry)

This register tracks real defects discovered during verification across the `hippo` + `rhino` neuro-symbolic cluster (`sandbox-init`, `abstract-ops`, `interview-ops`, `hostel-ops`), their root causes, regression tests, and systemic Corrective & Preventive Actions (`CAPA`).

## Summary Matrix

| Defect ID | Repo / CR | Severity | Summary | Root Cause | Process Improvement |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BUG-002** | All 4 dev repos (`CR-021`) | Medium (Test Blind Spot) | Cyrillic character `(Cyrillic `ty`)` in `docs/releases/v0.7.0-refine.md` bypassed `tests/test_docs_quality.py`. | `audit_documentation` scanned only `required_files` rather than all tracked `*.md` files. | **CAPA-005** |
| **BUG-001** | `hostel-ops` (`CR-007`) | High (Data Integrity / TOCTOU) | Overlapping bookings (`[10, 14)` vs `[12, 16)`) both committed on live `rhino` PostgreSQL under barrier concurrency. | `CREATE TABLE IF NOT EXISTS` silently skipped adding `bookings_no_overlap_excl` (`EXCLUDE USING gist`) to pre-existing `v0.1.0` table; unit tests checked DDL strings rather than live catalog state. | **CAPA-001** |

---

## Detailed Records

### BUG-001: Silent DDL Schema Drift on `CREATE TABLE IF NOT EXISTS` (`hostel-ops`, CR-007)
- **Symptom:** Running `test_concurrent_overlapping_bookings_enforced_by_rhino_gist` against `rhino` (`127.0.0.1:15432`) produced `2` committed bookings instead of `1` commit + `1` `psycopg.errors.ExclusionViolation` (`23P01`).
- **Root Cause:** In `CR-004` (`v0.2.0`), `CONSTRAINT bookings_no_overlap_excl` was placed inside `CREATE TABLE IF NOT EXISTS bookings`. On stateful `rhino`, `bookings` already existed from `v0.1.0`, so PostgreSQL ignored the new constraint definition without error.
- **Fix:** Added an idempotent `DO $$ ... IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'bookings_no_overlap_excl') THEN ALTER TABLE bookings ADD CONSTRAINT ... $$` block in `src/hostel_ops/storage.py`.
- **Regression Evidence:** `tests/test_live_gist_concurrency.py` (`@pytest.mark.integration`) — verified `1 passed` against live `rhino` PostgreSQL.

### CAPA-001: Idempotent DDL Evolution & Stateful Integration Gate
- **Scope:** All PostgreSQL / DuckDB persistence layers (`hostel-ops`, `interview-ops`, `sandbox-init`).
- **Preventive Rule 1 (DDL):** Never rely on `CREATE TABLE IF NOT EXISTS` to add constraints, columns, or indexes to existing tables. Every schema invariant must be enforced by an idempotent catalog check (`pg_constraint`, `pg_indexes`, `CREATE INDEX IF NOT EXISTS`).
- **Preventive Rule 2 (Verification):** DDL and concurrency invariants require `@pytest.mark.integration` execution against stateful cluster databases on `rhino`, complementing mocked/in-memory unit tests.

## CAPA-002: Cross-Session Context Drift, Toolchain Mismatch & Language Governance
- **Triggering Incidents:** New release chat sessions guessing unverified Pydantic/MCP schemas, invoking `uv` instead of `.venv/bin/`, pasting `set -e` into interactive shells, and risking Russian text leakage into Git artifacts.
- **Root Cause:** Operational engineering conventions existed only in ephemeral chat history rather than a versioned, machine-checked repository standard.
- **Corrective & Preventive Action (`CR-013`):** Codified `DEVPROCESS.md` across all 4 repositories (`Zero-Orphan Artifact Rule`, `Chat vs. Git Language Split`, `Zero-Guesswork Contract Rule`, and `.venv/bin/` + `./scripts/run_logged.sh` standard), backed by `tests/test_docs_quality.py` (`LANGUAGE_DRIFT_CYRILLIC`).
## CAPA-003: PTY Paste Buffer Truncation, Log Flooding & Scratchpad Hygiene
- **Triggering Incidents (`v0.7.0`):** Multi-line heredoc pastes exceeding ~1.5 KiB were truncated or stripped of leading spaces by the KDE Konsole canonical PTY buffer; unfiltered `ruff` output flooded stdout; a temporary log touched system `/tmp`.
- **Root Cause:** `DEVPROCESS.md` lacked explicit byte/line thresholds (`<= 1.5 KiB` / `<= 35 lines`) and an automated gate verifying `DEVPROCESS.md` invariants.
- **Corrective & Preventive Action (`CR-019`):** Codified **PTY Paste Cap (`<= 35 lines / <= 1.5 KiB`)**, `logs/` summary caps (`<= 15` lines), and zero `/tmp` usage in `DEVPROCESS.md` across all 5 repos, enforced by `tests/test_docs_quality.py`.

## CAPA-004: Cluster-Wide Governance Document Duplication & Drift
- **Triggering Incident (`v0.7.0`):** SHA-256 audit across the 4 dev repositories revealed identical or whitespace-drifting copies of `DEVPROCESS.md`, `RELEASES.md`, `docs/DEFECTS_AND_CAPA.md`, and `docs/releases/*`.
- **Root Cause:** Cluster-wide governance artifacts were stored inside each product repository instead of the root profile hub `spanskikh/spanskikh`.
- **Corrective & Preventive Action (`CR-020`):** Consolidated `DEVPROCESS.md`, `RELEASES.md`, `docs/DEFECTS_AND_CAPA.md`, and `docs/releases/*` into `spanskikh/spanskikh` as the Single Source of Truth, removed copies from the 4 dev repos, and enforced anti-duplication (`CLUSTER_DOC_DUPLICATE`) in `tests/test_docs_quality.py`.

### BUG-002: Incomplete Markdown Tree Scope in `LANGUAGE_DRIFT_CYRILLIC` Auditor (`CR-021`)
- **Symptom:** `docs/releases/v0.7.0-refine.md` contained Cyrillic `(Cyrillic `ty`)` and passed `test_repository_documentation_passes_quality_gate` across all 4 dev repos, failing only when audited by `spanskikh/tests/test_profile_quality.py`.
- **Root Cause:** `audit_documentation` iterated over `loaded` (`required_files` only) instead of scanning all repository `*.md` files.
- **Fix:** Extended `audit_documentation` to scan every non-cache `*.md` file in the repository and added the `cyrillic_in_subdoc` counterexample.

## CAPA-005: Full-Tree Markdown Hygiene & Cluster SSoT Enforcement
- **Preventive Rule (`CR-021`):** Every repository documentation gate must scan all tracked `*.md` files recursively for Cyrillic and placeholders, and dev repos must fail with `CLUSTER_DOC_DUPLICATE` if cluster-level governance docs (`DEVPROCESS.md`, `RELEASES.md`, `docs/DEFECTS_AND_CAPA.md`, `docs/releases/*`) are duplicated locally.
