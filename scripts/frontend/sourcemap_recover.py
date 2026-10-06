#!/usr/bin/env python3
"""Locate sourceMappingURL, load a v3 map, list and safely recover sourcesContent."""
from __future__ import annotations
import argparse,base64,hashlib,json,pathlib,re,urllib.parse,urllib.request
MAPREF=re.compile(r'(?://[#@]|/\*[#@])\s*sourceMappingURL=([^\s*]+)')
def get(ref,base,timeout):
 if ref.startswith('data:'):
  meta,data=ref.split(',',1); raw=base64.b64decode(data) if ';base64' in meta else urllib.parse.unquote_to_bytes(data); return 'inline',raw
 if urllib.parse.urlsplit(base).scheme in ('http','https'):
  u=urllib.parse.urljoin(base,ref); return u,urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'frontend-re/1.0'}),timeout=timeout).read()
 p=(pathlib.Path(base).parent/ref).resolve(); return str(p),p.read_bytes()
def safe(name,i):
 parts=[x for x in pathlib.PurePosixPath(name).parts if x not in ('','/','.','..')]
 return pathlib.Path(*parts) if parts else pathlib.Path(f'source-{i}.txt')
def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('javascript'); ap.add_argument('-o','--output-dir',type=pathlib.Path,required=True); ap.add_argument('--timeout',type=int,default=15); ns=ap.parse_args()
 base=ns.javascript
 if urllib.parse.urlsplit(base).scheme in ('http','https'): text=urllib.request.urlopen(urllib.request.Request(base,headers={'User-Agent':'frontend-re/1.0'}),timeout=ns.timeout).read().decode(errors='replace')
 else:text=pathlib.Path(base).read_text(errors='replace')
 refs=MAPREF.findall(text); ns.output_dir.mkdir(parents=True,exist_ok=True); maps=[]
 for ref in refs:
  loc,raw=get(ref,base,ns.timeout); data=json.loads(raw); recovered=[]
  for i,name in enumerate(data.get('sources',[])):
   item={'index':i,'name':name,'recovered':False}
   contents=data.get('sourcesContent') or []
   if i<len(contents) and contents[i] is not None:
    dest=ns.output_dir/'sources'/safe(name,i); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(contents[i]); item.update(recovered=True,path=str(dest),sha256=hashlib.sha256(contents[i].encode()).hexdigest())
   recovered.append(item)
  safe_ref=('data:[REDACTED sha256='+hashlib.sha256(raw).hexdigest()[:12]+']') if ref.startswith('data:') else ref
  maps.append({'reference':safe_ref,'location':loc,'version':data.get('version'),'sourceRoot':data.get('sourceRoot'),'sources':recovered,'names_count':len(data.get('names',[]))})
 result={'schema':'frontend-re/sourcemap-v1','javascript':base,'map_count':len(maps),'maps':maps}; (ns.output_dir/'sourcemap-report.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n'); print(json.dumps({'map_count':len(maps),'source_count':sum(len(x['sources']) for x in maps),'recovered_count':sum(y['recovered'] for x in maps for y in x['sources'])}))
if __name__=='__main__': main()
