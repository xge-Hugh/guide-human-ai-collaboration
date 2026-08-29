# 保障形式实验笔记（v1）

> 地位：**保障形式实验，不是规范正文。**  
> 规范主张：[overview.md](overview.md) · [norm/](norm/README.md)  
> 机制来源与取舍：[human-ai-collaboration-reference-study.md](human-ai-collaboration-reference-study.md)  
> 保障需求与早期观察：[archive/assurance-and-pilot-notes-from-workflow-v0.15.md](archive/assurance-and-pilot-notes-from-workflow-v0.15.md)  
> 试点证据：[../tasks/archive/out-webapi-batch/](../tasks/archive/out-webapi-batch/)
>
> 状态：试点已结束；本文保留设计与修订记录，供以后决定「是否 / 如何」做成可用形式时对照。  
> 日期：2026-08-09（试点）；2026-08-10（迁入本仓库并规范化导航）

**一句话**：曾用最小的 `AGENTS.md + Skill + 任务胶囊` 把规范试跑成行为；这是价值验证，不是已选定的产品形态。

## 阅读地图

| 你想了解 | 去哪 |
| --- | --- |
| 规范本身主张什么 | [norm/](norm/README.md) |
| 为什么要做保障、早期问题清单 | [assurance 笔记](archive/assurance-and-pilot-notes-from-workflow-v0.15.md) |
| 社区机制怎么筛、哪些自研 | [reference-study](human-ai-collaboration-reference-study.md) |
| 试点里试了什么栈、结果如何 | **本文**（先看下方结论表，再按需下钻） |
| Skill 源码（实验载体） | [../skills/](../skills/README.md) |

## 试点结论速览

| 类别 | 内容 |
| --- | --- |
| 已证实 | 任务文件夹 + 小状态能恢复目标/阶段/行动者/下一步；最小上下文与自然提问降低阅读负担；人能在业务与架构边界上作承重判断 |
| 已暴露失效 | 静默长审查；架构文档变流水账；AI 单方复盘并关单；「凭直觉」审查缺上下文；测试全绿仍漏真实请求；状态 schema / `current_actor` 语义曾混乱 |
| v1.1 已改（Skill 侧） | 审查/复盘参考独立成篇；风险—证据匹配；成熟模式检查；行为 eval；状态 schema 与初始化规则 |
| 仍开放 | 常驻底线清单；共同航标的**呈现形式**；本仓库是否把 Skill/`AGENTS` 定为正式可用形态；脚本/Hook 是否值得加 |

当前主要失效仍是语义与阶段行为，不是 JSON 格式错误；**暂不**因「技术上可以」加脚本。

---

## 1. 实验目标

用最小的 `AGENTS.md + Skill + 任务胶囊` 组合，把已经形成的人机协作规范转化为可试运行行为，并验证它是否：

- 降低长对话中的方向丢失和恢复成本；
- 减少长文、问卷、重复澄清和不必要决策；
- 保留人的独立判断、学习机会和可观察贡献；
- 不显著拖慢 Batch 重构的业务交付；
- 在失效时能够低成本停用或删除。

v1 是价值验证，不是通用治理平台。

## 2. 当时事实与约束（CRM 试点期）

下列路径与所有权描述的是 **2026-08 SUNWARD CRM / Codex 试点环境**，不是本仓库的产品承诺：

- 两层规则入口：个人全局 `/home/xge/.codex/AGENTS.md`；仓库根未跟踪的 `AGENTS.md` 作试运行触发。首版不改全局入口。
- Skill 安装在 `/home/xge/.codex/skills/guide-human-ai-collaboration`。曾评估迁移到产品无关的 `$HOME/.agents/skills`；仓库级 `.agents/skills` 不符合跨项目作用域设想。
- 历史 Changeset 文档不能完整代表后来的「普通 Batch + 原子变体」目标。
- 工作流与研究当时为个人、未跟踪资产，不作为 CRM 团队规范。
- 首版不碰业务编译/测试/交付，不加 Hook、MCP、Plugin、数据库、后台服务或跨产品同步。

