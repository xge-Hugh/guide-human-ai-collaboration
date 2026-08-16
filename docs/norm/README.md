# 旧规范目录：迁移中

> 本目录正在迁往 [`../spec/`](../spec/README.md)。不要把本目录整体继续理解成一个同层级的“规范正文”。
>
> 项目的当前分类与演进方法见 [`../governance/project-evolution.md`](../governance/project-evolution.md)。
>
> 重组前快照：[../archive/workflow-v0.15.md](../archive/workflow-v0.15.md)

## 权威边界

迁移期间不维护两份并列权威：

- 原 Chapter 00 已完成全文迁移到 [`../spec/norms.md`](../spec/norms.md)，旧路径只保留兼容跳转；
- [`../spec/model.md`](../spec/model.md) 已承载参与者/角色/权威、协作状态、抽象层与能力、证据/表示/独立性等当前概念区分；
- Chapter 01/02 的**通用语义与领域定位**已分别提炼到 [`../spec/evaluation.md`](../spec/evaluation.md)、[`../spec/workflows.md`](../spec/workflows.md) 与 [`../spec/domains/software-development.md`](../spec/domains/software-development.md)；但旧文件仍暂时保留部分更细的操作文本，完成逐项核对前不删除；
- Chapter 03–05 尚未完成物理拆分，必须结合本表解释其语义地位；
- [`decisions.md`](decisions.md) 仍为历史决策与状态记录，主张以当前正文为准；后续将迁往治理层。

## 旧文件的当前作用

| 文件 | 当前解释 |
| --- | --- |
| [01-roles-and-abstraction.md](01-roles-and-abstraction.md) | 迁移源与历史详细展开；通用概念/评估语义已在 `spec/` 重述，角色与 L0–L4 已作为软件专项解释；待核对剩余细节后转兼容入口 |
| [02-five-phases.md](02-five-phases.md) | 迁移源与软件五阶段详细操作文本；通用关注点已进入 `spec/workflows.md`，专项结构已进入 `spec/domains/software-development.md`；待核对后转兼容入口 |
| [03-cognitive-mechanisms.md](03-cognitive-mechanisms.md) | 历史混合章节：通用机制、状态估计、评估、策略/配方、信息架构与工程专项；已完成语义审查，待物理拆分 |
| [04-templates.md](04-templates.md) | 操作载体/指导性质模板；待迁入 guidance 层 |
| [05-antipatterns-and-boundaries.md](05-antipatterns-and-boundaries.md) | 失效表现、项目证据边界与研究引用混合；待拆分 |
| [decisions.md](decisions.md) | 历史决策与项目状态；追溯用，不自动等于当前规范层级 |

## 执行保障边界

当前通用规范仍保留“不能只依赖人的记忆、AI 上下文或软性约定，需要可观察、可检查、可恢复的执行保障”这一需求，但不预设 Skill、状态文件、会话恢复、子代理、Hook 或其他具体实现形式。载体与保障系统应根据规范对象、失效模型和真实运行证据另行设计。
