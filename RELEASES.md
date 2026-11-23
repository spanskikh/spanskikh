# Product Releases & Business Value Traceability (`RELEASES.md`)

Official release roadmap and business-value traceability matrix across the local neuro-symbolic verification cluster (`sandbox-init`, `abstract-ops`, `interview-ops`, `hostel-ops`).

---

## Release `v0.8.0` (Released — 2026-11-23)
- **Business Goal:** Enforce cross-cluster Z3 RAM allocation invariants (`hippo` 24 GiB / `rhino` 16 GiB), 12-tool FastMCP namespace disjointness, deterministic `CycloneDX` SBOM reproducibility, and live end-to-end `Ollama` + `rhino` PostgreSQL sign-off (`139/139` tests green).
- **Retrospective:** [`docs/releases/v0.8.0-retrospective.md`](docs/releases/v0.8.0-retrospective.md) | **Refinement Record:** [`docs/releases/v0.9.0-refine.md`](docs/releases/v0.9.0-refine.md)

| CR # & Short Name | Repository | Short Task Description | Contribution to Release Business Goal | Architecture Learning Value | Formal Invariant / DoD |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CR-022: Cross-Cluster Z3 Resource Contract & `CycloneDX` SBOM Gate** | All 4 dev repos | Add `tests/test_sbom_and_contracts.py` proving joint `hippo`/`rhino` Z3 RAM budget (`SAT`/`UNSAT`), 12-tool FastMCP namespace disjointness, and two-run `CycloneDX` SBOM determinism + path hygiene in CI. | Prevents cross-service memory contention, MCP tool name collisions, and non-reproducible or path-leaking SBOM artifacts. | Cluster-level SMT composition over multi-node resource contracts and deterministic supply-chain provenance. | `test_sbom_and_contracts.py` and `.github/workflows/ci.yml` SBOM gate green across all 4 repos. |
| **CR-023: Live Integration & Grammar-Constrained Rubric Sign-Off (`BUG-003` / `CAPA-006`)** | All 5 repos | Upgrade `_judge_doc_with_ollama` to `DocRubricScore.model_json_schema()` grammar decoding (`temperature=0.0`, `timeout=180.0`) and execute full `@pytest.mark.integration` sign-off against `hippo` Ollama and `rhino` PostgreSQL. | Eliminates stochastic schema drift in LLM-as-a-Judge evaluation and verifies live two-node execution end-to-end. | Grammar-constrained decoding (`llama.cpp` JSON Schema) enforcing Pydantic invariants at token sampling time. | `131` offline + `8` live integration tests (`139/139`) green; `v0.8.0` tagged across all 5 repos. |

---

## Release `v0.7.0` (Released — 2026-11-23)
- **Business Goal:** Standardize engineering competence, stack, process, and QA metrics documentation (`docs/ENGINEERING_PROFILE.md`) across all four cluster repositories and establish a unified root GitHub profile showcase (`spanskikh/spanskikh`) with live CI badges and architecture topology.
- **Refinement Record:** [`docs/releases/v0.7.0-refine.md`](docs/releases/v0.7.0-refine.md)

