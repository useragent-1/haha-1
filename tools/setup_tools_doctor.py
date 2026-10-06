#!/usr/bin/env python3
"""Parse TOOLS.md and perform non-network command/import/path availability checks."""
from __future__ import annotations
import argparse,json,pathlib,shutil,subprocess,sys

def parse(path):
 rows=[]
 for line in path.read_text(errors='replace').splitlines():
  if not line.startswith('| ') or line.startswith('|---'):continue
  cells=[x.strip() for x in line.strip().strip('|').split('|')]
  if len(cells)!=7 or cells[0]=='类别':continue
  rows.append(dict(zip(('category','tool','purpose','declared_status','version','limits','check'),cells)))
 return rows
def check(row,timeout):
 spec=row['check'];detail=''
 if spec.startswith('cmd:'):
  c=spec[4:];p=shutil.which(c)
  if not p:
   for base in ('/usr/sbin','/usr/local/sbin'):
    x=pathlib.Path(base)/c
    if x.exists():p=str(x);break
  ok=bool(p);detail=p or 'command not found'
 elif spec.startswith('py:'):
  m=spec[3:]
  try:q=subprocess.run([sys.executable,'-c',f'import {m}'],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout);ok=q.returncode==0;detail='import ok' if ok else (q.stderr.strip().splitlines()[-1] if q.stderr.strip() else f'exit {q.returncode}')
  except subprocess.TimeoutExpired:ok=False;detail=f'import timeout>{timeout}s'
 elif spec.startswith('path:'):
  p=pathlib.Path(spec[5:]);ok=p.exists();detail=str(p) if ok else 'path missing'
 else:
  ok=False;detail='not installed by tier rule' if row['declared_status'] in ('仅记录','跳过') else row['limits']
 if ok:return 'PASS',detail
 if row['declared_status']=='失败':return 'FAIL',detail
 return 'MISSING',detail

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('tools_md',nargs='?',type=pathlib.Path,default=pathlib.Path('TOOLS.md'));ap.add_argument('--json',type=pathlib.Path);ap.add_argument('--timeout',type=int,default=15);ns=ap.parse_args();rows=parse(ns.tools_md);results=[]
 for r in rows:
  state,detail=check(r,ns.timeout);x={**r,'doctor':state,'detail':detail};results.append(x);print(f"{state}\t{r['category']}\t{r['tool']}\t{r['version']}\t{detail}")
 counts={k:sum(x['doctor']==k for x in results) for k in ('PASS','FAIL','MISSING')};print(f"SUMMARY\tTOTAL={len(results)}\tPASS={counts['PASS']}\tFAIL={counts['FAIL']}\tMISSING={counts['MISSING']}")
 if ns.json:ns.json.write_text(json.dumps({'schema':'tools-doctor/v1','tools_md':str(ns.tools_md.resolve()),'counts':counts,'results':results},indent=2,ensure_ascii=False)+'\n')
 return 0 if counts['FAIL']==0 else 1
if __name__=='__main__':raise SystemExit(main())
