from scapy.all import Ether,IP,TCP,UDP,DNS,DNSQR,DNSRR,Raw,wrpcap
p=[]
q=Ether(src='02:00:00:00:00:01',dst='02:00:00:00:00:02')/IP(src='192.0.2.10',dst='198.51.100.53')/UDP(sport=53000,dport=53)/DNS(id=0x1234,rd=1,qd=DNSQR(qname='example.test'))
r=Ether(src='02:00:00:00:00:01',dst='02:00:00:00:00:02')/IP(src='198.51.100.53',dst='192.0.2.10')/UDP(sport=53,dport=53000)/DNS(id=0x1234,qr=1,aa=1,qd=DNSQR(qname='example.test'),an=DNSRR(rrname='example.test',rdata='203.0.113.20'))
q.time=1.0;r.time=1.05;p += [q,r]
http=(b'GET /api/status HTTP/1.1\r\nHost: api.example.test\r\nUser-Agent: curl/8.14.1\r\nAuthorization: Bearer TEST_PLACEHOLDER\r\n\r\n')
for i,t in enumerate((2.0,7.0,12.0,17.0)):
 x=Ether(src='02:00:00:00:00:01',dst='02:00:00:00:00:02')/IP(src='192.0.2.10',dst='203.0.113.20')/TCP(sport=40000,dport=80,flags='PA',seq=1+i*len(http))/Raw(http)
 x.time=t;p.append(x)
wrpcap('/home/user/p2-protocol-test/mixed.pcap',p)
print('wrote_packets=',len(p),sep='')
