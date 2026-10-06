#!/usr/bin/env python3
"""Extract protocol fields from PCAP and emit a reusable parsing template."""
from __future__ import annotations
import argparse,json,pathlib,re
from scapy.all import PcapReader,IP,IPv6,TCP,UDP,DNS,DNSQR,DNSRR,Raw
AUTH=re.compile(r'(?im)^(authorization|proxy-authorization):\s*([^\r\n]+)')
REQ=re.compile(r'^(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+(\S+)\s+HTTP/',re.M)
def redact_auth(v):
 m=re.match(r'(Bearer|Basic|Digest|Negotiate)\s+',v,re.I); return (m.group(1).title()+' [REDACTED]') if m else '[REDACTED]'
def sval(x): return x.decode(errors='replace') if isinstance(x,bytes) else str(x)
def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('pcap',type=pathlib.Path); ap.add_argument('-o','--output',type=pathlib.Path,required=True); ap.add_argument('--template',type=pathlib.Path,required=True); ns=ap.parse_args()
 records=[]; protocols=set()
 with PcapReader(str(ns.pcap)) as reader:
  for i,p in enumerate(reader,1):
   r={'packet':i,'time':float(p.time),'length':len(p)}
   if IP in p: r.update(network='IPv4',src=p[IP].src,dst=p[IP].dst,ttl=p[IP].ttl); protocols.add('IPv4')
   elif IPv6 in p: r.update(network='IPv6',src=p[IPv6].src,dst=p[IPv6].dst); protocols.add('IPv6')
   if TCP in p: r.update(transport='TCP',sport=p[TCP].sport,dport=p[TCP].dport,flags=str(p[TCP].flags),seq=p[TCP].seq,ack=p[TCP].ack); protocols.add('TCP')
   elif UDP in p: r.update(transport='UDP',sport=p[UDP].sport,dport=p[UDP].dport); protocols.add('UDP')
   if DNS in p:
    protocols.add('DNS'); d=p[DNS]; r['dns']={'id':d.id,'qr':d.qr,'opcode':d.opcode,'rcode':d.rcode}
    if d.qd and DNSQR in d: r['dns'].update(qname=sval(d[DNSQR].qname).rstrip('.'),qtype=d[DNSQR].qtype)
    answers=[]
    if d.an:
     for j in range(int(d.ancount)):
      try:a=d.an[j]; answers.append({'name':sval(a.rrname).rstrip('.'),'type':a.type,'rdata':sval(a.rdata)})
      except Exception: break
    if answers:r['dns']['answers']=answers
   if Raw in p:
    data=bytes(p[Raw].load); text=data[:8192].decode(errors='replace'); m=REQ.search(text)
    if m:
     protocols.add('HTTP'); headers={}
     for line in text.splitlines()[1:]:
      if ':' in line:
       k,v=line.split(':',1); k=k.strip().lower()
       if k in ('host','user-agent','content-type'): headers[k]=v.strip()
       elif k in ('authorization','proxy-authorization'): headers[k]=redact_auth(v.strip())
     r['http']={'method':m.group(1),'path':m.group(2),'headers':headers}
    r['payload_length']=len(data); r['payload_prefix_hex']=data[:32].hex()
   records.append(r)
 template={'schema':'protocol-re/parser-template-v1','protocols':sorted(protocols),'fields':{'IPv4':['src','dst','ttl'],'TCP':['sport','dport','flags','seq','ack'],'UDP':['sport','dport'],'DNS':['id','qr','rcode','qname','qtype','answers'],'HTTP':['method','path','headers.host','headers.user-agent','headers.authorization(redacted)']}}
 ns.output.write_text(json.dumps({'schema':'protocol-re/fields-v1','records':records},indent=2,ensure_ascii=False)+'\n'); ns.template.write_text(json.dumps(template,indent=2,ensure_ascii=False)+'\n'); print(json.dumps({'packets':len(records),'protocols':sorted(protocols),'template':str(ns.template)}))
if __name__=='__main__': main()
