#!/usr/bin/env python3
"""Parse GDB text into a redaction-friendly crash summary."""
from __future__ import annotations
import argparse, json, pathlib, re, sys

FRAME = re.compile(r"^#(?P<index>\d+)\s+(?:(?P<addr>0x[0-9a-fA-F]+)\s+in\s+)?(?P<body>.*)$")
SIGNAL = re.compile(r"Program received signal\s+(?P<signal>[A-Z0-9]+)(?:,\s*(?P<description>.*))?\.")
STOPPED = re.compile(r"Program (?:terminated|stopped) with signal\s+(?P<signal>[A-Z0-9]+)(?:,\s*(?P<description>.*))?\.")
REG = re.compile(r"^(?P<name>(?:r(?:[0-9]+|ip|sp|bp|ax|bx|cx|dx|si|di)|e(?:ip|sp|bp|ax|bx|cx|dx|si|di)|pc|sp|lr|x[0-9]+))\s+(?P<value>0x[0-9a-fA-F]+)\b", re.I)
MAPPING = re.compile(
    r"^(?P<start>0x[0-9a-fA-F]+)\s+(?P<end>0x[0-9a-fA-F]+)\s+"
    r"(?P<size>0x[0-9a-fA-F]+)\s+(?P<offset>0x[0-9a-fA-F]+)\s+"
    r"(?P<perms>[-rwxps]+)(?:\s+(?P<path>.*))?$"
)

def parse(text: str) -> dict:
    signal = description = None
    frames, registers, mappings = [], {}, []
    for line in text.splitlines():
        m = SIGNAL.search(line) or STOPPED.search(line)
        if m and signal is None:
            signal, description = m.group('signal'), (m.groupdict().get('description') or '').strip()
        m = FRAME.match(line.strip())
        if m:
            body=m.group('body').strip()
            fn=body.split(' (',1)[0].split(' at ',1)[0].strip()
            frames.append({'index':int(m.group('index')),'address':m.group('addr'),'function':fn,'raw':line.strip()})
        m = REG.match(line.strip())
        if m: registers[m.group('name')]=m.group('value')
        m = MAPPING.match(line.strip())
        if m:
            item=m.groupdict(); item['path']=(item.get('path') or '').strip()
            mappings.append(item)
    key=[f for f in frames if not re.search(r"(__libc|libc_start|start_thread|clone)",f['function'])][:8]
    key_maps=[m for m in mappings if 'x' in m['perms'] or m['path'] in ('[stack]','[heap]')]
    return {'schema':'dynamic-recon/crash-trace-v1','signal':signal,'description':description,'frame_count':len(frames),'frames':frames,'key_frames':key,'registers':registers,'mapping_count':len(mappings),'mappings':mappings,'key_mappings':key_maps}

def markdown(data: dict) -> str:
    lines=['# Crash Trace','',f"- Signal: `{data['signal'] or 'not detected'}`",f"- Frames: {data['frame_count']}",'','## Key frames','','| # | Address | Function |','|---:|---|---|']
    for f in data['key_frames']:
        lines.append(f"| {f['index']} | `{f['address'] or ''}` | `{f['function'].replace('|','\\|')}` |")
    lines += ['','## Registers','']
    lines += [f"- `{k}` = `{v}`" for k,v in sorted(data['registers'].items())] or ['- Not found']
    lines += ['','## Key memory mappings','',f"Total mappings: {data['mapping_count']}",'','| Start | End | Perms | Offset | Path |','|---|---|---|---|---|']
    for m in data['key_mappings']:
        safe_path=m['path'].replace('|','\\|')
        lines.append(f"| `{m['start']}` | `{m['end']}` | `{m['perms']}` | `{m['offset']}` | `{safe_path}` |")
    if not data['key_mappings']: lines.append('|  |  |  |  | Not found |')
    return '\n'.join(lines)+'\n'

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('gdb_output',type=pathlib.Path)
    ap.add_argument('-o','--output',type=pathlib.Path)
    ap.add_argument('--format',choices=('json','markdown'),default='json')
    ns=ap.parse_args()
    data=parse(ns.gdb_output.read_text(errors='replace'))
    result=json.dumps(data,ensure_ascii=False,indent=2)+'\n' if ns.format=='json' else markdown(data)
    if ns.output: ns.output.write_text(result)
    else: sys.stdout.write(result)
    return 0 if data['frames'] or data['signal'] else 1
if __name__=='__main__': raise SystemExit(main())