| CR # & Short Name | Repository | Short Task Description | Contribution to Release Business Goal | Architecture Learning Value | Formal Invariant / DoD |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CR-017: Standardized 5-Section Engineering Profile Dossier** | All 4 repositories | Author `docs/ENGINEERING_PROFILE.md` with 5 mandatory competence/QA sections, link from `README.md`, and enforce via `tests/test_docs_quality.py`. | Provides technical interviewers and architects a uniform, auditable specification of theories, libraries, environment, processes, and empirical QA metrics per repository. | Standardized architectural dossier modeling and automated section/link invariant enforcement. | `docs/ENGINEERING_PROFILE.md` present with all 5 mandatory headings; `test_docs_quality.py` and `test_release_hygiene.py` green across all 4 repos. |
| **CR-018: Root GitHub Profile Showcase (`spanskikh/spanskikh`)** | `spanskikh/spanskikh` + cluster `v0.7.0` tags | Create root profile repository (`PRIVATE` -> `PUBLIC`) with cluster Mermaid topology, cross-repo comparison matrix linking to `docs/ENGINEERING_PROFILE.md`, and live CI badges. | Unifies the 4-repository neuro-symbolic portfolio behind a single executive entry point with verified links and CI status. | Multi-repository portfolio architecture, automated cross-repo link verification, and private-first public promotion. | `spanskikh/spanskikh` `PUBLIC` with green CI; `v0.7.0` annotated tags pushed across cluster. |
| **CR-019: PTY Paste Cap & `DEVPROCESS.md` Governance (`CAPA-003`)** | All 5 repos | Codify `CAPA-003` in `docs/DEFECTS_AND_CAPA.md`, add `<= 1.5 KiB` / `<= 35 lines` PTY paste & `logs/` caps to `DEVPROCESS.md`, and enforce in `test_docs_quality.py`. | Eliminates interactive terminal paste truncation and stdout log flooding. | Closed-loop CAPA process governance backed by automated tests. | `CAPA-003` logged; `DEVPROCESS.md` updated across all 5 repos; tests green. |
| **CR-020: Consolidate Cluster Governance Docs into `spanskikh/spanskikh` (`CAPA-004`)** | All 5 repos | Move `DEVPROCESS.md`, `RELEASES.md`, `docs/DEFECTS_AND_CAPA.md`, and `docs/releases/*` to `spanskikh/spanskikh`; remove copies from dev repos and enforce `CLUSTER_DOC_DUPLICATE`. | Eliminates multi-repo governance doc duplication and whitespace drift. | Single Source of Truth architecture with automated anti-duplication gates. | Canonical docs live in `spanskikh/spanskikh`; dev repos link to hub; CI green. |
| **CR-021: Fix `BUG-002` Full-Tree Markdown Scan & `CLUSTER_DOC_DUPLICATE` Gate (`CAPA-005`)** | All 5 repos | Log `BUG-002` & `CAPA-005`, scan all `*.md` recursively in `test_docs_quality.py`, and add `cyrillic_in_subdoc` & `cluster_doc_duplicate` counterexamples. | Closes blind spot where sub-documents bypassed English-only and SSoT invariants. | Meta-testing (`Who tests the tests?`): regression counterexamples prove the doc auditor catches sub-doc drift. | `BUG-002` fixed; `cyrillic_in_subdoc` & `cluster_doc_duplicate` pass; CI green. |

---

## Release `v0.6.0` (Released — 2026-11-22)
- **Business Goal:** Prepare and promote all four neuro-symbolic cluster repositories (`sandbox-init`, `abstract-ops`, `interview-ops`, `hostel-ops`) to public portfolio status on GitHub with zero secret/PII leakage, verified `CycloneDX` SBOM generation, up-to-date showcase metrics, and green GitHub Actions CI pipelines.
- **Refinement Record:** [`docs/releases/v0.6.0-refine.md`](docs/releases/v0.6.0-refine.md)

| CR # & Short Name | Repository | Short Task Description | Contribution to Release Business Goal | Architecture Learning Value | Formal Invariant / DoD |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CR-014: Pre-Public Secret, PII & Hygiene Audit Gate** | All 4 repositories | Automated repository hygiene and secret/PII scanner (`tests/test_release_hygiene.py`) + staged CI / `publish_to_github.sh` verification. | Eliminates risk of leaking PII, real credentials, or local host paths when flipping repositories to public. | Automated release-readiness gating, secret/PII hygiene checks, and supply-chain hardening. | `tests/test_release_hygiene.py` green across all tracked files; `docs/ci/ci.yml` validated. |
| **CR-015: Public Portfolio Landing & Metrics Synchronization** | All 4 repositories | Update `README.md` and `docs/ARCHITECTURE.md` with verified `v0.5.0` metrics, diagrams, and quickstart commands. | Ensures reviewers immediately see empirical QA proofs (`Recall@3`, `MRR`, `0` false `SAT`, MCP `stdio`) on every landing page. | Aligns Level-1 (`README.md`) and Level-2 (`docs/ARCHITECTURE.md`) technical documentation with telemetry. | `test_docs_quality.py` (offline + live `Ollama` rubric `>= 4/5`) green across all 4 repositories. |
| **CR-016: Public GitHub Promotion & CycloneDX SBOM CI Activation** | All 4 repositories | Promote `docs/ci/ci.yml -> .github/workflows/ci.yml` via `scripts/publish_to_github.sh`, switch to `public`, and verify green CI + SBOM artifact. | Completes public release delivery with live CI verification and `CycloneDX` SBOM transparency. | Operationalizes private-to-public promotion workflows and automated `CycloneDX` SBOM generation. | All 4 repos `public` on GitHub; GitHub Actions green with `cyclonedx-sbom` artifact uploaded. |

---

## Release `v0.5.0` (Released — 2026-11-22)
- **Business Goal:** Prove end-to-end protocol reliability, retrieval precision, and adversarial resilience of the neuro-symbolic agentic cluster under automated, reproducible QA harnesses—demonstrating production-grade AI Quality Assurance readiness without cloud dependencies.
- **Refinement Record:** [`docs/releases/v0.5.0-refine.md`](docs/releases/v0.5.0-refine.md)

