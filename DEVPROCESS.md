# Engineering & AI-Assisted Development Process (`DEVPROCESS.md`)

Normative standard governing release lifecycle, traceability, document roles, quality gates, and human-AI collaboration across `spanskikh/spanskikh` (Single Source of Truth) and dev repositories (`sandbox-init`, `abstract-ops`, `interview-ops`, `hostel-ops`).

---

## 1. Traceability & Zero-Orphan Artifact Rule
- **Mandatory Change Request (`CR-XXX`):** No code, test, or process document may enter `main` without an assigned `CR-XXX` registered in `RELEASES.md` and `docs/releases/vX.Y.Z-refine.md`.
- **Defect & CAPA Rule (`BUG-XXX` / `CAPA-XXX`):** Any discovered defect or recurring process failure halts new feature work until root cause, regression test, and cross-repo preventive rule are logged in `docs/DEFECTS_AND_CAPA.md`.
- **Git Tagging & Branching:** Develop on `feat/cr-XXX-<slug>`, merge via `git merge --no-ff --no-edit`, and tag releases with `git -c tag.gpgSign=false tag -a vX.Y.Z -m "Release vX.Y.Z: CR-AAA..CR-BBB"`.

---

## 2. Release Lifecycle & Scrum Gates (`1 Release = 1 Chat Session`)
1. **Opening Gate (`Retro` + `Refine` + `RELEASES.md`):**
   - Author `docs/releases/v{prev}-retrospective.md` with four required sections: `Lessons Learned`, `Rejected Ideas`, `Unlucky Probe-Runs`, and `Release Chat Digest`.
   - Author `docs/releases/vX.Y.Z-refine.md` decomposing planned `CR-XXX` items, architectural learning value, and formal `Definition of Done (DoD)`.
   - Register release **Business Goal** and CR contribution rows in `RELEASES.md`.
2. **Execution Gate (`CR-XXX`):**
   - Persist incremental scripts/patches in `docs/dev-log/YYYYMMDD-HHMMSS_<cr-id>_<slug>.(sh|py|patch)` with an explicit `# Target: <relative_path>` header.
3. **Verification & Closure Gate:**
   - Execute checks via `./scripts/run_logged.sh <task> -- <cmd>` (`.venv/bin/ruff check src tests`, `.venv/bin/mypy src tests --strict`, `.venv/bin/pytest -v -m "not integration"`).
   - Record verified metrics and log artifact paths in `CHANGELOG.md`, tag `vX.Y.Z`, and push `main` + tags.

---

## 3. Language & Document Role Policy
- **Chat vs. Git Language Split:** Interactive chat discussions with AI collaborators may be conducted in Russian or English, but **all Git-tracked files** (code, docstrings, comments, `README.md`, `RELEASES.md`, `CHANGELOG.md`, `DEVPROCESS.md`, `docs/releases/*`, `docs/dev-log/*`) must be written **strictly in English** (enforced by `LANGUAGE_DRIFT_CYRILLIC` in `tests/test_docs_quality.py`).
- **Public Showcase (`README.md`, `RELEASES.md`, `CHANGELOG.md`, `DEVPROCESS.md`, `docs/ARCHITECTURE.md`, `docs/DEFECTS_AND_CAPA.md`):** Enforced by deterministic AST/Markdown checks + 9 seeded mutation counterexamples + local `Ollama` rubric (`>= 4/5`).
- **Forensic Audit (`docs/releases/*`, `docs/dev-log/*`):** Versioned in Git for engineering due diligence.
- **Ephemeral Execution Logs (`logs/YYYYMMDD-HHMMSS_<task>.{stdout,stderr,log}`):** Gitignored (`logs/`); verified by `tests/test_run_logged.py`.

---

