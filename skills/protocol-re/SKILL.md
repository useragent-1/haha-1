# protocol-re — 授权协议与离线流量逆向

## 安全边界

仅处理自有、公开或明确授权的 PCAP；默认离线只读，不主动重放，不提取或外传凭据。Authorization/Cookie 只输出字段位置和认证方案，值强制脱敏。

## 环境与入口

```bash
# Linux sandbox
python3 -m pip install scapy 2>pip.err || python3 -m pip install --break-system-packages scapy
python3 -c 'import scapy; print(scapy.__version__)'
```

## 1. 会话重组与协议分层

```bash
python3 scripts/protocol/pcap_rebuild.py capture.pcap -o sessions.json
```

按双向五元组聚合会话，统计 Ether/IP/TCP/UDP/DNS/Raw 层，记录方向、包数、字节、持续时间和 payload 样本。明文/加密判断只是端口、TLS 记录头和可打印字符启发式，不能证明机密性。

## 2. 字段提取与解析模板

```bash
python3 scripts/protocol/field_extract.py capture.pcap -o fields.json --template parser-template.json
```

提取 IP、TCP/UDP、DNS、HTTP 请求字段；Authorization 只保留 `Bearer/Basic/... [REDACTED]`。模板给出观测协议和字段集合，供后续解析器实现。

## 3. 异常与 beaconing 扫描

```bash
python3 scripts/protocol/anomaly_scan.py capture.pcap -o anomalies.json --large-threshold 1400
```

检查固定间隔心跳、C2 beaconing 指标、异常包长和可疑 UA。结论必须写“启发式指标”，不能把低方差周期或 curl UA 单独判为恶意。

## 实测流程

```bash
python3 make_fixture.py                         # 只生成本地合成 PCAP，不发包
python3 scripts/protocol/pcap_rebuild.py mixed.pcap -o sessions.json
python3 scripts/protocol/field_extract.py mixed.pcap -o fields.json --template template.json
python3 scripts/protocol/anomaly_scan.py mixed.pcap -o anomalies.json
```

## 已知问题与限制

- TCP 重组是会话级统计，不是完整乱序/重传字节流重组；分片、隧道、QUIC、HTTP/2 和 TLS 解密需专用工具。
- 加密判定基于端口/签名/可打印性，非密码学证明。
- Scapy 对损坏或超大 PCAP 可能慢；脚本不替代 Wireshark/tshark 人工复核。
- NAT、时钟漂移、抓包丢失会扭曲 beaconing；阈值需结合基线。
- 沙箱不执行实时网卡嗅探、凭据捕获或未授权流量注入。

## 输出契约

保留输入 SHA-256、命令、Scapy 版本、包数、会话数、原始异常输出、限制与错误原文。敏感字段只报告包号、字段名、协议和脱敏模式。
