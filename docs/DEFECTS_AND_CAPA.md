# Cluster Defect Log & Process Improvements (CAPA Registry)

This register tracks real defects discovered during verification across the `hippo` + `rhino` neuro-symbolic cluster (`sandbox-init`, `abstract-ops`, `interview-ops`, `hostel-ops`), their root causes, regression tests, and systemic Corrective & Preventive Actions (`CAPA`).

## Summary Matrix

| Defect ID | Repo / CR | Severity | Summary | Root Cause | Process Improvement |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BUG-005** | `sandbox-init` (`CR-024` / `v0.9.1`) | Medium (CI Portability & Registry Drift) | GitHub Actions run `45188880471` failed in `test_run_integration_script_dry_run` because `scripts/run_integration.sh` hardcoded `.venv/bin/python` absent on hosted CI runners, and `BUG-005` was initially patched in `CHANGELOG.md` without updating `DEFECTS_AND_CAPA.md` or `pyproject.toml`. | Shell wrapper assumed local `.venv/bin/python` instead of `PYTHON_BIN -> .venv/bin/python -> python3 -> python` fallback; release closeout lacked mandatory `DEFECTS_AND_CAPA.md` and `pyproject.toml` sync gates. | **CAPA-010**, **CAPA-011** |
| **BUG-004** | All 4 dev repos (`v0.8.0` / `CR-026`) | High (Supply-Chain Hygiene) | Editable CI installs wrote PEP 610 `file:///home/<user>/...` URIs into `CycloneDX` SBOM `externalReferences`, tripping host-path hygiene assertions. | `pip install -e ".[dev]"` embeds local `direct_url.json` metadata serialized by `cyclonedx-py environment`. | **CAPA-007** |
| **BUG-003** | All 4 dev repos (`CR-023`) | Medium (Oracle Determinism & Timeout) | Live `Ollama` doc rubric judge hit `httpx.ReadTimeout` (`60.0s`) on cold CPU load and drifted from `DocRubricScore` schema under generic `"format": "json"`. | Generic JSON mode does not enforce JSON Schema fields/lengths, and `60.0s` timeout was below cold CPU GGUF load + prefill latency. | **CAPA-006** |
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

### BUG-003: Unconstrained JSON Mode & Cold-Load ReadTimeout in Live Ollama Rubric Judge (`CR-023`)
- **Symptom:** `_judge_doc_with_ollama` hit `httpx.ReadTimeout` at `60.0s` on cold CPU model load (`qwen2.5-coder:7b`, `5.07 GiB` on `hippo`), and under `"format": "json"` omitted `interviewer_market_value` or exceeded `rationale` `max_length=400`.
- **Root Cause:** Ollama's generic `"format": "json"` constrains JSON syntax rather than JSON Schema fields/lengths, and `timeout=60.0` was shorter than cold GGUF load + prefill on CPU (`i5-9500`).
- **Fix:** Switched `/api/generate` `"format"` to `DocRubricScore.model_json_schema()` (grammar-constrained decoding in `llama.cpp`) with `"options": {"temperature": 0.0}` and `timeout=180.0` across all 4 dev repos.

## CAPA-006: Grammar-Constrained Structured Outputs for All LLM-as-a-Judge Oracles
- **Preventive Rule (`CR-023`):** Never rely on plain `"format": "json"` or prompt-only field hints for Pydantic-validated LLM judges. Always pass `<PydanticModel>.model_json_schema()` to Ollama's structured-output `format` parameter with `temperature=0.0` and CPU-safe timeouts (`>= 180.0s`).

### BUG-004: PEP 610 `file:///home/<user>/...` URI Leakage in CI `CycloneDX` SBOM (`v0.8.0`)
- **Symptom:** GitHub Actions `Verify & CycloneDX SBOM` failed on `test_cyclonedx_sbom_reproducibility_and_hygiene` (`assert '/home/' not in raw`) because `pip install -e ".[dev]"` writes PEP 610 `direct_url.json` (`file:///home/<user>/work/...`) into editable package metadata serialized by `cyclonedx-py environment`.
- **Root Cause:** Editable installs in CI embed runner-specific `file://` paths into `externalReferences` of the generated `CycloneDX` BOM.
- **Fix:** Stripped `file://` `externalReferences` during SBOM serialization in `.github/workflows/ci.yml` and `tests/test_sbom_and_contracts.py` across all 4 dev repositories.

