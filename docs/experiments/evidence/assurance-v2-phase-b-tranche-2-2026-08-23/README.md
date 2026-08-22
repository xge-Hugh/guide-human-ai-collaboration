# Phase B tranche 2 阻断运行云端协作交接

本目录是供人类与云端 Agent 共同判断是否另行授权重启 tranche 2 的完整证据包。它逐字复制了本次唯一一次获授权运行所产生的全部 7 条 record、14 份逐调用 evidence、resolved plan、manifest、run status 和自动 summary，并把 tranche 1 的联合人工裁决备注与原始 Qwen 判断分开保存。

本次运行触发预注册的正式阻断条件并按设计停止，因此这里的“完整”是指**本次阻断运行实际产生的全部证据**，不是说 repetitions 2–3 已经完成。不得把这个前缀当作完整 tranche 2，也不得据此宣布 B0/B1/B2 胜者。

## 与 tranche 1 的关系

- tranche 1 完整发布包：[`../assurance-v2-phase-b-tranche-1-2026-08-22/`](../assurance-v2-phase-b-tranche-1-2026-08-22/)
- 原实验 revision：`4c805561e0d3d73613291133e9bed6b5b786a484`
- 共同 resolved-plan SHA-256：`c9ddc1d82f5c9b7a45481443f71ee08fb185c942638b7815e61068a62efa9a52`
- 原始私有 tranche-1 run：`40098907d5c5452a81d8677b26a4e33c`
- 本次 tranche-2 blocked run：`ed2c0c99bfa64fcea316b0deb1e9c6f3`
- 本次 raw artifact-tree SHA-256：`ce47643c063ae1cbec8850d13eec448b334b03a7c0ff0e9681938debaed075b9`

tranche 1 的 30 个原始 Qwen 判断没有被修改。联合人工裁决只作为独立 sidecar 保存在 [`joint-human-adjudication-notes.json`](joint-human-adjudication-notes.json)：

- `p011/B0/r001`：暂定 `partial`，不能有把握地判为 `satisfied`；
- `p012/B1/r001`：位于 `partial` 与 `satisfied` 的边界；
- `p012/B2/r001`：保护遗漏；`late_recoverable` 比 `too_late` 更合理。

这些裁决没有用于修改 prompt、rubric、variant 或 tranche-2 条件。

## 运行前离线确认

在没有 provider 网络调用的阶段完成了：

- detached worktree 的 HEAD 精确为 `4c805561...a484`，Git 状态干净；
- 21/21 harness tests 通过；
- formal `validate` 返回 `network_calls: 0`；
- formal `plan` 精确重现 `c9ddc1d8...a9a52`；
- 原始 tranche-1 private run 的 `report` 校验通过，状态为 `completed`、30 records、60 calls、secret scan pass；
- 模型、token budget、timeout、renderer、cases、rubrics、grading axes、standalone context 与零重试政策均保持不变；
- tranche 2 仍只包含 repetition 2 `B1 -> B2 -> B0` 与 repetition 3 `B2 -> B0 -> B1`，计划 60 records、最多 120 calls。

## 唯一一次获授权运行的结果

运行从 repetition 2 开始，完成 p003 和 p004 的全部三个 variant；在 `p005/B1/r002` 的 generator 成功后，grader 调用发生 `RemoteDisconnected`。harness 将其归类为 `grader_transport_or_invocation_failure`，保存失败证据，停止后续调用，并将 run 正式标记为 `blocked`。

| record | generator | grader / 原始逐轴结果 |
|---|---|---|
| `p003/B1/r002` | succeeded | applicable / on_time / satisfied / compensation no / over-trigger none |
| `p003/B2/r002` | succeeded | applicable / on_time / satisfied / compensation no / over-trigger none |
| `p003/B0/r002` | succeeded | applicable / on_time / unsatisfied / compensation yes / over-trigger low |
| `p004/B1/r002` | succeeded | not_applicable / not_applicable / not_applicable / compensation no / over-trigger none |
| `p004/B2/r002` | succeeded | not_applicable / not_applicable / not_applicable / compensation no / over-trigger none |
| `p004/B0/r002` | succeeded | not_applicable / not_applicable / not_applicable / compensation no / over-trigger none |
| `p005/B1/r002` | succeeded | failed：`RemoteDisconnected`，无 grade |

