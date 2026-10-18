"""Detection-quality tests for the one-click pipeline.

`scan_anti_analysis` used plain substring matching, so ordinary MSVC section
names ("`.idata$2`" contains "ida") made every PE look like it employed
anti-analysis tricks and pushed the risk rating to MEDIUM. These tests lock
the word-boundary behaviour in both directions: no false positives on section
names, no false negatives on real indicators.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def _load():
    spec = importlib.util.spec_from_file_location("auto_analyze", SCRIPTS / "auto_analyze.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pe_section_names_are_not_anti_analysis_indicators():
    mod = _load()
    assert mod.scan_anti_analysis([".idata$2", ".idata$5", ".idata$6", ".rdata", ".text"]) == []


def test_real_indicators_still_detected():
    mod = _load()
    found = mod.scan_anti_analysis(["IsDebuggerPresent", "SxIn.dll", "ida", "vmware"])
    assert set(found) == {"IsDebuggerPresent", "SxIn.dll", "ida", "vmware"}


def test_detection_is_case_insensitive():
    mod = _load()
    assert mod.scan_anti_analysis(["isdebuggerpresent"]) == ["isdebuggerpresent"]


def test_timing_apis_are_reported_separately():
    """GetTickCount/QueryPerformanceCounter are ubiquitous; they are a hint, not a risk."""
    mod = _load()
    assert mod.scan_anti_analysis(["GetTickCount", "QueryPerformanceCounter"]) == []
    assert mod.scan_timing_api(["GetTickCount", "QueryPerformanceCounter", "ntdll"]) == [
        "GetTickCount",
        "QueryPerformanceCounter",
    ]


def test_results_are_sorted_and_unique():
    mod = _load()
    found = mod.scan_anti_analysis(["vmware", "IsDebuggerPresent", "vmware"])
    assert found == sorted(set(found))


def _shellcode_tools():
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    import shellcode_tools  # noqa: PLC0415 - path must be set first

    return shellcode_tools


def _stack_string_findings(data: bytes):
    tools = _shellcode_tools()
    return [f for f in tools.find_obfuscated_strings(data) if f.get("type") == "stack_string"]


def test_stack_string_heuristic_ignores_ordinary_code():
    """0xC6 (MOV r/m8,imm8) appears ~150 times in a 96 KB system binary."""
    ordinary = b"\x90" * 199_700 + b"\xc6" * 300
    assert _stack_string_findings(ordinary) == []


def test_stack_string_heuristic_fires_on_dense_construction():
    dense = b"\xc6\x11" * 3000 + b"\x90" * 40_000
    findings = _stack_string_findings(dense)
    assert findings, "dense MOV-byte construction should be reported"
    assert findings[0]["confidence"] == "low"
