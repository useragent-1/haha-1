"""Contract tests for the optional Rea CLI.

Rea is an optional backend, so these tests skip when it is not installed. When
it is present they pin the parts `references/rea-backend.md` depends on: the
version line shape and the provider identifiers. If upstream renames a
provider, the routing table in the docs must be updated in the same change.
"""

from __future__ import annotations

import re
import shutil
import subprocess

import pytest

REA = shutil.which("rea")

pytestmark = pytest.mark.skipif(REA is None, reason="rea CLI not installed (optional backend)")

DOCUMENTED_PROVIDERS = ("ghidra", "hopper", "ida")


def _run(*args: str) -> tuple[int, str]:
    proc = subprocess.run(
        [REA, *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
    )
    return proc.returncode, f"{proc.stdout}\n{proc.stderr}"


def test_version_reports_semver():
    code, out = _run("--version")
    assert code == 0, out[:400]
    assert re.search(r"\d+\.\d+\.\d+", out), out[:400]


def test_capabilities_expose_provider_candidates():
    code, out = _run("capabilities")
    assert code == 0, out[:400]
    assert "analysis_provider_candidates" in out, "capabilities output shape changed"
    lowered = out.lower()
    for provider in DOCUMENTED_PROVIDERS:
        assert provider in lowered, (
            f"documented provider '{provider}' missing from `rea capabilities`; "
            "update references/rea-backend.md"
        )


def test_capabilities_report_open_state():
    code, out = _run("capabilities")
    assert code == 0, out[:400]
    assert re.search(r"^open:\s*(true|false)", out, re.MULTILINE), (
        "capabilities no longer reports the open/bound state; the probe procedure in "
        "references/rea-backend.md relies on it"
    )
