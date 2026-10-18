"""Cross-validate our stdlib parsers against LIEF.

`test_parsers_golden.py` proves the parsers recover values we chose. That still
leaves one doubt: what if our fixture encodes the same misunderstanding the
parser holds? LIEF is an independent, widely used implementation, so agreement
on the same bytes is real evidence rather than self-agreement.

LIEF is a development-only dependency (see requirements-dev.txt); without it
these tests skip instead of failing.
"""

from __future__ import annotations

import json
import os
import shutil
import struct
import subprocess
import sys
from pathlib import Path

import pytest

lief = pytest.importorskip("lief", reason="LIEF not installed (dev dependency)")

from . import sample_factory as sf

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def _child_env() -> dict:
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def _scan(script: str, data: bytes, filename: str, out_json: str, tmp_path: Path) -> dict:
    src = tmp_path / filename
    src.write_bytes(data)
    out = tmp_path / "out"
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / script), str(src), "--out", str(out)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=_child_env(),
        timeout=180,
    )
    assert proc.returncode == 0, f"{script} failed:\n{proc.stdout}\n{proc.stderr}"
    return json.loads((out / out_json).read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- PE

def test_pe_sections_match_lief(tmp_path):
    data = sf.build_pe64()
    got = _scan("pe_deep_scan.py", data, "sections.exe", "pe_scan.json", tmp_path)

    src = tmp_path / "sections.exe"
    ref = lief.parse(str(src))
    ours = [s["name"] for s in got["sections"]]
    assert ours == [s.name for s in ref.sections]
    assert int(ref.header.machine) == 0x8664
    assert got["pe_header"]["num_sections"] == ref.header.numberof_sections


def test_pe_imports_match_lief(tmp_path):
    data = sf.build_pe64(with_imports=True)
    got = _scan("pe_deep_scan.py", data, "imports.exe", "pe_scan.json", tmp_path)

    ref = lief.parse(str(tmp_path / "imports.exe"))
    ours = {(i["dll"], i["name"]) for i in got["imports"]}
    theirs = {
        (lib.name, entry.name)
        for lib in ref.imports
        for entry in lib.entries
        if entry.name
    }
    assert ours == theirs
    assert ours, "import table must not be empty (regression: wrong directory offset)"


def test_real_system_pe_matches_lief():
    """A real Windows binary: sections, imports and mitigation bits must agree."""
    system_root = os.environ.get("SystemRoot")
    if not system_root:
        pytest.skip("not a Windows host")
    sample = Path(system_root) / "System32" / "where.exe"
    if not sample.exists():
        pytest.skip("where.exe not present on this host")

    out = Path(os.environ.get("TEMP", ".")) / "rf_cross_validate"
    shutil.rmtree(out, ignore_errors=True)
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "pe_deep_scan.py"), str(sample), "--out", str(out)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=_child_env(),
        timeout=180,
    )
    assert proc.returncode == 0, proc.stderr
    got = json.loads((out / "pe_scan.json").read_text(encoding="utf-8"))

    ref = lief.parse(str(sample))
    assert got["pe_header"]["num_sections"] == ref.header.numberof_sections
    assert [s["name"] for s in got["sections"]] == [s.name for s in ref.sections]

    ours_dlls = {i["dll"] for i in got["imports"]}
    theirs_dlls = {lib.name for lib in ref.imports}
    assert ours_dlls == theirs_dlls
    assert len(ours_dlls) > 1, "a real system binary imports several DLLs"

    # LIEF 1.0 no longer exposes dll_characteristics as an int; read the field
    # straight from the optional header instead (offset 70 in both PE flavours).
    raw = sample.read_bytes()
    opt = struct.unpack_from("<I", raw, 0x3C)[0] + 24
    assert struct.unpack_from("<H", raw, opt)[0] in (0x10B, 0x20B)
    dll_chars = struct.unpack_from("<H", raw, opt + 70)[0]
    assert got["mitigations"]["aslr"] is bool(dll_chars & 0x40)
    assert got["mitigations"]["dep"] is bool(dll_chars & 0x100)
    assert got["mitigations"]["cfg"] is bool(dll_chars & 0x4000)


# -------------------------------------------------------------------------- ELF

def test_elf_header_and_sections_match_lief(tmp_path):
    data = sf.build_elf64()
    got = _scan("elf_deep_scan.py", data, "sample.elf", "elf_scan.json", tmp_path)

    ref = lief.parse(str(tmp_path / "sample.elf"))
    assert int(ref.header.machine_type) == 0x3E
    assert got["header"]["machine"] == "x86-64"
    assert got["header"]["entry"] == ref.header.entrypoint == sf.ELF_ENTRY
    assert "EXEC" in str(ref.header.file_type)
    assert got["header"]["type"] == "EXEC"
    ours = [s["name"] for s in got["section_headers"]]
    assert ours == [s.name for s in ref.sections]


# ----------------------------------------------------------------------- Mach-O

def test_macho_header_matches_lief(tmp_path):
    data = sf.build_macho64()
    got = _scan("macho_scan.py", data, "sample.macho", "macho_scan.json", tmp_path)

    ref = lief.parse(str(tmp_path / "sample.macho"))
    assert int(ref.header.cpu_type) == 0x01000007
    assert got["header"]["cputype"] == "x86-64"
    assert str(ref.header.file_type).endswith("EXECUTE")
    assert got["header"]["filetype"] == "EXECUTE"
    assert got["header"]["ncmds"] == ref.header.nb_cmds
