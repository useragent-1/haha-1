# protocol-re deep evidence

`evidence/` 包含纯文档地址空间（192.0.2.0/24、198.51.100.0/24、203.0.113.0/24）生成的 6 包 HTTP+DNS 合成流量、生成器和三步输出。首次未显式设置 MAC 时 Scapy 只读环境报 `getmacbyip ... Operation not permitted` 并使用广播地址；fixture 随后固定本地 MAC，复测无警告。
