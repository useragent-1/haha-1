#!/usr/bin/env python3
"""Summarize process, filesystem, network, persistence and environment behavior from traces."""
from __future__ import annotations
import argparse, json, pathlib, re
from collections import defaultdict

PID=re.compile(r'^(?P<pid>\d+)\s+')
EXEC=re.compile(r'execve\("(?P<path>[^"]+)"')
CHILD=re.compile(r'(?:clone|clone3|fork|vfork)\(.*\)\s+=\s+(?P<child>\d+)')
OPEN_WRITE=re.compile(r'(?:open|openat)\([^\n]*?"(?P<path>[^"]+)"[^\n]*?(?:O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND)')
FILE_MUTATE=re.compile(r'(?:rename(?:at2?)?|unlink(?:at)?|mkdir(?:at)?|rmdir|symlink(?:at)?|link(?:at)?)\([^\n]*?"(?P<path>[^"]+)"')
CONNECT=re.compile(r'connect\([^\n]*?(?P<endpoint>(?:sin_addr=inet_addr\("[^"]+"\).*?sin_port=htons\(\d+\)|sun_path="[^"]+"|\[?[0-9a-fA-F:]+\]?:\d+))')
ENV=re.compile(r'\b(?:setenv|putenv|unsetenv)\("(?P<name>[A-Za-z_][A-Za-z0-9_]*)')
PERSIST=re.compile(r'(?i)(?:/\.config/autostart/|/etc/(?:cron|systemd|init)|/var/spool/cron|\.service\b|crontab\b|rc\.local\b)')

def uniq(items): return list(dict.fromkeys(items))
def read(path): return path.read_text(errors='replace') if path and path.exists() else ''

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--strace',type=pathlib.Path,required=True)
    ap.add_argument('--ltrace',type=pathlib.Path)
    ap.add_argument('-o','--output-dir',type=pathlib.Path,required=True)
    ns=ap.parse_args(); ns.output_dir.mkdir(parents=True,exist_ok=True)
    st=read(ns.strace); lt=read(ns.ltrace)
    execs=[]; edges=[]; writes=[]; network=[]; persistence=[]; env=[]
    for line in st.splitlines():
        pm=PID.match(line); pid=int(pm.group('pid')) if pm else None
        m=EXEC.search(line)
        if m: execs.append({'pid':pid,'path':m.group('path')})
        m=CHILD.search(line)
        if m: edges.append({'parent_pid':pid,'child_pid':int(m.group('child'))})
        for rx in (OPEN_WRITE,FILE_MUTATE):
            m=rx.search(line)
            if m:
                item={'pid':pid,'path':m.group('path'),'syscall':line.split('(',1)[0].split()[-1]}
                writes.append(item)
                if PERSIST.search(item['path']): persistence.append(item)
        m=CONNECT.search(line)
        if m: network.append({'pid':pid,'endpoint':m.group('endpoint')})
        if PERSIST.search(line): persistence.append({'pid':pid,'evidence':line.strip()[:500]})
    for line in (st+'\n'+lt).splitlines():
        m=ENV.search(line)
        if m: env.append({'name':m.group('name'),'operation':line.split('(',1)[0].split()[-1]})
    result={'schema':'dynamic-recon/behavior-v1','sources':{'strace':str(ns.strace),'ltrace':str(ns.ltrace) if ns.ltrace else None},'processes':execs,'process_edges':edges,'file_writes':writes,'network_connections':network,'persistence_indicators':persistence,'environment_changes':env}
    # Stable de-duplication via canonical JSON.
    for k in ('processes','process_edges','file_writes','network_connections','persistence_indicators','environment_changes'):
        seen=set(); vals=[]
        for x in result[k]:
            key=json.dumps(x,sort_keys=True)
            if key not in seen: seen.add(key); vals.append(x)
        result[k]=vals
    (ns.output_dir/'behavior.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    lines=['# Behavior Report','']
    sections=[('Process executions','processes'),('Process tree edges','process_edges'),('File writes','file_writes'),('Network connections','network_connections'),('Persistence indicators','persistence_indicators'),('Environment variable changes (values redacted)','environment_changes')]
    for title,key in sections:
        lines += [f'## {title}','',f'Count: {len(result[key])}','']
        lines += [f'- `{json.dumps(x,ensure_ascii=False,sort_keys=True)}`' for x in result[key]] or ['- None observed']
        lines.append('')
    (ns.output_dir/'behavior.md').write_text('\n'.join(lines))
    print(json.dumps({k:len(result[k]) for _,k in sections},sort_keys=True))
    return 0
if __name__=='__main__': raise SystemExit(main())
