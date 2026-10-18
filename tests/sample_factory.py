"""Build minimal, spec-valid binary fixtures in memory.

The point is a closed loop: we write the bytes, so we know the ground truth
(machine type, section names, entry point, hashes). Tests then assert that the
parsers recover exactly that truth. If a parser silently changes semantics, the
value stops matching and the test fails -- which is what "smoke tests" never did.

Fixtures are built at test time and never committed: the repository stays text.
"""

from __future__ import annotations

import hashlib
import struct
import zlib

# --------------------------------------------------------------------------- PE

PE_SECTIONS = (".text", ".rdata")
PE_ENTRY_RVA = 0x1000
PE_IMAGE_BASE = 0x140000000
PE_TIMESTAMP = 0x5F3759DF & 0xFFFFFFFF
PE_MACHINE = 0x8664
PE_RDATA_MARKER = b"GOLDEN_RDATA_MARKER\x00"


def build_pe64() -> bytes:
    """PE32+ x86-64, 2 sections, no imports, one marker string in .rdata."""
    e_lfanew = 0x40
    size_optional = 0xF0
    headers_size = 0x200

    dos = bytearray(0x40)
    dos[0:2] = b"MZ"
    struct.pack_into("<I", dos, 0x3C, e_lfanew)

    coff = struct.pack(
        "<4sHHIIIHH",
        b"PE\x00\x00",
        PE_MACHINE,          # machine
        len(PE_SECTIONS),    # number of sections
        PE_TIMESTAMP,        # timestamp
        0,                   # pointer to symbol table
        0,                   # number of symbols
        size_optional,       # size of optional header
        0x0022,              # characteristics: executable | large address aware
    )

    # PE32+ optional header: 112 fixed bytes + 16 data directories * 8
    opt = bytearray()
    opt += struct.pack("<H", 0x20B)          # magic PE32+
    opt += struct.pack("<BB", 14, 0)         # linker version
    opt += struct.pack("<I", 0x200)          # size of code
    opt += struct.pack("<I", 0x200)          # size of initialized data
    opt += struct.pack("<I", 0)              # size of uninitialized data
    opt += struct.pack("<I", PE_ENTRY_RVA)   # entry point RVA
    opt += struct.pack("<I", 0x1000)         # base of code
    opt += struct.pack("<Q", PE_IMAGE_BASE)  # image base
    opt += struct.pack("<I", 0x1000)         # section alignment
    opt += struct.pack("<I", 0x200)          # file alignment
    opt += struct.pack("<HH", 6, 0)          # OS version
    opt += struct.pack("<HH", 0, 0)          # image version
    opt += struct.pack("<HH", 6, 0)          # subsystem version
    opt += struct.pack("<I", 0)              # win32 version value
    opt += struct.pack("<I", 0x3000)         # size of image
    opt += struct.pack("<I", headers_size)   # size of headers
    opt += struct.pack("<I", 0)              # checksum
    opt += struct.pack("<H", 3)              # subsystem: Windows CUI
    opt += struct.pack("<H", 0)              # dll characteristics
    opt += struct.pack("<Q", 0x100000)       # stack reserve
    opt += struct.pack("<Q", 0x1000)         # stack commit
    opt += struct.pack("<Q", 0x100000)       # heap reserve
    opt += struct.pack("<Q", 0x1000)         # heap commit
    opt += struct.pack("<I", 0)              # loader flags
    opt += struct.pack("<I", 16)             # number of RVA and sizes
    opt += b"\x00" * (16 * 8)                # data directories (all zero)
    assert len(opt) == size_optional, len(opt)

    def section(name: str, vsize: int, vaddr: int, raw_size: int, raw_ptr: int, chars: int) -> bytes:
        return struct.pack(
            "<8sIIIIIIHHI",
            name.encode().ljust(8, b"\x00"),
            vsize, vaddr, raw_size, raw_ptr,
            0, 0, 0, 0, chars,
        )

    sections = (
        section(".text", 0x100, 0x1000, 0x200, 0x200, 0x60000020)   # CODE|EXECUTE|READ
        + section(".rdata", 0x100, 0x2000, 0x200, 0x400, 0x40000040)  # INITIALIZED_DATA|READ
    )

    head = bytes(dos) + coff + bytes(opt) + sections
    assert len(head) <= headers_size
    body = bytearray(headers_size)
    body[0:len(head)] = head
    body[0x200:0x400] = b"\x90" * 0x200                     # .text
    body[0x400:0x400 + len(PE_RDATA_MARKER)] = PE_RDATA_MARKER  # .rdata
    return bytes(body)


def pe_expected() -> dict:
    return {
        "sha256": hashlib.sha256(build_pe64()).hexdigest(),
        "machine_id": "0x8664",
        "num_sections": 2,
        "section_names": list(PE_SECTIONS),
        "entry_rva": "0x1000",
        "marker": PE_RDATA_MARKER[:-1].decode(),
    }


# -------------------------------------------------------------------------- ELF

ELF_ENTRY = 0x401000
ELF_MACHINE = 0x3E  # EM_X86_64
ELF_SECTION_NAMES = (".text", ".shstrtab")
ELF_TEXT_MARKER = b"\x90" * 32


