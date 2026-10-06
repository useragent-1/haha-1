#!/usr/bin/env python3
"""Compare packed/unpacked binaries: hashes, entropy, ELF sections, and undefined imports."""
from __future__ import annotations
import argparse,collections,hashlib,json,math,pathlib,re,subprocess
def entropy(b):
 if not b:return 0.0
 c=collections.Counter(b);n=len(b);return -sum((v/n)*math.log2(v/n) for v in c.values())
def cmd(args):
 p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);return {'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def inspect(p):
 b=p.read_bytes(); sec=cmd(['readelf','-W','-S',str(p)]); sym=cmd(['readelf','-W','-s',str(p)])
 sections=[]
 for line in sec['stdout'].splitlines():
  m=re.match(r'\s*\[\s*\d+\]\s+(\S+)\s+(\S+)\s+([0-9a-fA-F]+)\s+([0-9a-fA-F]+)\s+([0-9a-fA-F]+)',line)
  if m:sections.append({'name':m.group(1),'type':m.group(2),'address':m.group(3),'offset':m.group(4),'size_hex':m.group(5)})
 imports=[]
 for line in sym['stdout'].splitlines():
  m=re.match(r'\s*\d+:\s+\S+\s+\d+\s+\S+\s+\S+\s+UND\s+(.+)$',line)
  if m:
   name=m.group(1).split()[0].split('@')[0]
   if name and name not in imports:imports.append(name)
 return {'path':str(p),'size':len(b),'sha256':hashlib.sha256(b).hexdigest(),'entropy':round(entropy(b),6),'sections':sections,'imports':imports,'readelf_section_exit':sec['exit'],'readelf_symbol_exit':sym['exit']}
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('before',type=pathlib.Path);ap.add_argument('after',type=pathlib.Path);ap.add_argument('-o','--output',type=pathlib.Path,required=True);ap.add_argument('--markdown',type=pathlib.Path);ns=ap.parse_args();a=inspect(ns.before);b=inspect(ns.after)
 result={'schema':'unpack-deobfusc/diff-v1','before':a,'after':b,'changes':{'size_delta':b['size']-a['size'],'entropy_delta':round(b['entropy']-a['entropy'],6),'sections_added':sorted(set(x['name'] for x in b['sections'])-set(x['name'] for x in a['sections'])),'sections_removed':sorted(set(x['name'] for x in a['sections'])-set(x['name'] for x in b['sections'])),'imports_added':sorted(set(b['imports'])-set(a['imports'])),'imports_removed':sorted(set(a['imports'])-set(b['imports']))}}
 ns.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 if ns.markdown:
  c=result['changes'];ns.markdown.write_text(f"# Binary Diff\n\n| Metric | Before | After |\n|---|---:|---:|\n| Size | {a['size']} | {b['size']} |\n| Entropy | {a['entropy']} | {b['entropy']} |\n\n- Sections added: `{c['sections_added']}`\n- Sections removed: `{c['sections_removed']}`\n- Imports added: `{c['imports_added']}`\n- Imports removed: `{c['imports_removed']}`\n")
 print(json.dumps(result['changes'],sort_keys=True))
if __name__=='__main__':main()