### 2.1 迁入本仓库后的对应关系

| 试点期位置 | 本仓库当前位置 |
| --- | --- |
| 完整工作流单文件 | [norm/](norm/README.md)（正文）+ [archive/workflow-v0.15.md](archive/workflow-v0.15.md) |
| 参考研究 / 本实施设计 | `docs/human-ai-collaboration-*.md`（本文与 study） |
| `.agents/tasks/out-webapi-batch/` | [tasks/archive/out-webapi-batch/](../tasks/archive/out-webapi-batch/) |
| Codex 个人 Skill | 源码镜像：[skills/guide-human-ai-collaboration/](../skills/guide-human-ai-collaboration/)（实验载体，非安装入口） |

## 3. 最小架构（实验栈）

```text
AGENTS 入口片段
  └─ 判断是否启用协作 Skill
        └─ guide-human-ai-collaboration/SKILL.md
             ├─ 按当前情境读取一个参考文件
             └─ 读取/更新当前任务胶囊
                    ├─ 指向稳定任务或实施文档
                    └─ 输出共同航标
```

四类信息只保留一个主要归属：

| 信息 | 主要归属 | 生命周期 |
| --- | --- | --- |
| 少数常驻底线与触发条件 | AGENTS 入口 | 跨任务稳定 |
| 可执行协作方法 | Skill 及 references | 跨任务演进 |
| 设计依据、研究和完整规范 | 规范正文与研究笔记 | 长期参考，不默认加载 |
| 当前目标、阶段和下一步 | 任务胶囊 | 单个任务，频繁但小幅更新 |

## 4. 文件结构

### 4.1 试点期布局（历史）

```text
/home/xge/.codex/skills/
└─ guide-human-ai-collaboration/
   ├─ SKILL.md
   ├─ agents/openai.yaml
   ├─ evals/evals.json
   └─ references/
      ├─ phases.md
      ├─ interaction-and-learning.md
      ├─ review-and-retrospective.md
      └─ state-conflict-and-recovery.md

<CRM 仓库根>/.agents/
├─ human-ai-collaboration-workflow.md
├─ human-ai-collaboration-reference-study.md
├─ human-ai-collaboration-v1-implementation.md
└─ tasks/
   └─ out-webapi-batch/
      ├─ state.json
      ├─ task.md
      ├─ architecture.md
      └─ …（按需 evidence / review / retrospective）
```

当时约定：不创建安装指南、变更日志、模板集合或辅助应用；不含 `scripts/` / `assets/`；`evals/` 只保存真实失效的行为回归，不复制规范正文。CRM 侧资产刻意未 Git 跟踪，避免误入团队提交。

### 4.2 本仓库布局（规范优先雏形）

见根 [README.md](../README.md)。规范正文在 `docs/norm/`；Skill 与任务胶囊降级为实验/证据，**不是**当前产品入口。

## 5. AGENTS 入口（实验设计）

### 5.1 职责

1. 指出何时使用协作 Skill；
2. 禁止静默替换已确认的目标和业务不变量；
3. 指出任务状态只辅助恢复由当前请求和对话确定的任务。

候选片段：

```markdown
## Human-AI Collaboration Pilot

- Use `$guide-human-ai-collaboration` when a development task spans multiple phases, clearly matches an active collaboration state, or explicitly includes a learning goal. Skip it for simple factual answers and low-risk mechanical edits unless the user invokes it.
- Never silently replace a confirmed goal, business invariant, or current next step. Surface material conflicts and reconcile them with the user in proportion to risk.
- Treat `*-collaboration-state.md` as recoverable task state, not as authority over newer user-confirmed decisions.
- Determine the current task from the user’s request and the conversation’s latest unfinished shared next step; active state only helps recover it.
```

这是比 Skill 更常驻的指令约束，但仍不是确定性硬门禁。

