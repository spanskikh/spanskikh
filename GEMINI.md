# Workspace Agent Instructions (`~/projects/GEMINI.md`)

Workspace-wide instruction anchor for the `spanskikh` neuro-symbolic verification cluster (`spanskikh`, `sandbox-init`, `abstract-ops`, `interview-ops`, `hostel-ops`).

## 1. Single Source of Truth (SSoT)
- **Canonical Process Standard:** Read and follow `~/projects/spanskikh/DEVPROCESS.md` as the authoritative SSoT before editing any repository.
- **Canonical Governance Registry:**
  - Release roadmap & CR traceability: `~/projects/spanskikh/RELEASES.md`
  - Defect log, preventive rules (`CAPA-001..012`) & feature backlog (`FEAT-XXX`): `~/projects/spanskikh/docs/DEFECTS_AND_CAPA.md`
  - Business product & operator workflows: `~/projects/spanskikh/docs/PRODUCT_GUIDE.md`
  - Retrospectives & refinement backlogs (`FEAT-XXX -> CR-XXX`): `~/projects/spanskikh/docs/releases/`
- **Anti-Duplication (`CAPA-004` / `CAPA-005`):** Never duplicate `DEVPROCESS.md`, `RELEASES.md`, `docs/DEFECTS_AND_CAPA.md`, or `docs/releases/*` inside the 4 dev repos (`sandbox-init`, `abstract-ops`, `interview-ops`, `hostel-ops`).
- **Rule Discovery Compatibility (`CAPA-008`):** `~/projects/GEMINI.md` and `~/projects/AGENTS.md` symlink to `spanskikh/GEMINI.md`. Antigravity CLI (`agy`) auto-loads both `GEMINI.md` and `AGENTS.md` and deduplicates by resolved path; note that directory walk-up stops at a child repository's `.git` boundary, so launch workspace-wide sessions from `~/projects` (`--add-dir ~/projects`) or explicitly read `~/projects/spanskikh/DEVPROCESS.md`.

## 2. Agent Roles, Two-Phase Protocol & Traceability
- **Primary Coding & Verification Agent:** Antigravity CLI (`agy` v1.5.13, FastMCP-native). User-level allow/deny command permissions are enforced in `~/.config/antigravity/settings.json`.
- **Workspace Root Launch (`--add-dir ~/projects`, `CAPA-008`):** Launch `agy` from `~/projects` (or pass `--add-dir ~/projects`) to load `~/projects/GEMINI.md`, access `spanskikh/` SSoT files, and edit target dev repos without workspace-boundary truncation.
- **Two-Phase Plan-Then-Edit Gate (`CAPA-008`):**
  - **Phase 1 (`--mode plan`):** Fast read-only pass inspecting `DEVPROCESS.md`, `docs/releases/vX.Y.Z-refine.md`, and target contracts (`models.py`, `contracts.py`, `server.py`, tests per `CAPA-002`) routed to `logs/vX.Y.Z-crNNN-plan.log`.
  - **Phase 2 (`--mode accept-edits`):** Execute approved edits, persist `docs/dev-log/` artifact, run `./scripts/run_logged.sh` verification gates (`ruff`, `mypy --strict`, `pytest`), update `CHANGELOG.md`, and route output to `logs/vX.Y.Z-crNNN-edit.log`.
- **Prompt & Phase-Log Auditability (`CAPA-009`):** Archive exact Phase 1 and Phase 2 prompt summaries, CLI flags, commit SHAs, and `logs/vX.Y.Z-crNNN-{plan,edit}.log` paths for every CR in `docs/releases/vX.Y.Z-retrospective.md`.
- **Mandatory Defect/CAPA Sync, CI Python Fallback, Version Sync & Backlog Intake (`CAPA-010..012`):** Register every `BUG-XXX`, `CAPA-XXX`, and feature request (`FEAT-XXX`) in `~/projects/spanskikh/docs/DEFECTS_AND_CAPA.md` (pulling `FEAT-XXX` into `docs/releases/vX.Y.Z-refine.md` to form `CR-XXX` items per `CAPA-012`), use `PYTHON_BIN -> .venv/bin/python -> python3 -> python` fallback in shell wrappers (`CAPA-010`), and synchronize `[project].version = "X.Y.Z"` in `<repo>/pyproject.toml` whenever a repo changes in release/patch `vX.Y.Z` (`CAPA-011`).
- **Aider:** Deferred; do not introduce Aider workflows or dependencies.
- **Local `Ollama`:** Restricted strictly to domain/business features and grammar-constrained LLM-as-a-Judge tests (`CAPA-006`: pass `<PydanticModel>.model_json_schema()`, `temperature=0.0`, `timeout >= 180.0s`). Do not use paid cloud APIs in domain code or tests.

