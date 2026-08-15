# 人机协作规范正文

> 地位：**规范权威正文**（由 `workflow` v0.15 重组并持续校准）。  
> 导读：[../overview.md](../overview.md)  
> 重组前快照：[../archive/workflow-v0.15.md](../archive/workflow-v0.15.md)

本目录承载「理想的人机协作应满足什么」。通用协作规范与特定领域工作流需要分层表达；执行保障的具体技术形态（Skill、子代理、`AGENTS.md`、任务胶囊、记忆或恢复设施等）不是规范本身，相关探索见仓库中的研究与实施笔记。

当前文档仍包含从软件研发实践形成的五阶段工作流和若干工程化表达，后续将继续按「通用协作规范 → 可复用工作流/机制 → 领域扩展 → 执行保障」的方向审查和重组；在完成迁移前，各章正文仍按其明确地位解释，不能因为文件顺序推断所有内容处于同一抽象层。

## 阅读顺序

| 顺序 | 文件 | 内容 |
| --- | --- | --- |
| 1 | [00-purpose-and-principles.md](00-purpose-and-principles.md) | 通用目标；基础承诺；认识论约束；通用策略与机制；执行保障边界 |
| 2 | [01-roles-and-abstraction.md](01-roles-and-abstraction.md) | 角色；抽象层 L0–L4；掌握层次 M0–M5（待继续审查通用层与领域层边界） |
| 3 | [02-five-phases.md](02-five-phases.md) | 任务理解 → 实施讨论 → 代码实施 → 独立审查 → 复盘（工程/执行型工作流，待继续定位） |
| 4 | [03-cognitive-mechanisms.md](03-cognitive-mechanisms.md) | 预测、压力模式、认知包、诊断、审查面、冲突、验证等（含通用机制与待拆分内容） |
| 5 | [04-templates.md](04-templates.md) | 可裁剪模板（附录性质，按风险选用） |
| 6 | [05-antipatterns-and-boundaries.md](05-antipatterns-and-boundaries.md) | 反模式、科学表述边界、精简参考资料 |
| 附录 | [decisions.md](decisions.md) | 文档状态与历史决策记录（追溯用；历史决策不自动等于当前规范层级） |

## 执行保障边界

原 §10「执行保障机制与试点」已归档至 [../archive/assurance-and-pilot-notes-from-workflow-v0.15.md](../archive/assurance-and-pilot-notes-from-workflow-v0.15.md)。

规范保留「不能只依赖人的记忆、AI 上下文或软性约定，需要可观察、可检查、可恢复的执行保障」这一**需求**，但不预设 Skill、状态文件、会话恢复、子代理、Hook 或其他具体实现形式。载体与保障系统应根据规范对象、失效模型和真实运行证据另行设计。
