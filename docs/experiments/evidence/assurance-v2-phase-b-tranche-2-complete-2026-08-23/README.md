# Phase B tranche 2 逻辑运行完成证据（续跑 episode）

本目录发布 tranche 2 **逻辑运行**完成后的续跑 episode 原始证据。它与既有阻断前缀发布包合起来构成完整的 tranche 2：

```text
tranche_2（逻辑运行）
  episode 1: 阻断前缀  ed2c0c99bfa64fcea316b0deb1e9c6f3   （已发布，未被修改）
  episode 2: 续跑完成  7864a41436e74f0884aca79b88a619df   （本目录）
```

阻断前缀发布包：[`../assurance-v2-phase-b-tranche-2-2026-08-23/`](../assurance-v2-phase-b-tranche-2-2026-08-23/)。该目录**未被删除、编辑或重新解释**；其 `artifact_tree_sha256` 仍为 `ce47643c063ae1cbec8850d13eec448b334b03a7c0ff0e9681938debaed075b9`，续跑后重新计算一致。

本包不计算总分，不宣布 B0/B1/B2 胜者，也不对 repetitions 1–3 作合并解释。以下轴向数字只是候选 grader 的原始判断转录，供人工与云端联合裁决。

## 逻辑 tranche 状态

| 项 | 值 |
|---|---|
| tranche | `tranche_2`（repetitions 2 与 3） |
| 逻辑状态 | `completed` |
| records | 60（repetition 2: 30，repetition 3: 30） |
| 完成观测 | 60 |
| 未完成观测 | 0 |
| `paused_retryable` 观测 | 0 |
| secret scan | `pass`，`secret_match_files=[]` |
| 需人工裁决的分组 | 30 组中 4 组：`p003/B0`、`p003/B2`、`p012/B0`、`p012/B1` |

## 执行 episode 与续跑语义

| episode | run_id | 角色 | 状态 |
|---|---|---|---|
| 1 | `40098907d5c5452a81d8677b26a4e33c` | `prior_tranche`（tranche 1） | completed |
| 2 | `ed2c0c99bfa64fcea316b0deb1e9c6f3` | `resumed_prefix` | blocked（保持不变） |
| 3 | `7864a41436e74f0884aca79b88a619df` | `current` | completed |

续跑没有就地编辑先前 episode，而是新建 run 目录并按引用复用其不可变证据：

- 复用 generator 逻辑调用 **7** 条：`p003/B0,B1,B2 r002`、`p004/B0,B1,B2 r002`、`p005/B1/r002`；
- 复用 grader 逻辑调用 **6** 条：`p003` 与 `p004` 的 r002 三个 variant；
- 新采集 generator **53** 条、grader **54** 条；
- `p005/B1/r002` 的 generator 最终回答与 `requested_at` 与阻断 episode **逐字一致**，仅重跑其 grader，未重新生成。

复用调用在 record 与逐调用证据中带 `imported_from_episode`，指向 episode 2 的原始 evidence 路径。

## 语义与执行策略报告

```text
treatment_semantics: equivalent
execution_policy: amended
reason:
  transient transport resilience and resumability
```

model-visible treatment 在续跑前离线逐项核对，与阻断 episode 完全一致：generator base instruction、B0/B1/B2 渲染后的 system instruction、generation packets、rubrics、grading axes/schema、cases、variants、counterbalanced 顺序、tranche 划分、模型与族、参数、renderer、timeout 均未改变。generator 仍为 `deepseek-v4-flash`（provider-reported `deepseek-v4-flash-202605`），grader 仍为 `qwen3.7-plus`。

resolved-plan hash 与阻断 episode 不同（`c3deb2d1bbe33c9306aeb7fad6258873a2e5a1be132ed2dd5b820db581ae2868` 对 `c9ddc1d82f5c9b7a45481443f71ee08fb185c942638b7815e61068a62efa9a52`），原因是执行器本身经过修订并纳入 provenance。哈希是来源与完整性元数据；**字节一致不等于实验语义等价**。等价判定基于解析后的 model-visible treatment 内容，而非源文件字节哈希。已知的无害表示差异：zh-CN variants 文件中 `semantic_source.sha256` 由 CRLF 版本更新为当前 LF checkout 版本，英文 semantic source 的 JSON 内容本身未变。

runner revision：`918648adc82bb9b256b1e7049af60b8209d148d6`。

## 网络调用与重试计量

| 项 | 值 |
|---|---|
| 计划逻辑调用 | 107 |
| 完成逻辑调用 | 107 |
| 实际网络 attempt | 107 |
| 总重试次数 | 0 |
| 按角色/错误类型的重试 | 无 |

