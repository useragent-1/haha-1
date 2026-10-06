#!/usr/bin/env python3
"""Run auto_analyze.py over files in a directory with per-sample timeout and build an index."""
from __future__ import annotations
import argparse,datetime,hashlib,json,pathlib,re,subprocess,sys
def slug(p):return re.sub(r'[^A-Za-z0-9._-]+','_',p.name)[:100]
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('directory',type=pathlib.Path);ap.add_argument('-o','--output-dir',type=pathlib.Path,required=True);ap.add_argument('--analyzer',type=pathlib.Path,default=pathlib.Path('scripts/auto_analyze.py'));ap.add_argument('--timeout',type=int,default=120);ap.add_argument('--max-bytes',type=int,default=100_000_000);ap.add_argument('--quick',action='store_true');ns=ap.parse_args();ns.output_dir.mkdir(parents=True,exist_ok=True);rows=[]
 files=sorted(p for p in ns.directory.iterdir() if p.is_file())
 for i,p in enumerate(files,1):
  b=p.read_bytes();rec={'sample':p.name,'path':str(p.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'status':'pending','exit_code':None};dest=ns.output_dir/f'{i:03d}-{slug(p)}';dest.mkdir(exist_ok=True)
  if len(b)>ns.max_bytes:rec.update(status='skipped-size');rows.append(rec);continue
  cmd=[sys.executable,str(ns.analyzer),str(p),'--out',str(dest/'analysis'),'--json','--skip-yara']+(['--quick'] if ns.quick else [])
  try:
   q=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=ns.timeout);rec['exit_code']=q.returncode;rec['status']='ok' if q.returncode==0 else 'failed';(dest/'stdout.txt').write_text(q.stdout);(dest/'stderr.txt').write_text(q.stderr);(dest/'command.json').write_text(json.dumps(cmd)+'\n')
  except subprocess.TimeoutExpired as e:
   rec.update(status='timeout',exit_code=124);(dest/'stdout.txt').write_text((e.stdout or '') if isinstance(e.stdout,str) else '');(dest/'stderr.txt').write_text((e.stderr or '') if isinstance(e.stderr,str) else '')
  rows.append(rec);print(f"{p.name}\t{rec['status']}\t{rec['exit_code']}")
 result={'schema':'report/batch-index-v1','generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sample_count':len(rows),'ok_count':sum(x['status']=='ok' for x in rows),'rows':rows};(ns.output_dir/'index.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 md=['# Batch Analysis Index','',f"- Samples: {len(rows)}",f"- OK: {result['ok_count']}",'','| Sample | Bytes | SHA-256 | Status | Exit |','|---|---:|---|---|---:|']+[f"| `{x['sample']}` | {x['bytes']} | `{x['sha256']}` | {x['status']} | {x['exit_code']} |" for x in rows];(ns.output_dir/'index.md').write_text('\n'.join(md)+'\n');print(json.dumps({'sample_count':len(rows),'ok_count':result['ok_count'],'index':str(ns.output_dir/'index.json')}))
if __name__=='__main__':main()