### 5.2 部署边界（试点期）

- 个人全局 `AGENTS.md` 不增加新协作规则；
- 仓库根未跟踪 `AGENTS.md` 只加短触发片段；
- Skill 装个人目录，任务胶囊与 Batch 文档放仓库 `.agents/`，匹配不同生命周期；
- 两层入口不重复维护同一规则。

## 6. Skill 设计（实验设计）

### 6.1 名称与触发

- 名称：`guide-human-ai-collaboration`
- 显式触发：用户点名 Skill，或要求按人机协作规范推进；
- 隐式触发：跨多阶段；存在匹配活动胶囊；明确学习目标；
- 跳过：简单事实、只读查询、低风险机械修改，以及启用后成本明显高于收益的任务。

试点优先显式启用，再观察隐式触发，避免把「是否触发」和「触发后是否有效」混成一个问题。

### 6.2 `SKILL.md` 只保留的内容

1. 读取活动任务胶囊和当前阶段需要的稳定文档；
2. 从自然表达中提取信息，不要求人填写模板；
3. 默认最小充分回答，一轮一个主要问题；
4. 按风险决定确认、反对、实施和验证强度；
5. 在阶段转换、分叉、恢复和高影响行动前显示共同航标；
6. 只在重大状态变化时更新任务胶囊；
7. 完成时分别结算结果、证据、人的贡献和剩余未知；
8. 按情境选择一个 reference，不预读全部材料。

不复述完整科学依据、全部反模式、长模板或社区研究。

### 6.3 按需参考

| 文件 | 何时读取 | 主要内容 |
| --- | --- | --- |
| `phases.md` | 进入或退出任务阶段时 | 五阶段最低产物、退出信号、快速通道 |
| `interaction-and-learning.md` | 不理解、主动学习、认知负担或刻意练习时 | 解释梯度、自然表达、预测、学习插槽、自我效能 |
| `state-conflict-and-recovery.md` | 恢复、压缩、目标冲突、优先级分叉时 | 权威层次、冲突协调、航标与胶囊更新 |
| `review-and-retrospective.md` | 独立审查、设计验证、人审代码或复盘时 | Reviewer 隔离、风险—证据、审查脚手架、交互式复盘 |

源码见 [../skills/guide-human-ai-collaboration/](../skills/guide-human-ai-collaboration/)。

## 7. 文档受众与人类审查面

任务/实施/证据文档主要服务 AI 执行、恢复与独立审查；不能要求人通读长文，也不能把「文件已生成」当成已批准。完整文档须可追溯、可抽查。

人的默认审查面只含：目的与不变量；本轮承重决定；重大风险/未知；待裁决事项；唯一下一步及正文链接。优先作为对话视图或权威文档小节，**不**另建会漂移的摘要事实源。

