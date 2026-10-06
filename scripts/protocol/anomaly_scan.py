#!/usr/bin/env python3
"""Offline heuristic scan for periodic beaconing, abnormal lengths, and suspicious HTTP UAs."""
from __future__ import annotations
import argparse,collections,json,math,pathlib,re,statistics
from scapy.all import PcapReader,IP,IPv6,TCP,UDP,Raw
SUSPICIOUS=[re.compile(x,re.I) for x in (r'^curl/',r'^python-requests/',r'^wget/',r'powershell',r'bot\b',r'headless')]
def key(p):
 if IP in p:s,d=p[IP].src,p[IP].dst
 elif IPv6 in p:s,d=p[IPv6].src,p[IPv6].dst
 else:return None
 if TCP in p:return ('TCP',s,p[TCP].sport,d,p[TCP].dport)
 if UDP in p:return ('UDP',s,p[UDP].sport,d,p[UDP].dport)
def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('pcap',type=pathlib.Path); ap.add_argument('-o','--output',type=pathlib.Path,required=True); ap.add_argument('--large-threshold',type=int,default=1400); ns=ap.parse_args()
 times=collections.defaultdict(list); lengths=[]; findings=[]; n=0
 with PcapReader(str(ns.pcap)) as reader:
  for p in reader:
   n+=1; k=key(p)
   if k: times[str(k)].append(float(p.time))
   lengths.append(len(p))
   if len(p)>ns.large_threshold: findings.append({'type':'abnormal-length','packet':n,'length':len(p),'threshold':ns.large_threshold})
   if Raw in p:
    text=bytes(p[Raw].load)[:8192].decode(errors='replace')
    m=re.search(r'(?im)^User-Agent:\s*([^\r\n]+)',text)
    if m and any(rx.search(m.group(1)) for rx in SUSPICIOUS): findings.append({'type':'suspicious-user-agent','packet':n,'value':m.group(1)[:200]})
 for flow,ts in times.items():
  if len(ts)>=4:
   gaps=[b-a for a,b in zip(ts,ts[1:]) if b>=a]
   if len(gaps)>=3 and statistics.mean(gaps)>0:
    mean=statistics.mean(gaps); cv=statistics.pstdev(gaps)/mean
    if cv<=0.20: findings.append({'type':'periodic-beaconing','flow':flow,'samples':len(ts),'mean_interval':round(mean,6),'coefficient_of_variation':round(cv,6)})
 result={'schema':'protocol-re/anomaly-v1','pcap':str(ns.pcap.resolve()),'packet_count':n,'length_summary':{'min':min(lengths) if lengths else 0,'max':max(lengths) if lengths else 0,'mean':statistics.mean(lengths) if lengths else 0},'finding_count':len(findings),'findings':findings,'notice':'Heuristics are indicators, not proof of C2 or maliciousness.'}
 ns.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n'); print(json.dumps({'packet_count':n,'finding_count':len(findings),'types':dict(collections.Counter(x['type'] for x in findings))},sort_keys=True))
if __name__=='__main__': main()