| CR # & Short Name | Repository | Short Task Description | Contribution to Release Business Goal | Architecture Learning Value | Formal Invariant / DoD |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CR-010: FastMCP `stdio` Contract & Z3 Rejection Harness** | `sandbox-init`, `abstract-ops`, `interview-ops`, `hostel-ops` | Automated JSON-RPC / `stdio` contract tests invoking all exposed `FastMCP` tools via official MCP client sessions (`SAT` happy-path + `UNSAT` rejection). | Guarantees agent-facing MCP tool boundaries never leak malformed payloads or bypass Z3 invariant gates. | Protocol-level testing of Model Context Protocol (`FastMCP`) servers and error-contract verification. | Verified: `tests/test_mcp_contracts.py` green across 100% of MCP tools (`SAT` + `UNSAT` + Pydantic validation rejection). |
| **CR-011: Hybrid RRF Benchmark & Recall@K / MRR Gate** | `interview-ops` (+ `sandbox-init` DuckDB telemetry) | Golden Dataset (16 queries against 12 SSOT records) measuring `Recall@3`, `MRR`, and p95 latency across `pgvector`, `tsvector`, and `RRF (k=60)`, logged to `DuckDB`. | Quantifies anti-hallucination retrieval quality with objective IR metrics before LLM synthesis. | Information Retrieval evaluation (`Recall@K`, `MRR`) and hybrid search trade-offs over SSH-tunneled `PostgreSQL + pgvector`. | Verified: `Recall@3 = 0.9375` (`>= 0.90`), `MRR = 1.0000` (`>= 0.85`), p95 `72.22 ms` (`< 150 ms`) on live `hippo <-> rhino`; persisted to `DuckDB`. |
| **CR-012: Adversarial Policy Fuzzing & CEGIS Convergence Gate** | `abstract-ops` | Property-based and adversarial spec generator (`Hypothesis` + 60 synthetic edge cases) benchmarking CEGIS repair convergence. | Proves the formal policy auditor catches 100% of subtle security/logic flaws within bounded CPU budgets. | Neuro-symbolic CEGIS convergence guarantees and adversarial robustness testing (`ISO/IEC 24029`). | Verified: `0` false `SAT` across `60` adversarial + `120` Hypothesis specs; CEGIS converges in `2` iterations (`<= 3`). |
| **CR-013: Normative Dev Process & CAPA-002 Standard** | All 4 repositories | Codify `DEVPROCESS.md` (zero-orphan CR traceability, Scrum gates, English-only Git policy, `.venv/bin/` & shell rules) linked to `CAPA-002`. | Prevents cross-session context drift and unverified schema guesswork across multi-repo AI development. | Establishes repeatable SDLC governance and human-AI collaboration protocols for senior QA/Architect review. | Verified: `DEVPROCESS.md` + `CAPA-002` published; `test_docs_quality.py` (`LANGUAGE_DRIFT_CYRILLIC`) green across all 4 repos. |

---

## Release `v0.4.0` (Released — 2026-11-22)
- **Business Goal:** Establish forensic engineering auditability, reproducible execution logging, and structured post-release retrospectives so every verification claim is backed by timestamped artifacts.
- **Retrospective:** [`docs/releases/v0.4.0-retrospective.md`](docs/releases/v0.4.0-retrospective.md)

| CR # & Short Name | Repository | Short Task Description | Contribution to Release Business Goal | Architecture Learning Value | Formal Invariant / DoD |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CR-009: Dev-Process Auditability & Release Retrospectives** | All 4 repositories | POSIX `scripts/run_logged.sh` wrapper (`.stdout`, `.stderr`, `.log` + ISO-8601 timestamps), `docs/dev-log/` artifacts, and release retrospective gate. | Eliminates unlogged test runs and preserves full engineering decision history for technical due diligence. | Reproducible test harness instrumentation and automated documentation-as-code governance. | `test_run_logged.py` + 8th mutation counterexample (`missing_retrospective_section`) green. |

---

## Release `v0.3.0` (Released — 2026-11-22)
- **Business Goal:** Eliminate stateful database race conditions, schema drift defects, and documentation quality gaps across all cluster repositories.
- **Retrospective:** [`docs/releases/v0.3.0-retrospective.md`](docs/releases/v0.3.0-retrospective.md)