以上仅是候选 grader 的原始输出转录，不是人工确认结论。完整 applicability basis、notes、请求和回答见逐调用文件。

运行级事实：

- 7 次 generator 调用全部成功；6 次 grader 成功，1 次 grader 失败；
- 共 14 次网络调用，每次 `attempt_count=1`、`retry_count=0`；
- repetition 3 未开始；
- secret scan 为 `pass`，`secret_match_files=[]`；
- generator configured model 为 `deepseek-v4-flash`，成功调用的 provider-reported model 为 `deepseek-v4-flash-202605`；
- grader configured/provider-reported model 为 `qwen3.7-plus`；
- generator 共 2,480 prompt、19,562 completion、22,042 total tokens，其中 reasoning 14,897；
- 成功 grader 共 7,697 prompt、7,550 completion、15,247 total tokens，其中 reasoning 6,640；失败调用没有 provider usage；
- generator latency 合计 205,900.895 ms、中位数 25,815.605 ms；包含失败调用的 grader latency 合计 399,710.556 ms、中位数 19,016.856 ms。

## 证据索引

- [`blocked-run/resolved_plan.json`](blocked-run/resolved_plan.json)：与 tranche 1 相同的完整冻结计划。
- [`blocked-run/manifest.json`](blocked-run/manifest.json)：run、角色、source、tranche scope 和 prior-run 绑定。
- [`blocked-run/run_status.json`](blocked-run/run_status.json)：正式 blocked 状态、14 次调用、secret scan 和 artifact-tree digest。
- [`blocked-run/summary.json`](blocked-run/summary.json)：自动生成的描述性分组视图；不替代人工裁决。
- [`blocked-run/call_evidence/`](blocked-run/call_evidence/)：14 份精确模型可见请求、最终输出或失败、公开响应 metadata、token、耗时、模型身份、attempt/retry 状态。
- [`blocked-run/records/`](blocked-run/records/)：7 条 record，包含 6 份原始逐轴判断和 1 条正式阻断记录。

`blocked-run/` 是私有原始 run 的逐字副本。不得编辑其中 JSON；否则 `run_status.json` 绑定的 artifact-tree digest 会失效。

## 发布提交与 plan hash 限制

本证据发布会推进当前分支 HEAD。resolved plan 把 Git revision、source 原始字节和解析后的绝对 output root 都纳入 hash，因此**不得从本发布提交规划或执行任何后续 tranche 2**。

尤其需要保留已经验证成功的独立 worktree：

- worktree：`/mnt/c/projects/guide-human-ai-collaboration-phase-b-tranche-2`
- revision：`4c805561e0d3d73613291133e9bed6b5b786a484`
- generation SHA-256：`b83a56690615b0bf59f87103170637064756b08a9e4295d29fe1d421302f6372`
- English semantic-source SHA-256：`bbe9b865efd07357810cd6eb8850fb18230fefc27bbca43b9faa75b0bf358517`
- zh-CN variants SHA-256：`d72157251b1d7e83b3fc96034704d6e2424331d3fa41f0743b65ce5cbcc6da01`
- rubrics SHA-256：`ed6ecd528f50ecdf37db4029979ca0aabbc0b331512dbce5774276ccf2fe6bae`
- resolved output root：`/home/xge/.local/share/guide-human-ai-collaboration/assurance-eval-results`

一次普通的新 checkout 曾因换行字节归一化而不能通过 semantic-source hash，且会产生不同 plan hash。不要“修复”hash 校验、重新格式化 source、改写 output path，或用发布后的 HEAD 代替原实验 revision。若人类与云端 Agent 决定继续，需要把当前 blocked run 作为 operational-failure evidence 永久保留，再由人类另行明确授权一次新的 tranche-2 run；新 run 仍必须从上述独立 worktree 离线重现 `c9dd...a9a52`，并继续使用原始 tranche-1 private run 作为 `--prior-run`。

## 解释边界

本包不计算总分，不自动宣布 variant 胜者，也不对 repetitions 1–3 作合并解释。当前只有完整 repetition 1 和 repetition 2 的一个阻断前缀。本地 Agent 没有给出效果解释；是否因纯 operational failure 另行授权重启，由人类和云端协作者独立审查本包与 tranche 1 后共同决定。
