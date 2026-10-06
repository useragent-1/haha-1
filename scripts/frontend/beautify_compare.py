#!/usr/bin/env python3
"""Conservative JS formatting plus before/after diff and obfuscation indicators."""
from __future__ import annotations
import argparse,difflib,hashlib,json,pathlib,re
def beautify(s):
 out=[];indent=0;quote=None;esc=False
 for c in s:
  if quote:
   out.append(c)
   if esc:esc=False
   elif c=='\\':esc=True
   elif c==quote:quote=None
   continue
  if c in "'\"`":quote=c;out.append(c)
  elif c=='{': indent+=1;out.append('{\n'+'  '*indent)
  elif c=='}': indent=max(0,indent-1);out.append('\n'+'  '*indent+'}')
  elif c==';':out.append(';\n'+'  '*indent)
  elif c=='\n':
   if out and not out[-1].endswith('\n'):out.append('\n'+'  '*indent)
  else:out.append(c)
 return re.sub(r'\n[ \t]*\n+', '\n', ''.join(out)).strip()+'\n'
def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('input',type=pathlib.Path); ap.add_argument('-o','--output',type=pathlib.Path,required=True); ap.add_argument('--diff',type=pathlib.Path,required=True); ap.add_argument('--analysis',type=pathlib.Path,required=True); ns=ap.parse_args()
 before=ns.input.read_text(errors='replace'); after=beautify(before); ns.output.write_text(after)
 ns.diff.write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile=str(ns.input),tofile=str(ns.output))))
 lines=before.splitlines() or ['']; indicators=[]
 checks=[('eval',r'\beval\s*\('),('Function-constructor',r'\bnew\s+Function\s*\('),('hex-escapes',r'(?:\\x[0-9a-fA-F]{2}){4,}'),('unicode-escapes',r'(?:\\u[0-9a-fA-F]{4}){3,}'),('array-rotation',r'\.push\s*\(.*\.shift\s*\(')]
 for name,rx in checks:
  n=len(re.findall(rx,before));
  if n: indicators.append({'type':name,'count':n})
 result={'schema':'frontend-re/beautify-v1','before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'before_lines':len(lines),'after_lines':len(after.splitlines()),'max_line_length':max(map(len,lines)),'long_lines_over_1000':sum(len(x)>1000 for x in lines),'indicators':indicators,'semantic_notice':'Formatting is lexical and not proof of semantic equivalence; inspect the diff.'}
 ns.analysis.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
