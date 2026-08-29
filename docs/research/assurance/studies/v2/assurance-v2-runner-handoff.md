# 执行保障 v2：本地 Runner 实施交接契约

> 地位：**实验实施交接，不是规范正文，也不是正式保障架构。**  
> Phase B 协议：[`assurance-v2-phase-b-protocol.md`](assurance-v2-phase-b-protocol.md)  
> 生成包：[`assurance-v2-phase-b-generation.json`](assurance-v2-phase-b-generation.json)  
> 隐藏 rubric：[`assurance-v2-phase-b-rubrics.json`](assurance-v2-phase-b-rubrics.json)  
> B0/B1/B2 变量：[`assurance-v2-phase-b-variants.json`](assurance-v2-phase-b-variants.json)
>
> 目的：把 Phase B 的受控回放变成一个**最小、可重复、可审查的本地实验仪器**。它服务当前实验并允许后续复用，但不预建通用 AI eval 平台，也不取得规范权威。

## 1. 三方协作角色

### 人：实验负责人和规范性裁决者

人负责会改变实验目标、证据解释、成本/隐私边界或项目方向的判断，例如：

- 允许使用哪些 API / 模型与可接受成本；
- 是否接受扩大实验范围或改变主要变量；
- 对 grader 分歧、`derived` 案例和会改变结论的边界作最终裁决；
- 是否把某次实验结果升级为后续生态试跑或机制选择的依据。

人**不需要**亲自决定普通 Python 工程细节，除非该细节会改变实验含义。

### 本地 AI Agent：实现者和本地运行者

本地 Agent 负责：

- 检查当前仓库和本地 Python/API 环境；
- 提出并实现最小 runner；
- 处理依赖、CLI、provider 适配、mock/fake provider、测试和本地运行；
- 从本地环境变量或未跟踪配置读取凭据；
- 保存原始运行证据和元数据；
- 在独立分支提交变更，并在大规模付费实验前停下来接受审查。

本地 Agent 不得把实现方便自动升级为实验设计决定，也不得修改当前规范以适配 runner。

### 云端审查 Agent：规格/实验与证据审查

云端审查负责：

- 检查实现是否忠实执行当前 Phase B 协议；
- 检查 rubric 泄漏、变量污染、上下文未隔离、原始输出被改写等证据风险；
- 检查 B0/B1/B2 是否只按既定变量不同；
- 检查记录和汇总是否超出证据边界；
- 将真正需要人裁决的分歧与普通实现问题分开。

这里的“三方协作”本身**不自动等于实验评价独立性**。grader 的独立性仍按 Phase B 协议另行判断。

## 2. Runner 的项目位置与边界

默认建议在仓库内建立一个小型、明确标记为实验工具的目录，例如：

```text
tools/assurance_eval/
```

具体 Python 包布局可由实现者按仓库实际情况选择；若要改为其他顶层位置，应说明它为什么能降低维护/权威混淆，而不是仅因个人偏好。

Runner 应直接读取 `docs/research/assurance/studies/v2/` 中已有的 generation / rubric / variant 文件，不复制其中的实验语义为另一套硬编码真相。

第一版明确**不做**：

- 通用评测平台或 Web 服务；
- Dashboard、数据库、队列或分布式执行；
- Hook、工作流引擎、长期记忆或用户画像；
- 多 Provider 的完整抽象层；
- 自动选择最终保障机制；
- 把全部轴压成一个总分；
- 自动把实验结果写回规范。

## 3. 第一版必须支持的能力

Runner v0 必须能够：

1. 选择一个或多个 Phase B generation case；
2. 对同一 case 运行 B0/B1/B2 中指定的 variant；
3. 为每个 `case × variant × repetition` 使用干净、等价的新上下文；
4. 配置一个真实 generator provider/model；
5. 提供一个 fake/mock provider，使实验管线可在不调用付费 API 的情况下测试；
6. 保存实际发送给 generator 的请求材料（秘密除外）；
7. 原样保存 generator 的原始输出，不用摘要替换；
8. 在独立调用路径构造 grader packet，并保证 generator 看不到 hidden rubric / expected behavior；
9. 保存逐轴 grader 结果，而不是只保存总分；
10. 记录足以复现/解释运行的元数据；
11. 能重复运行同一实验配置；
12. 生成一个简单、可检查的汇总，但保留原始记录可回查。

## 4. 最低运行元数据

每次实际模型调用至少记录：

- run / case / variant / repetition 标识；
- provider；
- 实际 model ID / snapshot / alias；
- 已设置的采样、reasoning 或等价参数；
- 无法控制的平台参数；
- 请求时间；
- runner 的 Git revision；
- generation / variants / rubrics 的文件 revision 或内容摘要；
- 调用是否成功、错误/重试事实；
- 原始模型输出。

API key、token、密码等秘密不得进入日志、运行 artifact 或 Git。

## 5. 证据隔离不变量

