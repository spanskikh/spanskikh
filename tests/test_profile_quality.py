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
        ROOT / "pyproject.toml",
        ROOT / "docs/ci/ci.yml",
        ROOT / "tests/test_profile_quality.py",
    ]
    for path in files:
        assert path.is_file(), f"Missing required file: {path}"
        content = path.read_text(encoding="utf-8")
        for pat in FORBIDDEN_PATTERNS:
            assert not pat.search(content), f"Forbidden {pat.pattern} in {path.name}"


def test_private_first_staged_ci_invariant() -> None:
    staged = ROOT / "docs/ci/ci.yml"
    assert staged.is_file(), "Staged CI workflow docs/ci/ci.yml must exist"
    content = staged.read_text(encoding="utf-8")
    assert "pytest -v" in content
    assert "mypy --strict" in content


def test_readme_cluster_links_and_mermaid() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert readme.count("```mermaid") == 1
    assert readme.count("```") % 2 == 0
    assert "flowchart TB" in readme

    for repo in CLUSTER_REPOS:
        repo_url = f"https://github.com/spanskikh/{repo}"
        profile_url = (
            f"https://github.com/spanskikh/{repo}/blob/main/docs/ENGINEERING_PROFILE.md"
        )
        arch_url = f"https://github.com/spanskikh/{repo}/blob/main/docs/ARCHITECTURE.md"
        badge_url = (
            f"https://github.com/spanskikh/{repo}/actions/workflows/ci.yml/badge.svg"
        )
        assert repo_url in readme, f"Missing repo link: {repo_url}"
        assert profile_url in readme, f"Missing profile dossier link: {profile_url}"
        assert arch_url in readme, f"Missing architecture link: {arch_url}"
        assert badge_url in readme, f"Missing CI badge link: {badge_url}"
