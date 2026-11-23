# Engineering & Release Governance (`DEVPROCESS.md`)

1. **English-Only Public Surface:** All tracked Markdown documentation, Python code, docstrings, comments, and Git commit messages must be strictly in English (`LANGUAGE_DRIFT_CYRILLIC` enforced by automated tests).
2. **Private-First Verification Gate:** New repositories and major releases are created as `PRIVATE` without active `.github/workflows/*.yml` until all local static, hygiene, and link checks pass (`docs/ci/ci.yml` promoted only at public release).
3. **Neuro-Symbolic Verification Principle:** Probabilistic LLM outputs are treated as untrusted hypotheses gated by deterministic `Pydantic v2` schemas, `Z3` SMT formal proofs (`SAT` / `UNSAT`), and database/protocol invariants.
4. **Zero-Leak Hygiene:** Tracked files must never contain credentials, API tokens, real PII, local `/home/<user>/` paths, or runtime `.duckdb`/`.log`/`.env` artifacts.
5. **Traceable Change Requests (`CR-XXX`):** Every architectural or documentation change maps to formal `CR-XXX` records in `RELEASES.md`, `CHANGELOG.md`, and `docs/dev-log/`.
