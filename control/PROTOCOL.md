# 多 Agent 编排协议（GitHub 控制面）

> 10 个 arena Agent 窗口通过本仓库互联。仓库 = 控制面 + 共享黑板 + 消息总线。

## 你的身份

启动时领取一个 worker id：`W01` ~ `W10`（不可重复）。

## 每个回合的标准动作（每次收到「检查控制面」时执行）

```
1. git pull origin main
2. 读 control/status/*.json → 写自己的心跳：
   control/status/<你的id>.json = { worker, state: idle|busy, task, hb: <时间戳> }
3. 读 control/blackboard/notes.md → 了解其他 agent 的发现
4. 读 control/tasks/*.json → 找 status=="pending" 的任务
   - 若已被别人 claimed 且 hb 在 5 分钟内 → 换下一个任务
   - 否则把该任务改成 {status:"claimed", claimed_by:"<你的id>", claimed_at:<时间戳>} 并 git push（push 成功才算领到）
   - 冲突（push 被拒）→ git pull --rebase 后换下一个任务
5. 如果领到任务 → 用逆向模式流程执行
6. 写 control/results/<任务id>.result.md（结论 + 原文证据 + 产物路径）
7. 在 control/blackboard/notes.md 追加：你的发现、对其他 worker 有用的提示
8. 把自己的 status 改回 idle
9. git add -A && git commit -m "..." && git push
```

## 任务格式（`control/tasks/T001.json`）

```json
{
  "id": "T001",
  "status": "pending",
  "title": "短标题",
  "goal": "要达成什么（可验证）",
  "target": "目标：文件路径 / URL / 样本",
  "deliverable": "产出：报告 / 脚本 / 二进制 / 结论",
  "constraints": ["速率限制", "只测授权目标", "不许做 X"],
  "claimed_by": null,
  "claimed_at": null
}
```

## 硬规则

| 规则 | 原因 |
|---|---|
| 一个任务只能被一个 worker 领（以 push 成功为准） | 避免 10 个 agent 抢同一个活 |
| 任务被 claim 后 30 分钟无心跳更新 → 标 `failed` 并写原因 | 防死锁 |
| 结论必须写进 `results/`，黑板只写摘要和给同伴的提示 | 黑板会被刷屏 |
| 不得重复别的 worker 已在做的任务 | 靠 `claimed_by` 判重 |
| push 冲突 → `git pull --rebase` 再 push | 并发写仓库必然冲突 |
| 结论必须贴原文证据（请求/响应/反编译输出） | 反向模式契约 |

## 状态文件格式（`control/status/W01.json`）

```json
{ "worker": "W01", "state": "idle", "task": null, "hb": "2026-10-06T10:00:00Z", "note": "" }
```

## 集群状态判定（编排器用）

- `idle` + `pending` 任务存在 → 该 worker 应该去领任务
- `claimed` 但 `hb` 超过 30 分钟 → 任务判死，可重派
- `results/` 里没有对应 result → 任务未完成