## CAPA-007: Sanitize PEP 610 Local `file://` References in Release SBOM Artifacts
- **Preventive Rule:** Every CI SBOM pipeline and reproducibility test must strip local `file://` `externalReferences` before asserting host-path hygiene (`/home/`, `/Users/`) and publishing SBOM artifacts.

## CAPA-008: Workspace Root Launch & Two-Phase Plan-Then-Edit Gate for Antigravity CLI (`agy`)
- **Triggering Incidents (`v0.9.0` / `CR-027` & `CR-024`):**
  1. Launching `agy` inside a child repository directory stops upward rule discovery at the child `.git` boundary, truncating visibility of the workspace instruction anchor (`~/projects/GEMINI.md`) and Single Source of Truth governance files in `~/projects/spanskikh/`.
  2. Running direct code edits without an upfront read-only inspection pass risks unverified contract assumptions against `models.py`, `contracts.py`, `server.py`, or `docs/releases/vX.Y.Z-refine.md` acceptance criteria (`CAPA-002`).
- **Root Cause:** Multi-repository agentic execution lacked an explicit workspace-root launch rule, tracked symlink topology, and mandatory read-only planning gate prior to file mutation.
- **Corrective & Preventive Action (`CR-027`):**
  1. **Workspace Root Launch (`--add-dir ~/projects`):** Always launch `agy` from `~/projects` (or pass `--add-dir ~/projects`) with `~/projects/GEMINI.md` and `~/projects/AGENTS.md` symlinked to Git-tracked `spanskikh/GEMINI.md`.
  2. **Mandatory Two-Phase Plan-Then-Edit Gate:** Execute a fast read-only Phase 1 plan pass (`agy chat --mode plan --add-dir ~/projects`) to inspect target contracts and acceptance criteria before running Phase 2 edits and verification (`agy chat --mode accept-edits --add-dir ~/projects`).
  3. **Strict HITL Git Gate:** Agents may edit files, run non-mutating git diagnostics (`git status`, `git diff`, `git log`, `git rev-parse`), and run verification gates routed to `logs/`; `git commit`, `git tag`, `git push`, and destructive filesystem commands remain strictly human-only (enforced in `DEVPROCESS.md` and `~/.config/antigravity/settings.json`).

## CAPA-009: Agent Prompt Auditability & Phase-Log Traceability
- **Triggering Incident (`v0.9.0`):** During multi-CR execution (`CR-027`, `CR-024`, `CR-025`, `CR-026`), phase logs were split across repository log directories (`sandbox-init/logs/v0.9.0-cr024-{plan,edit}.log` vs `spanskikh/logs/v0.9.0-cr025-plan.log` and `v0.9.0-cr026-plan.log`), and the exact Phase 1 / Phase 2 CLI prompts were not archived alongside `docs/dev-log/` and release records.
- **Root Cause:** `DEVPROCESS.md` mandated logging linter/typecheck/pytest runs via `./scripts/run_logged.sh` (`CAPA-003`) but did not standardize archival of the exact Phase 1 Plan and Phase 2 Edit/Verify agent prompts and their corresponding `logs/vX.Y.Z-crNNN-{plan,edit}.log` paths.
- **Corrective & Preventive Action (`v0.9.0` Closeout -> `v0.10.0` Gate):**
  1. **Canonical Phase Log Naming (`logs/vX.Y.Z-crNNN-{plan,edit}.log`):** Route every Phase 1 (`--mode plan`) and Phase 2 (`--mode accept-edits`) `agy` invocation to `logs/vX.Y.Z-crNNN-plan.log` and `logs/vX.Y.Z-crNNN-edit.log` in addition to per-tool verification logs (`./scripts/run_logged.sh`).
  2. **Mandatory Prompt & Log Traceability Table:** Document the exact Phase 1 Plan and Phase 2 Edit/Verify prompt summaries, CLI flags, commit SHAs, and phase/verification log artifact paths for every Change Request in `docs/releases/vX.Y.Z-retrospective.md` and `docs/dev-log/` so agent runs remain reproducible and forensically auditable.

