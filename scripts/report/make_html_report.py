#!/usr/bin/env python3
"""Combine JSON/Markdown evidence into a single, offline HTML report."""
from __future__ import annotations
import argparse,datetime,hashlib,html,json,pathlib
CSS="""body{font:15px/1.5 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#17202a}h1,h2{color:#17365d}table{border-collapse:collapse;width:100%}th,td{border:1px solid #bbb;padding:.45rem;text-align:left}pre{background:#f5f7f9;border:1px solid #d9e0e6;padding:1rem;overflow:auto;white-space:pre-wrap}.high{color:#176b2c}.medium{color:#8a5900}.low{color:#a12424}.meta{color:#566}section{margin:2rem 0}"""
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('inputs',nargs='+',type=pathlib.Path);ap.add_argument('-o','--output',type=pathlib.Path,required=True);ap.add_argument('--title',default='Agent Analysis Report');ap.add_argument('--conclusion',action='append',default=[]);ap.add_argument('--confidence',choices=('high','medium','low'),default='medium');ns=ap.parse_args()
 evidence=[];sections=[];signals=[]
 for p in ns.inputs:
  b=p.read_bytes();kind='JSON' if p.suffix.lower()=='.json' else 'Markdown/Text';evidence.append({'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'type':kind})
  text=b.decode(errors='replace')
  if kind=='JSON':
   try:
    obj=json.loads(text);pretty=json.dumps(obj,indent=2,ensure_ascii=False)
    for k in ('finding_count','packet_count','session_count','frame_count'):
     if k in obj:signals.append(f'{p.name}: {k}={obj[k]}')
   except Exception as e: pretty=text;signals.append(f'{p.name}: JSON parse error: {e}')
  else:pretty=text
  sections.append((str(p),kind,pretty))
 conclusions=ns.conclusion or signals or ['Evidence assembled; analyst conclusion not supplied.']
 lines=['<!doctype html>','<html lang="en">','<head>','<meta charset="utf-8">','<meta name="viewport" content="width=device-width,initial-scale=1">',f'<title>{html.escape(ns.title)}</title>',f'<style>{CSS}</style>','</head>','<body>',f'<h1>{html.escape(ns.title)}</h1>',f'<p class="meta">Generated UTC: {datetime.datetime.now(datetime.timezone.utc).isoformat()}</p>','<section>','<h2>Conclusions</h2>',f'<p>Confidence: <strong class="{ns.confidence}">{ns.confidence.upper()}</strong></p>','<ul>']
 lines += [f'<li>{html.escape(x)}</li>' for x in conclusions];lines += ['</ul>','</section>','<section>','<h2>Evidence table</h2>','<table>','<thead><tr><th>Path</th><th>Type</th><th>Bytes</th><th>SHA-256</th></tr></thead>','<tbody>']
 for e in evidence:lines.append(f"<tr><td>{html.escape(e['path'])}</td><td>{e['type']}</td><td>{e['bytes']}</td><td><code>{e['sha256']}</code></td></tr>")
 lines += ['</tbody>','</table>','</section>']
 for name,kind,text in sections:lines += ['<section>',f'<h2>{html.escape(name)}</h2>',f'<p class="meta">{kind}</p>',f'<pre>{html.escape(text)}</pre>','</section>']
 lines += ['</body>','</html>'];ns.output.write_text('\n'.join(lines)+'\n');print(json.dumps({'output':str(ns.output),'evidence_count':len(evidence),'confidence':ns.confidence,'bytes':ns.output.stat().st_size}))
if __name__=='__main__':main()