规范正文中的对应原则见 [横切机制 · 文档受众与审查面](norm/03-cognitive-mechanisms.md#文档受众与审查面)。

## 8. 任务目录与控制状态

试点目录：`.agents/tasks/out-webapi-batch/`（现已归档至本仓库 `tasks/archive/out-webapi-batch/`）。

- `state.json`：标识、生命周期、阶段、行动者、唯一下一步、模式、文档/债务引用；
- `task.md`：目的、范围、不变量、成功观察、学习目标；
- `architecture.md`：心智模型、决定、理由、风险、验证方法（**不**写逐轮流水）；
- `evidence.md` / `review.md` / `retrospective.md`：仅在有跨会话交接价值时创建。

### 8.1 更新条件

仅在生命周期/阶段/行动者/下一步改变，压力或学习模式改变，权威文档/阻塞/债务引用改变，或交接、恢复、阶段结算时更新。目标与决定写 Markdown；聊天流水不入库。

### 8.2 权威关系

人的最新明确确认 > 稳定任务文档 > 实施文档 > 胶囊索引。冲突记录来源与取代关系，不自动「最新胜出」或「最初冻结」。

## 9. 首轮运行方式（历史计划）

### 9.1 起点

从已有讨论生成胶囊，短复述暴露推断；仅会改变方向的内容才确认。

### 9.2 第一观察段范围

恢复任务 → 业务层 Batch/Changeset 公共契约的实施讨论 → 可独立判断的心智模型与实施文档 → 阶段边界轻量结算。通过后再延到编码、审查、复盘。

### 9.3 正向信号 / 9.4 失效信号

正向：无需重读长史即可说出目标与下一步；能审承重决定；无问卷化；能解释 Batch/Changeset 边界；取舍能指出人的判断与证据；产物不膨胀；学习未拖垮主线。

失效：简单消息反复触发；每轮弹航标；胶囊复制正文；强迫填表；任务成功误当掌握；方向仍丢；旁支无独立状态；文档维护成本超过收益；形式化通读批准。

## 10. 退出、降级与增强

- **降级**：关隐式触发；删长 references；缩胶囊；应急只留不变量/风险/债务。  
- **停用**：移除 AGENTS 片段即可；Skill/胶囊为可读文件，不改业务代码。  
- **增强脚本/Hook**：仅在状态不一致、压缩漏载、忘记更新等**可重复**失效后考虑。

## 11. 实施与验证顺序（历史）

AGENTS 片段 → Skill 与 references → Batch 胶囊 → 前向场景检查 → 按摩擦删减。验收看协作行为与成本，不看「文件是否齐全」。

## 12. Batch 试点结果与 v1.1 修订

### 12.1 已证实的收益

- 任务文件夹和小状态能够恢复目标、阶段、行动者和唯一下一步；
- 任务理解与实施讨论中的最小上下文、代表性例子和自然提问明显降低了人的阅读负担；
- 人能够在业务语义、架构边界和结果消费方式上作出承重判断，并发现便利 API 泄漏通用嵌套模型的问题。

### 12.2 已暴露的失效

- 实施完成后 AI 静默进入长时间独立审查，人没有选择审查方式，也没有获得代码参与或学习插槽；
- `architecture.md` 吸收逐轮进展、验证和复盘，逐渐成为流水日记；
- AI 单方面生成「复盘」并把状态标记为完成，人没有参与，也没有收到即时复盘结论；
- 人被要求「凭直觉」判断设计，却未必知道上一轮完成了什么；
- 数百个单元测试通过仍未发现真实请求问题，暴露测试数量与失效边界不匹配；
- 状态生命周期缺少完整 schema，`current_actor` 与 `next_action` 的职责描述曾互相冲突。

### 12.3 修订内容

1. 新增 `review-and-retrospective.md`；
2. 约定复盘时，人未参与或明确跳过前不得单方关单；
3. 审查前区分 Builder 自检与独立 Reviewer，协作方式变化时保留人的选择权；
4. 验证改为「变化—失效模式—业务后果—证据缺口」；
5. 五阶段增加按风险触发的借鉴—适配—自研检查；
6. 增加小型行为 eval；
7. 状态参考增加最小 schema 与生命周期事件；`current_actor` = 恢复后下一行动者；
8. 按实际阶段初始化；不可持久化时显式降级为对话航标。

### 12.4 当前不增加脚本的理由

主要失效仍是语义判断和阶段行为；JSON/迁移机械错误尚未重复到足以证明脚本收益。

## 13. 对本仓库的含义（2026-08-10）

1. **规范正文**已独立可读；本文只解释「曾经怎么保障、试出了什么」。  
2. 是否把 Skill / `AGENTS` / 胶囊定为正式形态，**尚未决定**。  
3. 已知体验债示例：共同航标「目标 → 阶段 → 下一步」意图对、呈现可改进——适合在 GitHub 上以 Issue 跟踪（推送仓库后处理）。  
4. 下一步默认：远程发布本仓库 → 用 Issue 收集呈现与形态反馈 → 再议「可用形式」设计。