### BUG-005: Hardcoded `.venv/bin/python` in `run_integration.sh` on Hosted CI Runner (`sandbox-init`, GitHub Actions run `45188880471`)
- **Symptom:** GitHub Actions CI run `45188880471` failed in `tests/test_topology.py::test_run_integration_script_dry_run` because `scripts/run_integration.sh` hardcoded `TOPOLOGY_PY="${REPO_ROOT}/.venv/bin/python"` (which does not exist on hosted GitHub Actions runners using the global toolcache interpreter), and the dry-run test constructed a restricted `PATH` (`"/usr/bin:/bin"`) that stripped the active Python interpreter directory. In addition, `BUG-005` was initially recorded in `sandbox-init/CHANGELOG.md` without simultaneous registration in `spanskikh/docs/DEFECTS_AND_CAPA.md`.
- **Root Cause:** Shell wrapper script assumed a local `.venv/bin/python` checkout layout instead of supporting an environment override and standard interpreter fallback chain (`PYTHON_BIN -> .venv/bin/python -> python3 -> python`), and defect closeout lacked an explicit rule requiring `spanskikh/docs/DEFECTS_AND_CAPA.md` synchronization before commit/tag.
- **Fix:** Updated `sandbox-init/scripts/run_integration.sh` to resolve `PYTHON_BIN` via `PYTHON_BIN -> .venv/bin/python -> python3 -> python`, updated `test_run_integration_script_dry_run` to pass `PYTHON_BIN=sys.executable` and include `Path(sys.executable).resolve().parent` in `PATH`, and registered `BUG-005` + `CAPA-010..012` in `spanskikh/docs/DEFECTS_AND_CAPA.md` for Patch Release `v0.9.1`.
- **Regression Evidence:** `sandbox-init` `./scripts/run_logged.sh v091_verify` (`53 passed, 3 deselected`) and `PYTHON_BIN=.venv/bin/python3 ./scripts/run_integration.sh --dry-run`.

## CAPA-010: CI Runner Python Interpreter Resolution Fallback & Mandatory Defect Registry Sync (`BUG-005`, GitHub Actions run `45188880471`)
- **Scope:** All shell wrapper scripts (`scripts/*.sh`), CLI subprocess harnesses, and defect closeout workflows across `spanskikh`, `sandbox-init`, `abstract-ops`, `interview-ops`, and `hostel-ops`.
- **Preventive Rule 1 (Interpreter Resolution Fallback):** Shell wrappers invoking Python modules must never hardcode `.venv/bin/python` without fallback. Always resolve the interpreter via the ordered fallback chain `PYTHON_BIN` (if set) -> `${REPO_ROOT}/.venv/bin/python` (if executable) -> `command -v python3` -> `command -v python`, and fail fast with a clear diagnostic on `stderr` if none is available.
- **Preventive Rule 2 (Mandatory SSoT Defect & CAPA Registration):** Every discovered defect (`BUG-XXX`) or process improvement (`CAPA-XXX`) across any cluster repository must be recorded in `spanskikh/docs/DEFECTS_AND_CAPA.md` (both in the `Summary Matrix` and `Detailed Records`) before committing the fix or closing out the release/patch. Mentioning a `BUG-XXX` only in a repository `CHANGELOG.md` without registering it in `spanskikh/docs/DEFECTS_AND_CAPA.md` is a process violation.

## CAPA-011: Synchronize `pyproject.toml` Package Version with Release Tags
- **Triggering Incident (`v0.9.0` / `v0.9.1`):** All four dev repositories (`sandbox-init`, `abstract-ops`, `interview-ops`, `hostel-ops`) shipped `v0.9.0` code and `CHANGELOG.md` entries while `[project].version` in `pyproject.toml` remained at `"0.8.0"`.
- **Root Cause:** `DEVPROCESS.md` Verification & Closure Gate required updating `CHANGELOG.md` and creating annotated Git tag `vX.Y.Z`, but did not explicitly mandate bumping `version = "X.Y.Z"` in `<repo>/pyproject.toml` whenever a repository changes in a release or patch.
- **Preventive Rule:** Whenever a repository receives code, script, dependency, test, or packaging changes in a release or patch tag `vX.Y.Z`, update `[project].version = "X.Y.Z"` in `<repo>/pyproject.toml` so installed package metadata and `CycloneDX` SBOM root component versions match the Git tag `vX.Y.Z` before tagging.

## CAPA-012: Unified Feature Backlog (`FEAT-XXX`) & Backlog-Driven Release Refinement
- **Triggering Need (`v0.9.1` -> `v0.10.0`):** Previously, new capabilities and process enhancements were drafted directly inside `docs/releases/vX.Y.Z-refine.md` as `CR-XXX` items without a persistent upstream intake backlog linking enhancement requests alongside defects (`BUG-XXX`) and preventive actions (`CAPA-XXX`).
- **Preventive Rule:**
  1. **Canonical Cluster Backlog (`spanskikh/docs/DEFECTS_AND_CAPA.md`):** `spanskikh/docs/DEFECTS_AND_CAPA.md` serves as the unified cluster backlog for defects (`BUG-XXX`), process preventive rules (`CAPA-XXX`), and feature requests (`FEAT-XXX`). Every new product or SDLC enhancement request is first added to the `## Feature Backlog (FEAT-XXX)` section below with an ID, target repositories, summary, and target release status.
  2. **Backlog-Driven Release Refinement (`FEAT-XXX -> CR-XXX`):** During the Release Opening Gate, `docs/releases/vX.Y.Z-refine.md` selects candidate `FEAT-XXX` items (together with any open `BUG-XXX` / `CAPA-XXX` engineering actions) from `spanskikh/docs/DEFECTS_AND_CAPA.md` and decomposes them into formal Change Requests (`CR-XXX`) with explicit `FEAT-XXX <-> CR-XXX` traceability links and Definitions of Done.

