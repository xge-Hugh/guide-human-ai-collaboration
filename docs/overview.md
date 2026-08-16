# 人机协作规格导读

> 地位：导读，**不是**第二份事实源。当前通用规范以 [`spec/norms.md`](spec/norms.md) 为准；迁移状态见 [`spec/README.md`](spec/README.md)。

## 要解决什么问题

人与 AI 协作时，问题不只是“AI 能否完成任务”，还包括：

- 结果与行动是否有与风险相称的证据；
- 人是否仍实质掌握目的、关键判断、风险接受与最终决定；
- 双方是否把理解、同意、授权、能力和证据区分清楚；
- AI 的帮助是否根据风险、人的认知状态、压力、学习目标和任务形式调整；
- 协作机制是否降低真实成本，而不是把内部结构转嫁成人的问卷和仪式。

当前跨领域规范见 [`spec/norms.md`](spec/norms.md)。参与者、角色、权威、协作状态、抽象层、能力、证据、表示和独立性等概念区分见 [`spec/model.md`](spec/model.md)。

## 当前规格的主要视图

- **通用规范**：[`spec/norms.md`](spec/norms.md) —— 必须保护的权威、认识论边界与通用机制；
- **概念模型**：[`spec/model.md`](spec/model.md) —— 用什么维度描述协作；
- **自适应模型**：[`spec/adaptation.md`](spec/adaptation.md) —— 风险、压力、熟悉程度、目标与协作状态如何调节投入；
- **评估模型**：[`spec/evaluation.md`](spec/evaluation.md) —— 任务结果、人的能力、协作能力和载体运行表现如何分开解释；
- **工作流模型**：[`spec/workflows.md`](spec/workflows.md) —— 问题框定、思考/计划、行动/产出、保障/评估、反思/学习等可复用关注点；
- **失效模型**：[`spec/failure-models.md`](spec/failure-models.md) —— 在什么条件和机制下协作会失去规范保护或预期价值；
- **软件开发专项**：[`spec/domains/software-development.md`](spec/domains/software-development.md) —— 软件研发角色、L0–L4、五阶段和具体证据实践。

## 软件开发五阶段的当前地位

软件五阶段现在被明确定位为**领域专项工作流**，不是所有人机协作的通用骨架。其通用来源被抽取为：

```text
问题框定
→ 思考 / 计划
→ 行动 / 产出
→ 保障 / 评估
→ 反思 / 学习
```

不同领域可以改变阶段数量、名称、产物和证据，只要不覆盖通用规范。旧 [`norm/02-five-phases.md`](norm/02-five-phases.md) 暂时继续保留更细的历史操作文本，完成逐项迁移核对后再转为兼容入口。

## 仓库里的其他材料

- [`feedback/`](../feedback/)：实战观察与摩擦入口；
- [`insights/`](../insights/)：候选主张和设计解释；
- [`skills/`](../skills/)：实验性 Skill 载体与行为 eval；
- [`guidance/`](guidance/README.md)：可替换的交互、表示与模板方法；
- [`research/`](research/README.md)：保障机制研究与外部依据；
- [`experiments/`](experiments/README.md)：历史保障形式实验与试点；
- [`governance/`](governance/README.md)：项目演进、证据政策与历史决策。

## 常见误解

| 误解 | 当前立场 |
| --- | --- |
| 这是必须安装的一套 Skill / Agent 规则 | 否。规格是根本；Skill 等只是载体或保障实验 |
| 五阶段是所有人机协作必须采用的流程 | 否。它是软件开发专项的一种工作流实现 |
| M0–M5 是人的永久等级 | 否。当前评估模型只把它保留为特定情境下可观察证据的历史表达，不是身份标签 |
| 模板逐项填写才算合规 | 否。表示与提问应服务当前任务，不把内部结构成本转嫁给人 |
| AI 自审等于独立审查 | 否。独立性的证明力取决于与相关失效来源的实际分离 |
| 测试全绿等于风险消失 | 否。证据只能证明它实际覆盖的断言和失效模式 |
| 任务成功等于人的独立能力或协作机制已经被验证 | 否。任务结果、人的能力、协作能力与载体运行表现需要分开解释 |

## 下一步读什么

- 先读 [`spec/README.md`](spec/README.md) 与 [`spec/norms.md`](spec/norms.md)；
- 需要概念边界时读 [`spec/model.md`](spec/model.md)；
- 需要能力/协作评价时读 [`spec/evaluation.md`](spec/evaluation.md)；
- 需要任务推进结构时读 [`spec/workflows.md`](spec/workflows.md)，软件开发再读 [`spec/domains/software-development.md`](spec/domains/software-development.md)；
- 需要维护项目或理解反馈如何进入规格时读 [`governance/project-evolution.md`](governance/project-evolution.md)；
- 需要研究依据或历史保障实验时读 [`research/`](research/README.md) 与 [`experiments/`](experiments/README.md)；
- 需要核对尚未完全迁出的历史细节时，再进入 [`norm/README.md`](norm/README.md)。
