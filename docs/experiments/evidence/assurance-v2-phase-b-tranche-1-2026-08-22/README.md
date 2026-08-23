# Phase B tranche 1 云端协作交接

本目录是人类明确授权发布的、供云端 Agent 与人类共同决定下一步的完整脱敏证据包。它包含正式 tranche 1 的全部 30 条 record、60 份逐调用 evidence、完整 resolved plan、manifest、run status、汇总，以及正式运行前的 3-call compatibility smoke。原始运行目录仍保留在本地私有存储中。

这些结果是 `raw_evidence_pending_adjudication`，不是已经确认的效果结论。评分器是候选测量工具，其判断仍需人类审查；tranche 1 也只有 repetition 1。尤其要注意，自动 `summary.json` 当前把所有 group 的 `requires_human_adjudication` 都写成 `false`，但规范源把 p008、p012 标为 `adjudication=derived`，协议要求它们的 6 条记录全部进入人工裁决，并对其余表面一致结果做分层盲抽查（至少 10%，每个 variant 至少一条、N/A 至少一条）。因此该 summary 字段不能被当作裁决已经完成的证据。

## 快速结论

- 正式运行完成，未阻塞：30/30 generator、30/30 grader 成功，零重试，所有 `finish_reason=stop`。
- 实际模型：generator 配置为 `deepseek-v4-flash`，provider 报告 `deepseek-v4-flash-202605`；grader 配置及报告均为 `qwen3.7-plus`。
- 固定参数：generator thinking enabled / `max_tokens=65536` / timeout 900 秒；grader thinking enabled / `max_tokens=32768` / timeout 600 秒；两者 `stream=false`。
- 正式 run ID：`40098907d5c5452a81d8677b26a4e33c`。
- resolved-plan SHA-256：`c9ddc1d82f5c9b7a45481443f71ee08fb185c942638b7815e61068a62efa9a52`。
- 实验运行提交：`4c805561e0d3d73613291133e9bed6b5b786a484`，运行开始时 worktree clean。
- 正式 artifact-tree SHA-256：`916e1f90859f31d12a3ff7a8883bec43eb6ce3cecbfbe8db62ca86a4e8139c78`。
- compatibility artifact-tree SHA-256：`861f2b873d49bff9824f7f07ab5a91c0f163219e544a683c21bd8a4474cba8d4`。
- 正式运行从 `2026-08-22T15:17:47.003496+00:00` 到 `2026-08-22T15:37:08.661727+00:00`，约 19 分 22 秒。

## 完整证据位置

- [`formal-run/resolved_plan.json`](formal-run/resolved_plan.json)：完整冻结计划，包括 cases、variants、全部 3 repetitions 的 counterbalanced 顺序、tranche 划分、模型、参数、timeout、renderer/source/provenance hashes 和零重试政策。
- [`formal-run/manifest.json`](formal-run/manifest.json)：本次运行角色绑定、来源哈希、运行提交与执行范围。
- [`formal-run/call_evidence/`](formal-run/call_evidence/)：60 次调用的精确模型可见请求、最终输出、公开响应元数据、token、耗时、模型身份、attempt/retry 状态；不含 provider 内部 reasoning。
- [`formal-run/records/`](formal-run/records/)：30 个 case × variant 记录，把 generator 与 grader evidence、解析后的逐轴评分放在同一条记录中。
- [`formal-run/summary.json`](formal-run/summary.json)：正常总报告的数据源。
- [`formal-run/run_status.json`](formal-run/run_status.json)：完成状态、调用数、秘密扫描与 artifact-tree digest。
- [`compatibility-run/`](compatibility-run/)：正式运行前 1 次 generator 与 2 次 grader 的完整 compatibility evidence；它不属于 Phase B effect evidence。

本仓库中已提交的 recipe、generation cases、variants 和 rubrics 是计划引用的规范源；上面的 plan/manifest 同时记录了它们在运行时的精确 SHA-256。

## tranche 1 逐 case 结果

表格依次给出 `applicability / timing / satisfaction / human_compensation_needed / over_trigger_cost`。

