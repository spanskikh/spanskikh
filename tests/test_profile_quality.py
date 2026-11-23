from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLUSTER_REPOS = ("sandbox-init", "abstract-ops", "interview-ops", "hostel-ops")

FORBIDDEN_PATTERNS = (
    re.compile(r"[\u0410-\u042f\u0430-\u044f\u0401\u0451]"),
    re.compile(r"\bTODO\b"),
    re.compile(r"\bTBD\b"),
    re.compile(r"\bFIXME\b"),
    re.compile(r"/home/[a-zA-Z0-9._-]+/"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
)


def test_tracked_markdown_and_code_hygiene() -> None:
    files = [
        ROOT / "README.md",
        ROOT / "DEVPROCESS.md",
        ROOT / "RELEASES.md",
        ROOT / "docs/DEFECTS_AND_CAPA.md",
        ROOT / "pyproject.toml",
        ROOT / "docs/ci/ci.yml",
        ROOT / "tests/test_profile_quality.py",
        *sorted((ROOT / "docs/releases").glob("*.md")),
    ]
    assert len(files) >= 13
    for path in files:
        assert path.is_file(), f"Missing required file: {path}"
        content = path.read_text(encoding="utf-8")
        for pat in FORBIDDEN_PATTERNS:
            assert not pat.search(content), f"Forbidden {pat.pattern} in {path.name}"


def test_canonical_cluster_governance_invariants() -> None:
    devp = (ROOT / "DEVPROCESS.md").read_text(encoding="utf-8")
    for tok in ("PTY Paste", "1.5 KiB", "logs/"):
        assert tok in devp, f"DEVPROCESS.md missing CAPA-003 token: {tok}"

    capa = (ROOT / "docs/DEFECTS_AND_CAPA.md").read_text(encoding="utf-8")
    for tok in ("BUG-001", "CAPA-001", "CAPA-002", "CAPA-003", "CAPA-004"):
        assert tok in capa, f"DEFECTS_AND_CAPA.md missing {tok}"

    retro = (ROOT / "docs/releases/v0.7.0-retrospective.md").read_text(encoding="utf-8")
    for sec in (
        "## Lessons Learned",
        "## Rejected Ideas",
        "## Unlucky Probe-Runs",
        "## Release Chat Digest",
    ):
        assert sec in retro

    refine = (ROOT / "docs/releases/v0.8.0-refine.md").read_text(encoding="utf-8")
    assert "## Next-Session Bootstrap Prompt" in refine


def test_readme_cluster_links_and_mermaid() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert readme.count("```mermaid") == 1
    assert readme.count("```") % 2 == 0
    assert "flowchart TB" in readme
    for repo in CLUSTER_REPOS:
        assert f"https://github.com/spanskikh/{repo}" in readme
        assert (
            f"https://github.com/spanskikh/{repo}/blob/main/docs/ENGINEERING_PROFILE.md" in readme
        )
        assert f"https://github.com/spanskikh/{repo}/blob/main/docs/ARCHITECTURE.md" in readme
