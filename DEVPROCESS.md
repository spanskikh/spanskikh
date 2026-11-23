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
- **Local Toolchain & Workspace Scratchpad:** Always use `.venv/bin/ruff`, `.venv/bin/mypy --strict`, and `.venv/bin/pytest` (never `uv` or paid cloud APIs). Place temporary helper scripts in `~/projects/tmp/` rather than system `/tmp`.
- **Interactive Shell Hygiene:** Never paste `set -e` into multi-line interactive `bash` commands (use `|| break` in loops). Keep `core.pager = "less -FRX"` and `GIT_PAGER=cat and GH_PAGER=cat (`gh config set pager cat`)`.
- **Zero-Guesswork Contract Rule:** Never guess Pydantic field names or `@mcp.tool()` signatures; inspect `models.py` and `server.py` first before writing tests.
- **Compact Exchange Protocol:** Deliver new modules/tests as clean code blocks with `Target: <relative_path>` headers rather than giant shell heredocs, and paste only compact 5–10 line summaries from `logs/*.log` into chat.

- **PTY Paste & Indentation Safety (`<= 35 lines / <= 1.5 KiB`):** Never paste multi-line blocks exceeding 35 lines or 1.5 KiB into an interactive terminal; split payloads into atomic chunks <= 1.5 KiB.
- **Log Routing & Summary Cap (`<= 15 lines`):** Route all linter, `mypy`, and `pytest` outputs into `logs/YYYYMMDD-HHMMSS_<task>.log` and never touch system `/tmp`; print at most 15 tail lines to stdout.

## Non-Interactive CLI Execution (No Pagers in Automation)
- All automated shell loops, verification scripts, and `run_logged.sh` invocations **must** disable interactive terminal pagers (`less`/`more`) by setting `PAGER=cat`, `GIT_PAGER=cat and GH_PAGER=cat (`gh config set pager cat`)`, and `GH_PAGER=""` (or passing explicit `--no-pager` / `--json ... --jq ...` flags) so non-TTY and scripted runs never block or truncate stdout.

## Release Session Isolation & Bootstrap Handoff

- **One Release = One Dedicated Chat Session:** Every major/minor release cycle (`vX.Y.0`) MUST be executed in a fresh, dedicated assistant session to prevent context window drift and stale state leakage across releases.
- **Release Closure Prerequisite:** Before starting a new release session, the previous release MUST be closed with `docs/releases/vX.Y.Z-retrospective.md` and `docs/releases/vX.(Y+1).0-refine.md` committed and verified against offline documentation and release-hygiene gates (`pytest -m "not integration"`).
- **Mandatory Bootstrap Prompt in `vX.Y.Z-refine.md`:** Every `docs/releases/vX.Y.Z-refine.md` file MUST include a self-contained `## Next-Session Bootstrap Prompt` section containing exact repository state, verified baselines, architectural constraints, and first-step execution instructions so a fresh session can resume without guesswork.
- Keep Python string literals `<= 85` characters in patches (`ruff format` does not wrap long string literals, causing `E501 > 100`).