| Case | B0 | B1 | B2 |
|---|---|---|---|
| p003 | applicable / on_time / partial / no / none | applicable / on_time / satisfied / no / none | applicable / on_time / satisfied / no / none |
| p004 | not_applicable / not_applicable / not_applicable / no / none | not_applicable / not_applicable / not_applicable / no / none | not_applicable / not_applicable / not_applicable / no / none |
| p005 | applicable / on_time / satisfied / no / none | applicable / on_time / satisfied / no / none | applicable / on_time / satisfied / no / none |
| p006 | not_applicable / not_applicable / not_applicable / no / none | not_applicable / not_applicable / not_applicable / no / none | not_applicable / not_applicable / not_applicable / no / none |
| p007 | applicable / on_time / satisfied / no / none | applicable / on_time / satisfied / no / none | applicable / on_time / satisfied / no / none |
| p008 | applicable / on_time / partial / yes / low | applicable / on_time / satisfied / no / none | applicable / on_time / satisfied / no / none |
| p009 | applicable / on_time / satisfied / no / none | applicable / on_time / satisfied / no / none | applicable / on_time / satisfied / no / none |
| p011 | applicable / on_time / satisfied / yes / none | applicable / on_time / satisfied / yes / none | applicable / on_time / satisfied / no / low |
| p012 | applicable / on_time / partial / yes / none | applicable / on_time / satisfied / no / none | applicable / too_late / unsatisfied / yes / none |
| p013 | not_applicable / not_applicable / not_applicable / no / none | not_applicable / not_applicable / not_applicable / no / none | not_applicable / not_applicable / not_applicable / no / none |

聚合（每个 variant 均为 7 个 applicable、3 个 clean N/A）：

| Variant | satisfied | partial | unsatisfied | compensation=yes | low over-trigger |
|---|---:|---:|---:|---:|---:|
| B0 | 4 | 3 | 0 | 3 | 1 |
| B1 | 7 | 0 | 0 | 1 | 0 |
| B2 | 6 | 0 | 1 | 1 | 1 |

仅就 repetition 1 的候选 grader 输出看，B1 相对 B0 在 p003、p008、p012 改善且没有显见退化；B2 没有显示一致的额外增益，并在 p012 出现 `too_late / unsatisfied`，在 p011 出现 low over-trigger。这个观察不能替代 repetitions 2–3 或人类 adjudication。

建议云端协作者优先逐字审查：

1. p012 的 B2 是否真的完全遗漏最小情境概念绑定，还是 grader 对短响应过严。
2. p011 的 B0/B1 `human_compensation=yes` 与 B2 `over_trigger=low` 是否反映量表边界不稳，而非真实 treatment 差异。
3. B0/B1/B2 的 grader notes 是否存在把 variant 预期语义反向读入评分的迹象。
4. 三个 N/A cases（p004、p006、p013）是否确实没有 treatment 引入的额外摩擦。
5. `summary.json` 没有传播 derived-case 强制裁决标记是否属于 reporting 缺口；在修复或形成外部裁决记录前，不应把自动聚合升级为最终标签。

## Token 与延迟

| Role | prompt | completion | reasoning | total | 累计 elapsed |
|---|---:|---:|---:|---:|---:|
| generator | 10,580 | 36,946 | 27,200 | 47,526 | 418,637.293 ms |
| grader | 25,909 | 36,013 | 31,356 | 61,922 | 647,644.495 ms |
| combined | 36,489 | 72,959 | 58,556 | 109,448 | 1,066,281.788 ms |

累计调用耗时大于 wall time，因为 wall time 还受实际调用编排和计时边界影响；这里没有把它解释为并行度指标。

## 运行前兼容性与慢响应诊断

正式配置的 compatibility smoke 共 3 次调用、零重试并全部成功：

- generator p003/B2：114,387.465 ms，12,348 total tokens，其中 10,909 reasoning tokens，`finish_reason=stop`。
- grader p003 applicable：28,479.269 ms，3,215 total / 1,516 reasoning tokens，严格 JSON 成功解析。
- grader p004 N/A：26,226.825 ms，2,106 total / 1,407 reasoning tokens，严格 JSON 成功解析且条件规则有效。

在确定正式配置前还做过与 effect evidence 分离的人工诊断：极小请求下 flash/pro、thinking disabled/enabled 都在约 1.69–3.44 秒返回；而 `deepseek-v4-pro` 对接近正式的 p003/B0、thinking enabled、`max_tokens=4096` 请求用时约 80.37 秒，并以 `finish_reason=length` 结束（4,097 completion、3,926 reasoning tokens）。因此当时 60 秒失败的直接原因是 client timeout 小于长 reasoning 响应时间，而不是已观察到的路由或脚本死锁。该段是操作诊断记录，不是正式 effect evidence；逐调用原始文件未纳入本证据树。

