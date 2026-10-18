"""Documentation consistency tests.

The README once claimed "11 scripts" while 18 existed, listed 3 of 28 docs, and
omitted five top-level directories entirely. Those drifts are invisible to a
reviewer and expensive to rediscover, so this module makes them fail CI:
every repository path named in the top-level documents must exist on disk.

Only existence is asserted -- counts and prose are still allowed to change.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

TOP_LEVEL_DOCS = [
    "README.md",
    "SKILL.md",
    "AGENTS.md",
    "SKILLS.md",
    "BOOTSTRAP.md",
    "docs/INDEX.md",
]

# Paths that are intentionally absent from the repository.
RUNTIME_ONLY_PREFIXES = (
    "tools/scripts/net",      # cloned by tools/setup_full.sh at install time
    "docs/agent-runs",        # historical run archives, subset is committed
    "docs/reports",
    "docs/tooling",
    "scripts/auto_analysis",  # produced by test runs, gitignored
)

# Backticked repository paths, e.g. `scripts/pe_deep_scan.py`.
PATH_RE = re.compile(r"`((?:scripts|references|skills|tools|docs)/[A-Za-z0-9_./-]+)`")
# Paths ending in a glob or placeholder are prose, not assertions.
SKIP_SUFFIX = ("*", "<", ">")


def _referenced_paths() -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for name in TOP_LEVEL_DOCS:
        doc = ROOT / name
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8", errors="replace")
        for raw in PATH_RE.findall(text):
            if any(ch in raw for ch in SKIP_SUFFIX):
                continue
            path = raw.rstrip("/")
            if any(path.startswith(prefix) for prefix in RUNTIME_ONLY_PREFIXES):
                continue
            found.append((name, path))
    return found


def test_top_level_docs_exist():
    missing = [name for name in TOP_LEVEL_DOCS if not (ROOT / name).exists()]
    assert not missing, f"missing top-level documents: {missing}"


def test_referenced_paths_exist():
    missing = sorted({f"{doc} -> {path}" for doc, path in _referenced_paths() if not (ROOT / path).exists()})
    assert not missing, "documented paths do not exist:\n" + "\n".join(missing)


def test_every_script_is_reachable_from_docs():
    """Each tracked script must be mentioned somewhere in the top-level docs."""
    docs_text = "\n".join(
        (ROOT / name).read_text(encoding="utf-8", errors="replace")
        for name in TOP_LEVEL_DOCS
        if (ROOT / name).exists()
    )
    undocumented = []
    for script in sorted((ROOT / "scripts").rglob("*.py")):
        if "__pycache__" in script.parts or script.name == "__init__.py":
            continue
        rel = script.relative_to(ROOT).as_posix()
        if rel not in docs_text:
            undocumented.append(rel)
    assert not undocumented, (
        "scripts missing from README/SKILL.md (add them, or the inventory will drift again):\n"
        + "\n".join(undocumented)
    )


def test_every_reference_is_indexed():
    """Each reference document must be linked from SKILL.md or README.md."""
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    text += (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
    missing = []
    for ref in sorted((ROOT / "references").glob("*.md")):
        if ref.name not in text:
            missing.append(ref.name)
    assert not missing, f"reference documents not indexed in SKILL.md/README.md: {missing}"


def test_every_skill_is_routed():
    """Each skills/<name>/ must be reachable from SKILLS.md or README.md."""
    text = (ROOT / "SKILLS.md").read_text(encoding="utf-8", errors="replace")
    text += (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
    missing = []
    for skill in sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir()):
        if not (skill / "SKILL.md").exists():
            missing.append(f"{skill.name} (no SKILL.md)")
        elif skill.name not in text:
            missing.append(f"{skill.name} (not routed)")
    assert not missing, f"skills not reachable from routing docs: {missing}"


def test_ci_workflow_matches_local_test_command():
    """The CI workflow must run the same test entry point the README documents."""
    workflow = ROOT / ".github" / "workflows" / "tests.yml"
    assert workflow.exists(), "CI workflow missing"
    body = workflow.read_text(encoding="utf-8")
    assert "pytest tests" in body, "CI does not run pytest tests"
    assert "requirements-dev.txt" in body, "CI does not install the dev requirements"


@pytest.mark.parametrize("path", ["requirements.txt", "requirements-dev.txt", "LICENSE"])
def test_release_files_present(path: str):
    assert (ROOT / path).exists(), f"{path} missing"