## 4. Tooling, Shell Safety & AI-Collaboration Protocol
- **Workspace Instruction Anchor (`CAPA-008`):** `spanskikh/GEMINI.md` (symlinked at `~/projects/GEMINI.md` and `~/projects/AGENTS.md`) serves as the workspace-wide context router pointing back to `spanskikh/DEVPROCESS.md` as Single Source of Truth (SSoT).
- **Primary Coding & Verification Agent (`CR-027`):** Antigravity CLI (`agy` v1.5.13, FastMCP-native) is the primary coding and verification agent across the cluster. User-level command allow/deny permissions are enforced in `~/.config/antigravity/settings.json`.
- **Workspace Root Launch (`--add-dir ~/projects`, `CAPA-008`):** Always launch `agy` from `~/projects` (or pass `--add-dir ~/projects`) so the agent loads `~/projects/GEMINI.md`, accesses SSoT governance files in `spanskikh/`, and edits target dev repositories without workspace-boundary truncation at child `.git` directories.
- **Two-Phase Plan-Then-Edit Gate (`CAPA-008`) & Prompt/Log Archival (`CAPA-009`):** Every code Change Request (`CR-NNN`) must execute in two logged phases with both phase prompts and log paths (`logs/vX.Y.Z-crNNN-{plan,edit}.log`) archived in the release retrospective (`docs/releases/vX.Y.Z-retrospective.md`) and `docs/dev-log/`:
  1. **Phase 1 — Read-Only Plan & Contract Audit (`--mode plan`):** Inspect `DEVPROCESS.md`, `docs/releases/vX.Y.Z-refine.md`, and target contracts (`models.py`, `contracts.py`, `server.py`, existing tests per `CAPA-002`) without mutating files:
     ```bash
     agy chat --mode plan --add-dir ~/projects \
       "Read spanskikh/DEVPROCESS.md, docs/releases/vX.Y.Z-refine.md, and <repo>/{src,tests}. Produce a concise file-by-file plan and verification checklist for CR-NNN without editing files." \
       > logs/vX.Y.Z-crNNN-plan.log 2>&1
     ```
  2. **Phase 2 — Accept-Edits Implementation & Logged Verification (`--mode accept-edits`):** Execute the approved plan, enforce string literals `<= 85` chars, record `docs/dev-log/` artifact, run verification gates via `./scripts/run_logged.sh`, and stop at the HITL Git boundary:
     ```bash
     agy chat --mode accept-edits --add-dir ~/projects \
       "Execute approved CR-NNN plan in <repo> under spanskikh/DEVPROCESS.md: implement modules/tests (strings <= 85 chars), add docs/dev-log/ artifact, run ruff/mypy --strict/pytest via ./scripts/run_logged.sh, update CHANGELOG.md, and print git status + git diff --stat (HITL Gate: do NOT run git commit, git tag, or git push)." \
       > logs/vX.Y.Z-crNNN-edit.log 2>&1
     ```
- **Deferred & Scoped Tools:** `Aider` is deferred. Local `Ollama` is restricted strictly to domain/business features and grammar-constrained LLM-as-a-Judge evaluation (`CAPA-006`: `<PydanticModel>.model_json_schema()`, `temperature=0.0`, `timeout >= 180.0s`).
- **Human-in-the-Loop (HITL) Git Gate (`CAPA-008`):** Agents edit files, run non-mutating git inspection (`git status`, `git diff`, `git log`, `git rev-parse`), and execute verification checks (`ruff`, `mypy --strict`, `pytest` routed to `logs/`). The explicit manual human perimeter covers `git diff` review, `git commit`, `git tag`, `git push`, and final release sign-off (mutating git and destructive shell commands are also denied to agents in `~/.config/antigravity/settings.json`).
- **FastMCP `stdio` Conventions (`agy mcp`):** Register and inspect local `FastMCP` `stdio` servers via `agy mcp add|list|enable|disable|remove` (global config `~/.gemini/config/mcp_config.json`; flags precede `<name>`). `stdio` servers must never pollute `stdout` with non-JSON-RPC logs; route diagnostics to `stderr` or `logs/`.
- **Local Toolchain & Workspace Scratchpad:** Always use `.venv/bin/ruff`, `.venv/bin/mypy --strict`, and `.venv/bin/pytest` inside each repository (never paid cloud APIs). Place temporary helper scripts in `~/projects/tmp/` rather than system `/tmp`.
- **Interactive Shell Hygiene:** Never paste `set -e` into multi-line interactive `bash` commands (use `|| break` in loops). Keep `core.pager = "less -FRX"`, `GIT_PAGER=cat`, and `GH_PAGER=cat` (`gh config set pager cat`).
- **Zero-Guesswork Contract Rule:** Never guess Pydantic field names or `@mcp.tool()` signatures; inspect `models.py` and `server.py` first before writing tests.
- **Compact Exchange Protocol:** Deliver new modules/tests as clean code blocks with `Target: <relative_path>` headers rather than giant shell heredocs, and paste only compact 5–10 line summaries from `logs/*.log` into chat.
- **PTY Paste & Indentation Safety (`<= 35 lines / <= 1.5 KiB`):** Never paste multi-line blocks exceeding 35 lines or 1.5 KiB into an interactive terminal; split payloads into atomic chunks <= 1.5 KiB.
- **Log Routing & Summary Cap (`<= 15 lines`):** Route all linter, `mypy`, and `pytest` outputs into `logs/YYYYMMDD-HHMMSS_<task>.log` and never touch system `/tmp`; print at most 15 tail lines to stdout.
- **SBOM & Path Hygiene (`CAPA-007`):** Strip PEP 610 local `file://` `externalReferences` from `CycloneDX` SBOM outputs before asserting path hygiene or publishing artifacts. Zero hardcoded `/home/<user>/` paths in tracked files or generated artifacts.

