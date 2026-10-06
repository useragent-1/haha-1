#!/usr/bin/env python3
"""Discover URLs, API paths, domains, WebSockets, and auth-header shapes in local/public frontend text."""
from __future__ import annotations
import argparse,hashlib,json,pathlib,re,sys,urllib.parse,urllib.request
URL=re.compile(r"(?:https?|wss?)://[A-Za-z0-9._~%:-]+(?:/[A-Za-z0-9._~%!$&'()*+,;=:@/?#\[\]-]*)?",re.I)
PATH=re.compile(r"[\"'`](/(?:api|v\d+|graphql|oauth|auth|socket|ws)(?:/[A-Za-z0-9._~%!$&()*+,;=:@{}?\[\]/-]*)?)[\"'`]",re.I)
DOMAIN=re.compile(r'(?<![\w.-])(?:[A-Za-z0-9-]+\.)+(?:com|org|net|io|dev|app|test|local|co|ai|gov|edu|cloud|xyz|info|biz|me|us|uk|cn|de|jp|fr|ru|ch|it|nl|se|no)(?![\w.-])',re.I)
AUTH=re.compile(r'(?i)(authorization|proxy-authorization)[\"\']?\s*[:=]\s*[\"\']?([^\r\n,;\"\']*)')
SCRIPT=re.compile(r'(?i)<script[^>]+src=["\']([^"\']+)["\']')
def fetch(url,timeout,max_bytes):
 req=urllib.request.Request(url,headers={'User-Agent':'dynamic-skill-recon/1.0 (public read-only)'})
 with urllib.request.urlopen(req,timeout=timeout) as r:
  final=r.geturl(); data=r.read(max_bytes+1); ctype=r.headers.get('Content-Type','')
 if len(data)>max_bytes: raise ValueError(f'response exceeds {max_bytes} bytes')
 return final,data.decode(errors='replace'),ctype
def sources(inp,timeout,max_bytes,follow_scripts):
 p=pathlib.Path(inp)
 if p.exists():
  fs=[p] if p.is_file() else sorted(x for x in p.rglob('*') if x.is_file() and x.suffix.lower() in {'.js','.mjs','.cjs','.ts','.tsx','.jsx','.html','.htm','.json'})
  for f in fs:
   if f.stat().st_size<=max_bytes: yield str(f),f.read_text(errors='replace')
  return
 final,text,_=fetch(inp,timeout,max_bytes); yield final,text
 if follow_scripts:
  origin=urllib.parse.urlsplit(final)
  for src in SCRIPT.findall(text)[:20]:
   u=urllib.parse.urljoin(final,src); q=urllib.parse.urlsplit(u)
   if (q.scheme,q.netloc)!=(origin.scheme,origin.netloc): continue
   try: fu,js,_=fetch(u,timeout,max_bytes); yield fu,js
   except Exception as e: print(f'warning: {u}: {e}',file=sys.stderr)
def ashape(v):
 m=re.match(r'(?i)(Bearer|Basic|Digest|Negotiate)\s+',v.strip()); return (m.group(1).title()+' [REDACTED]') if m else '[REDACTED expression]'
def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('input'); ap.add_argument('-o','--output',type=pathlib.Path,required=True); ap.add_argument('--timeout',type=int,default=15); ap.add_argument('--max-bytes',type=int,default=5_000_000); ap.add_argument('--follow-scripts',action='store_true'); ns=ap.parse_args()
 findings=[]; seen=set(); srcmeta=[]
 for name,text in sources(ns.input,ns.timeout,ns.max_bytes,ns.follow_scripts):
  srcmeta.append({'source':name,'sha256':hashlib.sha256(text.encode()).hexdigest(),'characters':len(text)})
  for ln,line in enumerate(text.splitlines(),1):
   candidates=[]
   candidates += [('websocket' if x.lower().startswith(('ws://','wss://')) else 'url',x) for x in URL.findall(line)]
   candidates += [('endpoint',x) for x in PATH.findall(line)]
   candidates += [('domain',x) for x in DOMAIN.findall(line)]
   candidates += [('authorization-pattern',ashape(m.group(2))) for m in AUTH.finditer(line)]
   for kind,val in candidates:
    key=(kind,val,name,ln)
    if key not in seen: seen.add(key); findings.append({'type':kind,'value':val,'source':name,'line':ln})
 out={'schema':'frontend-re/endpoints-v1','input':ns.input,'sources':srcmeta,'finding_count':len(findings),'findings':findings,'notice':'Authorization values are never emitted.'}
 ns.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n'); print(json.dumps({'sources':len(srcmeta),'findings':len(findings),'types':dict(__import__('collections').Counter(x['type'] for x in findings))},sort_keys=True))
if __name__=='__main__': main()
