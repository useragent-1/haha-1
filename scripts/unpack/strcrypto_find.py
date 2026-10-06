#!/usr/bin/env python3
"""Rank static candidates for string decode/decrypt routines; report offsets and call clues only."""
from __future__ import annotations
import argparse,collections,json,pathlib,re,subprocess
KEYWORDS=(b'decrypt',b'decode',b'base64',b'xor',b'cipher',b'aes',b'rc4',b'rot13')
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('binary',type=pathlib.Path);ap.add_argument('-o','--output',type=pathlib.Path,required=True);ns=ap.parse_args();data=ns.binary.read_bytes();candidates=[]
 low=data.lower()
 for kw in KEYWORDS:
  pos=0
  while True:
   pos=low.find(kw,pos)
   if pos<0:break
   candidates.append({'kind':'keyword','offset_hex':hex(pos),'indicator':kw.decode(),'score':2});pos+=1
 proc=subprocess.run(['objdump','-d',str(ns.binary)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 lines=proc.stdout.splitlines(); funcs={};current=None
 for i,line in enumerate(lines):
  m=re.match(r'^([0-9a-fA-F]+) <([^>]+)>:',line)
  if m:current={'address':'0x'+m.group(1),'function':m.group(2),'xor_count':0,'loop_jumps':0,'calls':[]};funcs[current['address']]=current;continue
  if not current:continue
  if re.search(r'\bxor[bwlq]?\b',line):current['xor_count']+=1
  if re.search(r'\bj(?:ne|nz|mp|g|l|a|b)\b',line):current['loop_jumps']+=1
  cm=re.search(r'\bcall\w*\s+([0-9a-fx]+)(?:\s+<([^>]+)>)?',line)
  if cm:current['calls'].append({'target':cm.group(1),'symbol':cm.group(2)})
 for f in funcs.values():
  score=f['xor_count']*2+min(f['loop_jumps'],4)
  if f['xor_count'] and f['loop_jumps']:
   f['kind']='xor-loop-function';f['score']=score;candidates.append(f)
 result={'schema':'unpack-deobfusc/strcrypto-v1','binary':str(ns.binary.resolve()),'objdump_exit':proc.returncode,'objdump_stderr':proc.stderr,'candidate_count':len(candidates),'candidates':sorted(candidates,key=lambda x:x.get('score',0),reverse=True)[:100],'notice':'Candidates are static clues, not proof of cryptography.'}
 ns.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'candidate_count':result['candidate_count'],'objdump_exit':proc.returncode}))
if __name__=='__main__':main()
