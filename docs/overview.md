# 人机协作规格导读

> 地位：导读，**不是**第二份事实源。当前通用规范以 [`spec/norms.md`](spec/norms.md) 为准；尚未完成拆分的历史内容见 [`norm/README.md`](norm/README.md)。

## 要解决什么问题

人与 AI 协作时，问题不只是“AI 能否完成任务”，还包括：

- 结果与行动是否有与风险相称的证据；
- 人是否仍实质掌握目的、关键判断、风险接受与最终决定；
- 双方是否把理解、同意、授权、能力和证据区分清楚；
- AI 的帮助是否根据风险、人的认知状态、压力、学习目标和任务形式调整；
- 协作机制是否降低真实成本，而不是把内部结构转嫁成人的问卷和仪式。

当前跨领域规范见 [`spec/norms.md`](spec/norms.md)。参与者、角色、权威、协作状态、抽象层、能力、证据、表示和独立性等概念区分见 [`spec/model.md`](spec/model.md)。

## 当前通用层的主要结构

当前通用规范分为四类：

1. **基础承诺**：人的目的与关键决定权、实质判断、风险与不确定性不能被便利性伪装消失；
2. **认识论约束**：证据边界、共同理解/同意/授权/能力所需的证据、来源与派生表示、独立性的实际分离；
3. **通用策略与机制**：保护承重判断、按抽象层与风险调整、反馈闭环、压力处理、学习、沟通、冲突、议程与协作状态；
4. **执行保障边界**：规范不能只依赖人的记忆、AI 当前上下文或一句提示词，但具体 Skill、状态、Hook、Agent 等只是候选载体。

## 软件开发五阶段的当前地位

旧 [`norm/02-five-phases.md`](norm/02-five-phases.md) 仍承载任务理解、实施讨论、代码实施、独立审查、复盘沉淀等软件研发场景形成的工作流材料。

它现在**不再被假定为所有人机协作的通用骨架**。后续会把可跨领域复用的“问题框定—思考/计划—行动/产出—保障/评估—反思/学习”关注点，与软件开发的具体阶段、角色、证据和技术细节分开。

在物理拆分完成前，五阶段文件仍是相关工作流内容的当前承载处，但不因位于旧 `norm/` 目录就自动成为跨领域通用规范。

## 仓库里的其他材料

- [`feedback/`](../feedback/)：实战观察与摩擦入口；
- [`insights/`](../insights/)：候选主张和设计解释；
- [`skills/`](../skills/)：实验性 Skill 载体与行为 eval；
- [`human-ai-collaboration-reference-study.md`](human-ai-collaboration-reference-study.md)：保障机制研究与取舍；
- [`human-ai-collaboration-v1-implementation.md`](human-ai-collaboration-v1-implementation.md)：早期保障形式实验；
- [`governance/project-evolution.md`](governance/project-evolution.md)：项目如何从观察形成、验证、重分类和维护当前知识。

## 常见误解

| 误解 | 当前立场 |
| --- | --- |
| 这是必须安装的一套 Skill / Agent 规则 | 否。规格是根本；Skill 等只是载体或保障实验 |
| 五阶段是所有人机协作必须采用的流程 | 否。它是软件研发形成的工作流实现，正在与通用层拆分 |
| 模板逐项填写才算合规 | 否。表示与提问应服务当前任务，不把内部结构成本转嫁给人 |
| AI 自审等于独立审查 | 否。独立性的证明力取决于与相关失效来源的实际分离 |
| 测试全绿等于风险消失 | 否。证据只能证明它实际覆盖的断言和失效模式 |
| 任务成功等于人的独立能力或协作机制已经被验证 | 否。任务结果、人的能力、协作能力与载体运行表现需要分开解释 |

## 下一步读什么

- 先读 [`spec/README.md`](spec/README.md) 与 [`spec/norms.md`](spec/norms.md)；
- 需要概念边界时读 [`spec/model.md`](spec/model.md)；
- 需要维护项目或理解反馈如何进入规格时读 [`governance/project-evolution.md`](governance/project-evolution.md)；
- 需要当前尚未拆分的工作流、机制或模板时，再进入 [`norm/README.md`](norm/README.md)。
