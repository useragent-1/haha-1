"""Golden tests: parsers must recover ground truth we constructed ourselves.

Each fixture is built byte by byte in `sample_factory`, so the expected values
(machine type, section names, entry point, header sizes, hashes) are known
before the parser runs. This is the difference between "the script exits 0" and
"the script read the file correctly".

Fixtures are generated at runtime; nothing binary is committed.
"""

from __future__ import annotations

import hashlib
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

import pytest

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
    payload = out / out_json
    assert payload.exists(), f"{script} produced no {out_json}: {proc.stdout}"
    return json.loads(payload.read_text(encoding="utf-8"))


# --------------------------------------------------------------- fixture sanity

def test_fixtures_match_the_format_specs():
    """Read the fixtures back with plain struct to prove they are well formed."""
    pe = sf.build_pe64()
    assert pe[:2] == b"MZ"
    e_lfanew = struct.unpack_from("<I", pe, 0x3C)[0]
    assert pe[e_lfanew:e_lfanew + 4] == b"PE\x00\x00"
    machine, nsections = struct.unpack_from("<HH", pe, e_lfanew + 4)
    assert (machine, nsections) == (0x8664, 2)
    opt = e_lfanew + 24
    assert struct.unpack_from("<H", pe, opt)[0] == 0x20B  # PE32+
    assert struct.unpack_from("<I", pe, opt + 16)[0] == sf.PE_ENTRY_RVA

    elf = sf.build_elf64()
    assert elf[:4] == b"\x7fELF"
    assert elf[4] == 2 and elf[5] == 1  # 64-bit, little endian
    assert struct.unpack_from("<H", elf, 16)[0] == 2       # ET_EXEC
    assert struct.unpack_from("<H", elf, 18)[0] == 0x3E    # EM_X86_64
    assert struct.unpack_from("<Q", elf, 24)[0] == sf.ELF_ENTRY

    macho = sf.build_macho64()
    assert struct.unpack_from("<I", macho, 0)[0] == 0xFEEDFACF
    assert struct.unpack_from("<I", macho, 4)[0] == 0x01000007
    assert struct.unpack_from("<I", macho, 12)[0] == 2      # MH_EXECUTE

    dex = sf.build_dex()
    assert dex[:8] == b"dex\n035\x00"
    assert struct.unpack_from("<I", dex, 32)[0] == sf.DEX_HEADER_SIZE
    assert struct.unpack_from("<I", dex, 36)[0] == sf.DEX_HEADER_SIZE


# --------------------------------------------------------------------------- PE

def test_pe_parser_recovers_ground_truth(tmp_path):
    data = sf.build_pe64()
    got = _scan("pe_deep_scan.py", data, "sample.exe", "pe_scan.json", tmp_path)

    assert got["size"] == len(data)
    assert got["hashes"]["sha256"] == hashlib.sha256(data).hexdigest()
    assert got["pe_header"]["machine_id"] == "0x8664"
    assert got["pe_header"]["is_64bit"] is True
    assert got["pe_header"]["num_sections"] == len(sf.PE_SECTIONS)
    assert got["pe_header"]["entry_point_rva"] == "0x1000"
    assert [s["name"] for s in got["sections"]] == list(sf.PE_SECTIONS)
    assert got["sections"][0]["virtual_address"] == "0x1000"
    assert got["sections"][0]["raw_offset"] == 0x200
    assert got["sections"][0]["permissions"] == "R-X"
    assert got["imports"] == [] and got["tls_callbacks"] == []


def test_pe_packer_detection_ignores_standard_sections(tmp_path):
    """`.rdata` used to match the `DAta` packer marker as a substring."""
    got = _scan("pe_deep_scan.py", sf.build_pe64(), "clean.exe", "pe_scan.json", tmp_path)
    flagged = [i for i in got["packer_indicators"] if "Section name" in i]
    assert flagged == [], f"standard sections reported as packer markers: {flagged}"


# -------------------------------------------------------------------------- ELF

def test_elf_parser_recovers_ground_truth(tmp_path):
    data = sf.build_elf64()
    got = _scan("elf_deep_scan.py", data, "sample.elf", "elf_scan.json", tmp_path)

    assert got["size"] == len(data)
    assert got["header"]["class"] == "ELF64"
    assert got["header"]["endian"] == "little"
    assert got["header"]["type"] == "EXEC"
    assert got["header"]["machine"] == "x86-64"
    assert got["header"]["entry"] == sf.ELF_ENTRY
    assert got["header"]["shnum"] == 3
    assert [s["name"] for s in got["section_headers"]] == ["", ".text", ".shstrtab"]
    assert got["program_headers"][0]["type"] == "LOAD"
    assert got["program_headers"][0]["flags"] == "RX"


# ------------------------------------------------------------------------ Mach-O

def test_macho_parser_recovers_ground_truth(tmp_path):
    data = sf.build_macho64()
    got = _scan("macho_scan.py", data, "sample.macho", "macho_scan.json", tmp_path)

    assert got["size"] == len(data)
    assert got["format"] == "Mach-O 64-bit"
    assert got["header"]["cputype"] == "x86-64"
    assert got["header"]["filetype"] == "EXECUTE"
    assert got["header"]["ncmds"] == 1
    assert got["load_commands"][0]["cmd"] == "SEGMENT_64"
    assert got["load_commands"][0]["segname"] == sf.MACHO_SEGNAME
    assert got["load_commands"][0]["vmsize"] == 0x1000
    assert got["dylibs"] == []


# --------------------------------------------------------------------------- DEX

def test_dex_parser_recovers_ground_truth(tmp_path):
    data = sf.build_dex()
    got = _scan("dex_analyze.py", data, "classes.dex", "dex_analyze.json", tmp_path)

    assert got["size"] == len(data)
    assert got["header"]["file_size"] == sf.DEX_HEADER_SIZE
    assert got["header"]["header_size"] == sf.DEX_HEADER_SIZE
    assert got["header"]["endian_constant"] == "0x12345678"
    assert got["is_little_endian"] is True
    # Integrity fields are computed against the fixture bytes themselves.
    assert got["integrity"]["checksum_valid"] is True
    assert got["integrity"]["sha1_valid"] is True
    assert got["strings"]["total"] == 0
    assert got["classes"]["total"] == 0


# ------------------------------------------------------------------- end to end

def test_auto_analyze_reports_the_real_hash_and_type(tmp_path):
    """The one-click pipeline must not invent metadata."""
    data = sf.build_pe64()
    got = _scan("auto_analyze.py", data, "pipeline.exe", "auto_analysis.json", tmp_path)
    blob = json.dumps(got, ensure_ascii=False)

    assert got["sample"]["size"] == len(data)
    assert got["sample"]["hashes"]["sha256"] == hashlib.sha256(data).hexdigest()
    assert got["sample"]["hashes"]["md5"] == hashlib.md5(data).hexdigest()
    assert "PEx64" in blob, "64-bit PE must be identified as such"


@pytest.mark.parametrize("name", ["pe", "elf", "macho", "dex"])
def test_every_fixture_is_deterministic(name: str):
    """Same builder twice -> identical bytes, so golden values cannot drift."""
    builder = sf.ALL_BUILDERS[name]
    assert builder() == builder()
