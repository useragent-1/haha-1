#!/usr/bin/env python3
"""Scan frontend text for credential/public-key/internal-address indicators without emitting values."""
from __future__ import annotations
import argparse,hashlib,json,pathlib,re
SUFFIX={'.js','.mjs','.cjs','.ts','.tsx','.jsx','.html','.htm','.json','.map','.env','.txt','.yaml','.yml'}
RULES={
 'private-key':re.compile(r'-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----'),
 'public-key':re.compile(r'-----BEGIN [A-Z0-9 ]*PUBLIC KEY-----'),
 'jwt':re.compile(r'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b'),
 'github-token':re.compile(r'\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b'),
 'aws-access-key':re.compile(r'\bAKIA[0-9A-Z]{16}\b'),
 'generic-secret-assignment':re.compile(r'(?i)\b(?:api[_-]?key|secret|token|password|authorization)\b\s*[:=]\s*["\']([^"\']{6,})["\']'),
 'private-ipv4':re.compile(r'\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b'),
 'localhost':re.compile(r'(?i)\b(?:localhost|127\.0\.0\.1)\b'),
}
def iterfiles(p):
 if p.is_file():yield p
 else:
  for f in p.rglob('*'):
   if f.is_file() and f.suffix.lower() in SUFFIX and f.stat().st_size<=10_000_000:yield f
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('path',type=pathlib.Path);ap.add_argument('-o','--output',type=pathlib.Path,required=True);ns=ap.parse_args();find=[];n=0
 for f in iterfiles(ns.path):
  n+=1;text=f.read_text(errors='replace')
  for ln,line in enumerate(text.splitlines(),1):
   for kind,rx in RULES.items():
    for m in rx.finditer(line):
     raw=m.group(1) if m.lastindex else m.group(0); find.append({'type':kind,'file':str(f),'line':ln,'column':m.start()+1,'length':len(raw),'fingerprint_sha256_12':hashlib.sha256(raw.encode()).hexdigest()[:12]})
 out={'schema':'frontend-re/secret-scan-v1','files_scanned':n,'finding_count':len(find),'findings':find,'notice':'Values are intentionally omitted; verify locations under authorization.'};ns.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'files_scanned':n,'finding_count':len(find),'types':dict(__import__('collections').Counter(x['type'] for x in find))},sort_keys=True))
if __name__=='__main__':main()