| CR # & Short Name | Repository | Short Task Description | Contribution to Release Business Goal | Architecture Learning Value | Formal Invariant / DoD |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CR-005 & CR-006: Live Cluster Smoke & `CHANGELOG` Traceability** | All 4 repositories | Live `hippo <-> rhino` integration smoke tests and structured `CHANGELOG.md` with CR-to-risk traceability. | Proves real cross-node operational readiness and transparent change management. | Live infrastructure verification (`SSH` tunnel, `Ollama`, `DuckDB`, `PostgreSQL`). | `@pytest.mark.integration` smoke tests green; `CHANGELOG.md` validated. |
| **CR-007 & BUG-001 / CAPA-001: Concurrent Booking Race & Idempotent DDL** | `hostel-ops`, `sandbox-init` | Barrier-synchronized `asyncio` concurrency race test (`btree_gist`), idempotent `pg_constraint` migration, and CAPA defect registry. | Prevents double-booking TOCTOU races and silent DDL drift on stateful databases. | Storage-engine `EXCLUDE USING gist` invariants and formal CAPA root-cause closure. | `23P01` `ExclusionViolation` verified live on `rhino`; `DEFECTS_AND_CAPA.md` published. |
| **CR-008: Architecture Docs & Mutation-Tested Quality Gate** | All 4 repositories | Level-2 `docs/ARCHITECTURE.md` across all repos + `tests/test_docs_quality.py` with 7 seeded mutation counterexamples and live Ollama rubric. | Ensures interview-ready architectural clarity with zero broken links, placeholders, or hollow claims. | Mutation testing of test oracles and hybrid deterministic + LLM-as-a-Judge doc auditing. | 100% of seeded defects rejected; live Ollama rubric `>= 4/5`. |

---

## Release `v0.2.0` (Released — 2026-11-22)
- **Business Goal:** Harden symbolic invariants against subtle semantic bypasses (free-text skill sneak-in, shadowed rules, dirty-room transitions) and add live RAM telemetry.

| CR # & Short Name | Repository | Short Task Description | Contribution to Release Business Goal | Architecture Learning Value | Formal Invariant / DoD |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CR-001: Node RAM Telemetry Collector** | `sandbox-init` | `/proc/meminfo` headroom telemetry collector persisted to `DuckDB` with `Hypothesis` property tests. | Prevents OOM crashes during local CPU LLM inference on `hippo` (`24 GiB` RAM). | Deterministic resource telemetry and property-based invariant verification. | `test_telemetry.py` green; headroom `>= 4 GiB` verified. |
| **CR-002: Rule Subsumption & Shadowing Detector** | `abstract-ops` | Z3 formal proof (`UNSAT(e2 and not e1)`) detecting shadowed/redundant policy rules. | Eliminates dead or masked compliance rules in underwriting and RBAC policies. | Symbolic subsumption checking in SMT solvers over continuous numeric bounds. | `test_detects_shadowed_redundant_rule` green. |
| **CR-003: Free-Text Bullet Entity & Year Guard** | `interview-ops` | Deterministic lexical extractor scanning `bullet_text` for unverified skills and years inside Z3 gate. | Blocks "skill sneak-in" hallucinations in generated CV bullets. | Neuro-symbolic lexical grounding bridging unstructured text and SMT constraints. | `test_bullet_entity_guard.py` green. |
| **CR-004: Anti-Overbooking & Housekeeping State Machine** | `hostel-ops` | Z3 + `btree_gist` disjoint stay intervals and `CLEAN -> DIRTY -> CLEAN` housekeeping transitions. | Guarantees zero overbooking and prevents check-ins into uncleaned rooms. | Formal state-machine invariants coupled with relational range exclusion constraints. | `test_db_gist_and_housekeeping.py` green. |

---

## Release `v0.1.0` (Released — 2026-11-22)
- **Business Goal:** Establish a zero-cloud-cost, two-node neuro-symbolic verification baseline (`hippo` + `rhino`) with Z3 SMT solvers, Pydantic v2 contracts, and FastMCP `stdio` interfaces.

| CR # & Short Name | Repository | Short Task Description | Contribution to Release Business Goal | Architecture Learning Value | Formal Invariant / DoD |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CR-000: Cluster & Domain Baseline** | All 4 repositories | Core Z3 verifiers, CEGIS loops, hybrid RRF search, triple-entry ledger, and `FastMCP` `stdio` servers. | Delivers working end-to-end neuro-symbolic prototypes across infrastructure, policy, RAG, and OLTP domains. | Separation of stochastic LLM generation from deterministic SMT proof verification. | `ruff`, `mypy --strict`, and unit `pytest` suites green across all 4 repos. |
