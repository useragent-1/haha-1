# report-batch — 报告合成与批量分析

## 单文件 HTML

```bash
python3 scripts/report/make_html_report.py result.json notes.md \
  -o report.html --title 'Authorized Analysis' \
  --confidence high --conclusion 'All referenced stages exited 0.'
```

HTML 内联 CSS、JSON 和 Markdown/Text，离线可查看；证据表包含每个输入的字节数和 SHA-256。所有文本先 HTML escape，不执行输入中的脚本。

## 批量运行

```bash
python3 scripts/report/batch_runner.py samples/ -o batch-output \
  --analyzer scripts/auto_analyze.py --timeout 120 --quick
```

每个普通文件单独目录，保留 command/stdout/stderr，输出 `index.json` 与 `index.md`。默认跳过 YARA 生成，避免批量创建不必要规则。

## 已知问题与限制

- HTML 将 Markdown 作为转义后的原文展示，不实现完整 Markdown 渲染。
- 置信度由操作者明确选择；脚本不会把工具退出 0 自动等同于高置信度结论。
- batch runner 当前只扫描目录第一层，不递归；不会自动解压压缩包。
- 超时只能终止直接子进程；分析器派生的失控进程仍需沙箱级回收。
- 大样本、GUI、内核级和强反调试目标不适合普通批处理。

## 输出契约

必须保留失败退出码和 stderr；凭据值不得进入 HTML。批量索引报告 hash、状态和退出码，不用“成功数”替代逐样本证据。