---

## 5. Two-Track Agentic Roadmap (Track A & Track B)
- **Track A — Agentic SDLC (How We Build & Verify):**
  - `v0.9.0`: Workspace instruction anchor `~/projects/GEMINI.md` (+ `AGENTS.md` symlink), `agy` v1.5.13 (`FastMCP`-native) as primary agent (`Aider` deferred; `Ollama` restricted to domain/business features), and HITL Git gate enforced via `DEVPROCESS.md` and `~/.config/antigravity/settings.json`.
  - `v0.10.0`: Autonomous pre-release audit checks (Python string literals `<= 85` chars, path hygiene, SBOM drift, `RELEASES.md` sync) and minimal-counterexample drafting for `docs/DEFECTS_AND_CAPA.md`.
  - `v1.0.0`: Frozen, auditable human-supervised agentic SDLC template.
- **Track B — Product Agentic Architecture (What the Cluster Ships):**
  - `v0.9.0` (Last Feature Release): `CR-024` (topology-aware integration runner), `CR-025` (`FastMCP` Supervisor/Worker chain across all 4 dev repos), `CR-026` (shared `CycloneDX` PEP 610 `file://` sanitizer CLI).
  - `v0.10.0` (Harden & Observability): Cross-agent `OpenTelemetry`/`OpenInference` `trace_id`, `PyRIT` adversarial red-teaming gates, and Golden Trace replay.
  - `v1.0.0` (Compliance Pack): Signed Release Evidence Bundle (`EU AI Act` Art. 9/12/14/15, `ISO/IEC 42001`, `ISO/IEC 24029`).
  - `v1.X.X` (Domain Agents): Autonomous background agents inside the 4 domain apps after `v1.0.0` freeze.

---

## Non-Interactive CLI Execution (No Pagers in Automation)
- All automated shell loops, verification scripts, and `run_logged.sh` invocations **must** disable interactive terminal pagers (`less`/`more`) by setting `PAGER=cat`, `GIT_PAGER=cat`, and `GH_PAGER=cat` (`gh config set pager cat`) (or passing explicit `--no-pager` / `--json ... --jq ...` flags) so non-TTY and scripted runs never block or truncate stdout.

## Release Session Isolation & Bootstrap Handoff

- **One Release = One Dedicated Chat Session:** Every major/minor release cycle (`vX.Y.0`) MUST be executed in a fresh, dedicated assistant session to prevent context window drift and stale state leakage across releases.
- **Release Closure Prerequisite:** Before starting a new release session, the previous release MUST be closed with `docs/releases/vX.Y.Z-retrospective.md` and `docs/releases/vX.(Y+1).0-refine.md` committed and verified against offline documentation and release-hygiene gates (`pytest -m "not integration"`).
- **Mandatory Bootstrap Prompt in `vX.Y.Z-refine.md`:** Every `docs/releases/vX.Y.Z-refine.md` file MUST include a self-contained `## Next-Session Bootstrap Prompt` section containing exact repository state, verified baselines, architectural constraints, and first-step execution instructions so a fresh session can resume without guesswork.
- Keep Python string literals `<= 85` characters in patches (`ruff format` does not wrap long string literals, causing `E501 > 100`).