以下条件属于 runner 正确性的实验不变量：

### 5.1 Generator 不得看到答案

Generator 输入不得包含：

- hidden rubric；
- `expected_behavior`；
- Phase A 的适用结论；
- FM 编号或“正在测试什么”的提示。

### 5.2 B0/B1/B2 只改变既定实验变量

同一 case 的任务上下文、用户消息、模型和运行参数必须保持等价；不得让 B2 同时获得额外任务事实、工具或历史状态。

### 5.3 Grader 与 generator 路径分离

Grader 可以看到规范/rubric 与原始输出，但不能修改 generator 的结果。若使用同一模型作为 grader，必须按 Level 1 而不是“独立验证”表述。

### 5.4 原始证据优先

任何 summary、评分或人工备注都必须能回查到原始 request/response。后处理不能覆盖原件。

## 6. 实现者可以自主决定什么

在不改变第 3～5 节实验语义的前提下，本地 Agent 可以自主决定：

- Python 版本的合理下限；
- 包管理/虚拟环境工具；
- CLI 框架或标准库实现；
- dataclass / pydantic / TypedDict 等内部表示；
- 文件拆分和普通模块命名；
- 日志库、HTTP SDK 和测试框架；
- 普通错误处理、退避和本地开发体验；
- 结果目录的具体文件命名。

这些决定应保持轻量，并尽量使用成熟、少依赖的做法。

## 7. 必须升级给人/审查的决定

下列变化不得由本地 Agent 静默决定：

- 改写 B0/B1/B2 的语义；
- 改写 Phase A case 的适用边界或 rubric；
- 增加新的主要实验变量；
- 同时引入跨会话 profile、状态、Hook 或工具执行；
- 取消 generator / grader 信息隔离；
- 为了方便实现而改变“干净上下文”要求；
- 自动把 grader 输出视为最终事实；
- 建立会改变隐私/长期存储边界的基础设施；
- 运行明显超出 smoke test 的付费批量实验；
- 选择会显著改变成本或证据解释的 provider/model 配置；
- 将 runner 提升为正式保障产品/架构。

遇到这类问题时，应记录：`问题 → 为什么现有协议无法决定 → 可选方案 → 实验/维护影响 → 推荐`，再升级裁决。

## 8. 实施阶段与审查点

### Stage 0：只读检查与方案

本地 Agent 先读取当前 `main`、本文件和 Phase B 协议，确认当前仓库没有可直接复用的 runner，然后提出：

- 最小目录/模块结构；
- 第一 Provider 的接入建议，但不立即绑定；
- fake provider 方案；
- 测试策略；
- 发现的任何需要升级的实验设计问题。

若无实验性分歧，可继续实现普通工程细节，不需要人逐项批准。

### Stage 1：Mock 管线

先实现不用真实 API 也能证明以下管线的测试：

- case/variant 载入正确；
- B0 不收到 B1/B2 内容；
- generator 不收到 rubric；
- 不同 repetition 形成独立记录；
- grader packet 正确构造；
- raw output 保留；
- summary 不覆盖逐次结果。

### Stage 2：真实 API smoke test

只选择极少 case/variant/repetition 验证：

- 认证与 provider adapter 正常；
- model/parameter 元数据真实记录；
- 请求/响应可回查；
- 错误和重试不会破坏运行记录。

Smoke test 不用于判断 B0/B1/B2 哪个更好。

### Stage 3：Phase B 小规模正式运行

只有 Stage 1/2 经审查后才运行预先同意的首批 case × B0/B1/B2 × repetition。结果先保持逐轴和逐次可检查，再形成实验解释。

## 9. 第一版验收边界

Runner v0 可以被认为“足以进入 Phase B 小规模运行”，需要同时满足：

- mock 测试证明主要信息隔离和变量隔离；
- 至少一个真实 provider 完成 smoke test；
- 原始 request/response 与元数据可回查；
- generator 和 grader 路径实际分离；
- 同一配置可以重复执行；
- 没有把 rubric / expected 泄漏给 generator；
- 没有把 runner 结构成功误写成保障机制已经可靠；
- 没有出现需要人裁决却被实现者静默决定的实验设计变化。

代码风格、模块数量或“看起来像成熟框架”不是验收标准。

## 10. 本地 Agent 的启动指令

本地 Agent 可直接从本文件启动。其第一条工作指令应理解为：

> 在当前仓库中实现 Phase B 的最小本地受控回放 runner。先读取本交接契约和相关 Phase B 文件；保持规范、case、rubric 和 B0/B1/B2 语义不变。先完成只读检查与最小方案，再实现 fake-provider 驱动的管线和测试。不要运行大规模付费实验。若遇到会改变实验意义、成本/隐私边界或规范解释的问题，停止该决定并形成短的升级说明；普通 Python 工程细节可自行处理。

建议所有实现先在独立分支完成，并通过 GitHub PR/branch diff 作为三方协作的共享可观察面。
