#!/usr/bin/env python3
"""Offline PCAP session reconstruction, layer statistics, and plaintext/encryption heuristic."""
from __future__ import annotations
import argparse, collections, json, pathlib, re
from scapy.all import PcapReader, IP, IPv6, TCP, UDP, Raw

PRINTABLE=re.compile(rb'^[\x09\x0a\x0d\x20-\x7e]+$')
TLS_PORTS={443,465,853,993,995,8443}; CLEAR_PORTS={21,25,53,80,110,143,8080}
def endpoint(p):
    if IP in p: return p[IP].src,p[IP].dst,'IPv4'
    if IPv6 in p: return p[IPv6].src,p[IPv6].dst,'IPv6'
    return None,None,'non-IP'
def flow_key(p):
    src,dst,net=endpoint(p)
    if TCP in p: proto='TCP'; sport,dport=p[TCP].sport,p[TCP].dport
    elif UDP in p: proto='UDP'; sport,dport=p[UDP].sport,p[UDP].dport
    else: return (net,src,dst,None,None)
    a=(str(src),int(sport)); b=(str(dst),int(dport)); lo,hi=sorted((a,b))
    return (proto,lo[0],lo[1],hi[0],hi[1])
def classify(payload:bytes,ports:set[int]):
    if ports & TLS_PORTS or payload.startswith((b'\x16\x03',b'\x17\x03')): return 'encrypted-likely'
    if payload and PRINTABLE.match(payload[:512]): return 'plaintext-likely'
    if ports & CLEAR_PORTS: return 'plaintext-or-clear-protocol'
    return 'unknown'
def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('pcap',type=pathlib.Path); ap.add_argument('-o','--output',type=pathlib.Path,required=True); ns=ap.parse_args()
    layers=collections.Counter(); flows={}; packets=0
    with PcapReader(str(ns.pcap)) as reader:
      for p in reader:
        packets+=1
        for layer in ('Ether','IP','IPv6','TCP','UDP','DNS','Raw'):
          if p.haslayer(layer): layers[layer]+=1
        key=flow_key(p); k='|'.join(map(str,key)); f=flows.setdefault(k,{'key':key,'packets':0,'bytes':0,'first':float(p.time),'last':float(p.time),'payload_bytes':0,'sample_hex':'','directions':collections.Counter()})
        f['packets']+=1; f['bytes']+=len(p); f['first']=min(f['first'],float(p.time)); f['last']=max(f['last'],float(p.time))
        src,dst,_=endpoint(p); f['directions'][f'{src}->{dst}']+=1
        if Raw in p:
          data=bytes(p[Raw].load); f['payload_bytes']+=len(data)
          if not f['sample_hex']: f['sample_hex']=data[:32].hex()
    out=[]
    for f in flows.values():
      ports={x for x in (f['key'][2],f['key'][4]) if isinstance(x,int)}
      sample=bytes.fromhex(f['sample_hex']) if f['sample_hex'] else b''
      f['duration']=round(f['last']-f['first'],6); f['classification']=classify(sample,ports); f['directions']=dict(f['directions']); out.append(f)
    result={'schema':'protocol-re/pcap-rebuild-v1','pcap':str(ns.pcap.resolve()),'packet_count':packets,'layer_counts':dict(layers),'session_count':len(out),'sessions':out,'heuristic_notice':'Encryption classification is heuristic; TLS port/signature is not proof of confidentiality.'}
    ns.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n'); print(json.dumps({'packet_count':packets,'session_count':len(out),'layer_counts':dict(layers)},sort_keys=True))
if __name__=='__main__': main()
