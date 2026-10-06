# unpack-deobfusc — 授权反混淆与脱壳

## 边界

仅处理自研、公开无害或明确授权样本。始终复制后操作，保留原件 hash；License/激活逻辑只定位，不提供绕过、patch、伪造响应或 keygen。

## 环境

```bash
sudo apt-get update
sudo apt-get install -y upx-ucl
upx --version
# 可选：sudo apt-get install -y binwalk || echo 'binwalk 未安装'
```

## 自动识别与 UPX 脱壳

```bash
scripts/unpack/unpack_auto.sh --output case/unpack packed.bin
```

流程：复制原件→`upx -t` 识别→超时保护的 `upx -d`→前后 SHA-256/file→自动差异报告。非 UPX 不猜测解包，不覆盖输入。

## 字符串解密候选

```bash
python3 scripts/unpack/strcrypto_find.py unpacked.bin -o strcrypto-candidates.json
```

结合关键词文件偏移与 objdump 中 XOR+回跳函数评分，输出函数地址和 call 线索。候选不等于密码算法，更不自动执行未知代码。

## 前后差异

```bash
python3 scripts/unpack/dump_diff.py packed.bin unpacked.bin -o diff.json --markdown diff.md
```

比较 hash、大小、Shannon entropy、ELF 节区和未定义导入。readelf 失败时保留 stderr/退出码。

## 自制无害样本验证

```bash
gcc -O2 -o hello hello.c
upx -9 -o hello.upx hello
scripts/unpack/unpack_auto.sh --output result hello.upx
result/unpacked.bin
```

## 已知问题与限制

- 自动解包仅支持当前 UPX 能识别的格式；定制壳、虚拟化壳和加密 loader 需人工动态分析。
- 高熵不是加密/加壳证明；编译器、压缩资源也会提高熵。
- objdump 候选评分会误报普通 XOR/循环，也会漏掉 SIMD、表驱动或运行时生成代码。
- 内核级壳、驱动、GUI 交互和强反调试对抗在本沙箱不可完整复现。
- dump 后导入重建、重定位和入口修复不可假装自动成功；必须真实执行验证。

## 输出契约

报告输入/输出 hash、UPX 原始 stdout/stderr、退出码、节区/熵/导入变化和运行验证。失败原文不得省略。