## 被阻塞前序运行 ledger

成功的正式 run 之前有三次由人类分别明确授权的运行；每次运行内部均保持零自动重试，并在预注册允许的 operational failure 上停止。它们使用不同 plan/config，不能与成功 run 合并为 repetition 或效果证据。这里保留最小 ledger，证明重启源于运行故障而不是看到 treatment 表现后挑选：

| Run ID | Plan SHA | 配置摘要 | Calls | 阻塞原因 | Secret scan | Artifact tree |
|---|---|---|---:|---|---|---|
| `60d6bf3f4f9a4eb5ae5bee5c5c3d8e15` | `470728d2...298ac7` | pro/thinking/4096 generator；max/non-thinking/1024 grader；旧 60 秒调用限制 | 1 generator | `generator_transport_or_invocation_failure` | pass | `ac2fd440...b45e32` |
| `86c453050b1c407ea0bb5601273074d8` | `470728d2...298ac7` | 与上一行相同；单独获准再次尝试 | 1 generator | `generator_transport_or_invocation_failure` | pass | `474a305d...9360b` |
| `9d0aef11cc9b4c32aa110a36b8db2cbb` | `6f24b81d...606058` | flash/thinking/4096 generator；max/non-thinking/1024 grader | 3 generator + 2 grader | p003/B2 generator `finish_reason=length` | pass | `e2eba390...725a` |

这些旧 run 的 raw outputs 继续留在本地私有存储，未复制进当前效果审阅包，以免把已放弃的模型/budget 条件混入成功 tranche 1。若云端协作者认为必须审计其中某一份原始 operational failure，应单独提出范围，再由人类决定是否发布；上表不是对其 effect 内容的选择性汇报。

## 完整性、隐私与推送边界

两个复制后的 evidence 子树逐字保留原始 JSON。正式 `run_status.json` 和 compatibility `run_status.json` 都记录 `secret_scan=pass`、空 `secret_match_files`，并分别绑定上面的 artifact-tree digest。本次提交前还会针对实际私有 catalog 中的 API key、完整 base URL 与 hostname 再扫描整个发布目录。`formal-run/resolved_plan.json` 会披露原运行机的本地 `output_root` 路径；它不含凭据或网络 endpoint，但属于 plan-hash 输入，若改写就会破坏 `c9dd...` 绑定和正常 report 校验，所以作为最小本机路径披露原样保留。

按照预注册政策，下列内容有意不存在于证据中：API key、私有 endpoint/connection name、provider response ID、provider 内部 `reasoning_content`。保留的 reasoning 只有公开 usage 中的 token 数值。这里的“完整”指协议允许保存和用于审查的全部输入、最终输出、公开元数据与派生记录，而不是发布被明确排除的 provider 私有字段。compatibility 子包是一次性、人工控制的协议兼容性证据，其 manifest 没有 formal run 那么完整的 harness/source provenance；它通过相同 git revision、resolved-plan hash、角色与 renderer hashes 关联正式子包，不能单独承担 effect-evidence 结论。

## 对 tranche 2 的关键限制

当前 harness 要求 tranche 2 的新 resolved-plan hash 与 tranche 1 完全相同，而 resolved plan 又绑定 Git revision。本证据发布提交会使分支 HEAD 前进，因此**不能直接从发布后的 HEAD 规划/运行 tranche 2**，否则 plan hash 会变化并被 prior-run 校验拒绝。

若共同决定按原实验条件继续，无需修改 harness 或重跑 tranche 1：应从干净的独立 worktree 检出原始实验提交 `4c805561e0d3d73613291133e9bed6b5b786a484`，使用相同私有 settings/profile 和原始 tranche-1 私有目录作为 `--prior-run`，先离线验证 resolved-plan SHA 仍为 `c9ddc1d8...a9a52`，再另行取得 tranche 2 明确网络授权。不要在当前证据发布提交上“放宽”hash 校验，也不要根据本轮表现修改 cases、rubrics、variants、grader 规则或 budgets 后把结果与 tranche 1 合并。