---

## Feature Backlog (FEAT-XXX)

Canonical intake register for product and agentic-SDLC feature requests across the `spanskikh` cluster (`CAPA-012`). Items selected during release refinement are linked to their assigned `CR-XXX` and release milestone.

| Feature ID | Track / Scope | Target Repos | Feature Summary & Architectural Value | Target Release / Assigned CR | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FEAT-001** | Track A (Agentic SDLC) | `sandbox-init`, `spanskikh` | **Automated Pre-Release Audit CLI & `CAPA-009` Phase-Log Gate:** Build `python -m sandbox_init.release_audit` and `./scripts/run_release_audit.sh` verifying Python string literals `<= 85` chars, zero `/home/<user>/` or secret leaks, `pyproject.toml` version sync (`CAPA-011`), `DEFECTS_AND_CAPA.md` registration (`CAPA-010`), `CycloneDX` SBOM parity (`CAPA-007`), `RELEASES.md` <-> `CHANGELOG.md` sync, and `CAPA-009` `logs/vX.Y.Z-crNNN-{plan,edit}.log` completeness. | `v0.10.0` (`CR-028`) | Refined (`v0.10.0-refine.md`) |
| **FEAT-002** | Track A (Live Oracle Reliability) | `sandbox-init`, all 4 dev repos | **Deterministic `Ollama` CPU Warmup Ping Before `CAPA-006` Live Tests:** Add a preflight keep-alive warmup request for `qwen2.5-coder:7b` and `nomic-embed-text` inside `sandbox_init.topology` / `./scripts/run_integration.sh` so grammar-constrained `@pytest.mark.integration` LLM-as-a-Judge tests never fail on cold GGUF model load into `hippo` RAM. | `v0.10.0` (`CR-028`) | Refined (`v0.10.0-refine.md`) |
| **FEAT-003** | Track B (Multi-Agent Observability) | `sandbox-init` + all 4 dev repos | **Cross-Agent `OpenTelemetry` / `OpenInference` `trace_id` Propagation:** Generate and propagate W3C / `OpenInference`-compatible `trace_id`, `span_id`, and `parent_span_id` metadata across every `FastMCP` `stdio` Supervisor/Worker hop (`sandbox-init -> abstract-ops -> interview-ops -> hostel-ops`) and persist correlation IDs in `OrchestrationReport` and `DuckDB` / `PostgreSQL` audit records. | `v0.10.0` (`CR-029`) | Refined (`v0.10.0-refine.md`) |
| **FEAT-004** | Track B (Adversarial AI Safety) | `abstract-ops`, `interview-ops`, `hostel-ops`, `sandbox-init` | **Automated `PyRIT`-Style Adversarial Red-Teaming Gate:** Ship a structured adversarial corpus and runner testing prompt-injection, boundary-overflow, MFA privilege-escalation (`is_external=True, mfa_verified=False`), free-text skill sneak-in (`CR-003`), and zero-sum ledger split-leg evasion across the 4-hop `FastMCP` `stdio` pipeline with `0` false `SAT` escapes. | `v0.10.0` (`CR-030`) | Refined (`v0.10.0-refine.md`) |
| **FEAT-005** | Track B (Deterministic Replay & Business UAT) | `sandbox-init`, `spanskikh` (`docs/PRODUCT_GUIDE.md`) | **Golden Trace Replay & End-to-End Business UAT Suite:** Provide offline Golden Trace recording/replay verification for deterministic multi-agent `SAT`/`UNSAT` verdicts alongside `tests/test_business_uat.py` (`./scripts/run_business_uat.sh`) validating all 5 executive and operator workflows (`UAT-1..UAT-5`) in `docs/PRODUCT_GUIDE.md`. | `v0.10.0` (`CR-029`, `CR-031`) | Refined (`v0.10.0-refine.md`) |