逻辑调用与网络 attempt 现在分开记账。本 episode 每个逻辑调用都在第 1 次 attempt 成功，因此 `attempt_count=1`、`retry_count=0`、`successful_attempt=1`；有界重试策略（每逻辑调用最多 3 次 attempt，退避 1s/2s）在本次未被触发。每次 attempt 仍单独 append-only 持久化在 `resumed-run/call_evidence/*__attempt_NNN.json`。

## 延迟

成功 attempt 延迟与端到端逻辑调用延迟分开保存，重试与退避时间不会混入模型推理成本。本 episode 新采集调用的成功 attempt 延迟：

| 角色 | n | 合计 ms | 中位数 ms | 最小 ms | 最大 ms |
|---|---|---|---|---|---|
| generator | 53 | 984,991.568 | 13,895.038 | 5,343.262 | 109,421.264 |
| grader | 54 | 1,208,804.902 | 21,268.725 | 15,162.290 | 34,995.781 |

generator 成功 attempt 延迟按 variant（仅描述，不构成结论）：

| variant | n | 中位数 ms | 均值 ms |
|---|---|---|---|
| B0 | 18 | 11,200.805 | 15,075.383 |
| B1 | 17 | 15,041.704 | 16,436.637 |
| B2 | 18 | 14,320.821 | 24,122.880 |

generator 保持串行并遵循 counterbalanced 顺序；grader 使用有界并行（默认 3）。因此 grader 延迟属于评估基础设施开销，不能与 generator 延迟并列解释。

## token 用量（本 episode 新采集调用）

| 角色 | prompt | completion | total | 其中 reasoning |
|---|---|---|---|---|
| generator | 18,680 | 80,880 | 99,560 | 66,337 |
| grader | 43,745 | 65,950 | 109,695 | 57,381 |

## 原始轴向判断分布（描述性）

repetitions 2 与 3 共 60 条 record，全部 `grade_parse_status=parsed`。每 variant 20 条：

| variant | applicable | not_applicable | on_time | satisfied | partial | unsatisfied | compensation yes | over-trigger low |
|---|---|---|---|---|---|---|---|---|
| B0 | 14 | 6 | 14 | 12 | 1 | 1 | 1 | 2 |
| B1 | 14 | 6 | 14 | 13 | 1 | 0 | 2 | 0 |
| B2 | 14 | 6 | 14 | 13 | 1 | 0 | 1 | 3 |

这些计数不是效果量，也不构成 variant 比较结论。完整 applicability basis、notes、精确模型可见请求与回答见逐调用文件。

## 证据索引

- [`resumed-run/resolved_plan.json`](resumed-run/resolved_plan.json)：本 episode 的完整冻结计划。
- [`resumed-run/manifest.json`](resumed-run/manifest.json)：run、角色、source、tranche scope、`execution_episodes`、`resume_from`（含语义与策略报告）、`prior_tranche_evidence`。
- [`resumed-run/run_status.json`](resumed-run/run_status.json)：`completed` 状态、网络记账、重试汇总、secret scan、artifact-tree digest。
- [`resumed-run/summary.json`](resumed-run/summary.json)：自动生成的描述性分组视图与裁决标记；不替代人工裁决。
- [`resumed-run/records/`](resumed-run/records/)：60 条 record，含复用与新采集的逻辑调用。
- [`resumed-run/call_evidence/`](resumed-run/call_evidence/)：214 份文件 = 107 条逻辑调用摘要 + 107 份逐 attempt 证据。

本 episode raw artifact-tree SHA-256：`7c402118c3e97a665c9e20141174cd379c1f4735487b255f11a624d7bc80df86`。

`resumed-run/` 是私有原始 run 的逐字副本（发布时逐文件比对，278/278 字节一致）。不得编辑其中 JSON；否则 `run_status.json` 绑定的 artifact-tree digest 会失效。

校验 digest 时请注意换行表示：本仓库没有 `.gitattributes`，在会做 CRLF 转换的 checkout 上，evidence JSON 的磁盘字节会变化，此时 artifact-tree digest 需在 **LF 归一化**后才能对上。既有的 tranche-1 `formal-run/` 与阻断 `blocked-run/` 在当前 Windows 工作副本上就属于这种情况（LF 归一化后分别精确匹配 `916e1f90...` 与 `ce47643c...`）。这是发布副本的表示差异，不是证据内容变化；权威字节仍是私有 run 目录。是否为 evidence 目录固定 LF checkout，留作联合审查时的决定。

## 解释边界

现在 repetitions 1、2、3 都有完整观测，但本包不作合并解释、不计算总分、不宣布 variant 胜者。下一步是人类与云端协作者独立审查 tranche 1、阻断前缀与本续跑 episode，共同完成联合裁决；4 个被标记分组需要优先裁决。本地 Agent 未给出效果解释。