def build_elf64() -> bytes:
    """ELF64 little-endian ET_EXEC x86-64: 1 PT_LOAD, 3 section headers."""
    ident = b"\x7fELF" + bytes([2, 1, 1, 0]) + b"\x00" * 8
    shstrtab = b"\x00.text\x00.shstrtab\x00"

    ehdr = ident + struct.pack(
        "<HHIQQQIHHHHHH",
        2,               # e_type ET_EXEC
        ELF_MACHINE,     # e_machine
        1,               # e_version
        ELF_ENTRY,       # e_entry
        0x40,            # e_phoff
        0x100,           # e_shoff
        0,               # e_flags
        0x40,            # e_ehsize
        0x38,            # e_phentsize
        1,               # e_phnum
        0x40,            # e_shentsize
        3,               # e_shnum
        2,               # e_shstrndx
    )
    assert len(ehdr) == 0x40

    phdr = struct.pack(
        "<IIQQQQQQ",
        1,               # PT_LOAD
        5,               # PF_R | PF_X
        0, 0x400000, 0x400000,
        0x240, 0x240,
        0x1000,
    )
    assert len(phdr) == 0x38

    def shdr(name_off, sh_type, flags, addr, offset, size, align) -> bytes:
        return struct.pack("<IIQQQQIIQQ", name_off, sh_type, flags, addr, offset, size, 0, 0, align, 0)

    text_off = 0x1C0
    shstr_off = text_off + len(ELF_TEXT_MARKER)
    shdrs = (
        b"\x00" * 0x40
        + shdr(1, 1, 6, ELF_ENTRY, text_off, len(ELF_TEXT_MARKER), 16)   # .text SHT_PROGBITS AX
        + shdr(7, 3, 0, 0, shstr_off, len(shstrtab), 1)                   # .shstrtab SHT_STRTAB
    )
    assert len(shdrs) == 3 * 0x40

    out = bytearray()
    out += ehdr
    out += phdr
    out += b"\x00" * (0x100 - len(out))
    out += shdrs
    out += b"\x00" * (text_off - len(out))
    out += ELF_TEXT_MARKER
    out += shstrtab
    return bytes(out)


def elf_expected() -> dict:
    return {
        "sha256": hashlib.sha256(build_elf64()).hexdigest(),
        "machine": "x86_64",
        "type": "EXEC",
        "entry": ELF_ENTRY,
        "section_names": list(ELF_SECTION_NAMES),
    }


# ------------------------------------------------------------------------ Mach-O

MACHO_CPU = 0x01000007  # CPU_TYPE_X86_64
MACHO_FILETYPE = 2      # MH_EXECUTE
MACHO_SEGNAME = "__TEXT"


def build_macho64() -> bytes:
    """Thin Mach-O 64 x86-64 executable with a single LC_SEGMENT_64."""
    segname = MACHO_SEGNAME.encode().ljust(16, b"\x00")
    segment = struct.pack(
        "<II16sQQQQIIII",
        0x19,        # LC_SEGMENT_64
        72,          # cmdsize
        segname,
        0x100000000, # vmaddr
        0x1000,      # vmsize
        0,           # fileoff
        0x1000,      # filesize
        5,           # maxprot RX
        5,           # initprot RX
        0,           # nsects
        0,           # flags
    )
    assert len(segment) == 72

    header = struct.pack(
        "<IIIIIIII",
        0xFEEDFACF,  # MH_MAGIC_64
        MACHO_CPU,
        3,           # cpusubtype X86_64_ALL
        MACHO_FILETYPE,
        1,           # ncmds
        len(segment),
        0,           # flags
        0,           # reserved
    )
    body = header + segment
    return body.ljust(0x100, b"\x00")


def macho_expected() -> dict:
    return {
        "sha256": hashlib.sha256(build_macho64()).hexdigest(),
        "cputype": "x86_64",
        "filetype": "EXECUTE",
        "ncmds": 1,
        "segname": MACHO_SEGNAME,
    }


# --------------------------------------------------------------------------- DEX

DEX_VERSION = 35
DEX_HEADER_SIZE = 0x70


def build_dex() -> bytes:
    """Minimal DEX 035 with no ids and no data section (valid, empty program)."""
    header = bytearray(DEX_HEADER_SIZE)
    header[0:8] = b"dex\n035\x00"
    struct.pack_into("<I", header, 32, DEX_HEADER_SIZE)  # file_size
    struct.pack_into("<I", header, 36, DEX_HEADER_SIZE)  # header_size
    struct.pack_into("<I", header, 40, 0x12345678)       # endian_tag
    # link_size/off, map_off, string_ids, type_ids, proto_ids,
    # field_ids, method_ids, class_defs, data_size/off stay zero.

    # Order matters: the SHA-1 covers everything after the signature field, and
    # the Adler-32 checksum covers everything after the checksum field, so the
    # signature must be written before the checksum is computed.
    header[12:32] = hashlib.sha1(bytes(header[32:])).digest()
    struct.pack_into("<I", header, 8, zlib.adler32(bytes(header[12:])) & 0xFFFFFFFF)
    return bytes(header)


def dex_expected() -> dict:
    return {
        "sha256": hashlib.sha256(build_dex()).hexdigest(),
        "version": DEX_VERSION,
        "file_size": DEX_HEADER_SIZE,
        "endian_tag": 0x12345678,
    }


ALL_BUILDERS = {
    "pe": build_pe64,
    "elf": build_elf64,
    "macho": build_macho64,
    "dex": build_dex,
}
