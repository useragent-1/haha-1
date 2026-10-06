# unpack-deobfusc deep evidence

`evidence/` 保留无害 C 源码、原始/UPX/脱壳后三次运行文本、状态、hash、差异和字符串解密候选；不提交编译后二进制。首个 `-O2` fixture 将 XOR 优化掉而得到 0 candidate，此结果保留在工作区原始日志；改用 `-O0 -fno-inline` 后识别 `demo_decode` 地址 `0x1139`。
