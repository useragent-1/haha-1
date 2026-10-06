#!/usr/bin/env python3
"""Extract API URLs, domains, WebSockets, endpoint paths and auth-header patterns."""
from __future__ import annotations
import argparse, json, pathlib, re, sys

TEXT_SUFFIXES={'.js','.mjs','.cjs','.ts','.tsx','.jsx','.html','.htm','.css','.json','.yaml','.yml','.xml','.py','.go','.rs','.java','.kt','.swift','.c','.cc','.cpp','.h','.hpp','.txt'}
URL=re.compile(r"(?P<url>(?:https?|wss?)://[A-Za-z0-9._~%:-]+(?:/[A-Za-z0-9._~%!$&'()*+,;=:@/?#\[\]-]*)?)",re.I)
DOMAIN=re.compile(r"(?<![A-Za-z0-9_.-])(?P<domain>(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,63})(?![A-Za-z0-9_.-])")
PATH=re.compile(r"[\"'`](?P<path>/(?:api|v[0-9]+|graphql|oauth|auth|socket|ws)(?:/[A-Za-z0-9._~%!$&()*+,;=:@{}?\[\]-]*)?)[\"'`]",re.I)
AUTH=re.compile(r"(?i)(authorization|proxy-authorization)[\"']?\s*[:=]\s*[\"']?([^\r\n,;\"']*)")

def files_for(path:pathlib.Path):
    if path.is_file(): yield path; return
    for p in sorted(path.rglob('*')):
        if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES and p.stat().st_size <= 10*1024*1024: yield p

def auth_shape(value:str)->str:
    value=value.strip()
    m=re.match(r'(?i)(Bearer|Basic|Digest|Negotiate)\s+',value)
    return (m.group(1).title()+' [REDACTED]') if m else '[REDACTED expression]'

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('path',type=pathlib.Path)
    ap.add_argument('-o','--output',type=pathlib.Path)
    ns=ap.parse_args()
    findings=[]; seen=set(); scanned=0
    root=ns.path.resolve()
    for p in files_for(root):
        scanned+=1
        try: text=p.read_text(errors='replace')
        except OSError as e:
            print(f'warning: {p}: {e}',file=sys.stderr); continue
        rel=str(p.resolve().relative_to(root)) if root.is_dir() else p.name
        for lineno,line in enumerate(text.splitlines(),1):
            for kind,rx,group in [('url',URL,'url'),('endpoint',PATH,'path'),('domain',DOMAIN,'domain')]:
                for m in rx.finditer(line):
                    value=m.group(group).rstrip(').,;')
                    if kind=='url' and value.lower().startswith(('ws://','wss://')): out_kind='websocket'
                    else: out_kind=kind
                    key=(out_kind,value,rel,lineno)
                    if key not in seen:
                        seen.add(key); findings.append({'type':out_kind,'value':value,'file':rel,'line':lineno})
            for m in AUTH.finditer(line):
                item={'type':'authorization-pattern','value':auth_shape(m.group(2)),'file':rel,'line':lineno}
                key=tuple(item.values())
                if key not in seen: seen.add(key); findings.append(item)
    result={'schema':'dynamic-recon/api-extractor-v1','root':str(root),'files_scanned':scanned,'finding_count':len(findings),'findings':findings}
    output=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if ns.output: ns.output.write_text(output)
    else: sys.stdout.write(output)
    return 0
if __name__=='__main__': raise SystemExit(main())