## 3. Human-in-the-Loop (HITL) Git Gate (`CAPA-008`)
- **Agent-Allowed Actions:** Edit files, run non-mutating git inspection (`git status`, `git diff`, `git log`, `git rev-parse`), and execute verification gates (`ruff`, `mypy --strict`, `pytest`).
- **Human-Only Actions (STRICTLY FORBIDDEN FOR AGENTS):** Never run `git commit`, `git tag`, `git push`, or `rm -rf` (also blocked in `~/.config/antigravity/settings.json`).
- **Handoff Requirement:** After completing edits and verification, present `git status` and a concise diff summary (`git diff --stat`) so the human reviews `git diff`, executes `git commit` / `git tag` / `git push`, and signs off the release.

## 4. FastMCP `stdio` Conventions (`agy mcp`)
- **Server Management:** Manage MCP registrations with `agy mcp list`, `agy mcp add`, `agy mcp enable`, `agy mcp disable`, and `agy mcp remove` (global config at `~/.gemini/config/mcp_config.json`).
- **CLI Syntax (`stdio` default):** Flags must precede `<name>`; e.g. `agy mcp add <name> <repo>/.venv/bin/python3 -m <pkg>.server`.
- **`stdio` Transport Hygiene:** FastMCP servers using `stdio` must never write logs or banners to `stdout`; route diagnostics strictly to `stderr` or `logs/`.
- **Zero-Guesswork Contract Rule (`CAPA-002`):** Always inspect `models.py` and `server.py` before writing MCP clients or tests. Preserve 12-tool FastMCP namespace disjointness across the 4 dev repos.

## 5. Toolchain, Code Style & Verification Gates
- **Local `.venv/bin/` First:** Run `.venv/bin/ruff`, `.venv/bin/mypy --strict`, and `.venv/bin/pytest` inside each repository.
- **`ruff` E501 String Literal Cap:** Keep Python string literals `<= 85` characters (`ruff format` does not wrap long string literals, causing `E501 > 100`).
- **Strict Typing:** `mypy --strict` must pass with `0` errors across `src` and `tests`.
- **Log Routing (`CAPA-003`):** Route all `ruff`, `mypy`, and `pytest` outputs to `logs/` (via `./scripts/run_logged.sh <task> -- <cmd>` or `logs/<name>.log`) and print at most `15` summary lines to stdout. Never write temporary files to system `/tmp` (use `~/projects/tmp/` for scratchpad helpers).
- **Non-Interactive Shell Hygiene:** Always set `PAGER=cat GIT_PAGER=cat GH_PAGER=cat` in automated commands; never paste `set -e` into multi-line interactive shells.

## 6. Hygiene, Language & SBOM Rules
- **English-Only Git Artifacts (`CAPA-002` / `CAPA-005`):** All Git-tracked code, comments, docstrings, and Markdown files must be strictly in English with zero Cyrillic characters and zero unfinished placeholder markers (forbidden by automated doc audits).
- **Zero Hardcoded Home Paths:** Never write hardcoded `/home/<user>/` or `/Users/<user>/` paths or secrets (`ghp_...`, `sk-...`) in tracked files or generated artifacts; always use `~/` or relative paths.
- **SBOM PEP 610 Sanitization (`CAPA-007`):** Strip local `file://` `externalReferences` from `CycloneDX` SBOM outputs before asserting path hygiene or publishing artifacts.
- **Stateful DDL Safety (`CAPA-001`):** Never rely on `CREATE TABLE IF NOT EXISTS` to evolve constraints or indexes on existing PostgreSQL/DuckDB tables; use idempotent catalog checks (`pg_constraint`, `pg_indexes`) and verify against live `rhino` integration tests.
