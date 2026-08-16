# 旧规范目录：迁移中

> 本目录正在迁往 [`../spec/`](../spec/README.md)、[`../guidance/`](../guidance/README.md) 与 [`../governance/`](../governance/README.md)。不要把本目录整体继续理解成一个同层级的“规范正文”。
>
> 重组前快照：[../archive/workflow-v0.15.md](../archive/workflow-v0.15.md)

## 权威边界

迁移期间不维护两份并列权威：

- 原 Chapter 00 已完成全文迁移到 [`../spec/norms.md`](../spec/norms.md)，旧路径只保留兼容跳转；
- Chapter 01/02 的通用语义与领域定位已提炼到 `spec/model.md`、`spec/evaluation.md`、`spec/workflows.md` 与软件开发专项；旧文件仍暂时保留更细操作文本；
- Chapter 03 的通用自适应语义已进入 `spec/adaptation.md`，交互/表示配方已进入 `guidance/`，评估语义已由 `spec/evaluation.md` 承接；旧章仍保留尚未逐项迁完的详细展开；
- Chapter 04 的模板已重述为 [`../guidance/templates.md`](../guidance/templates.md) 的可裁剪操作载体；旧文件暂保留历史模板原貌；
- Chapter 05 的反模式已经按条件与机制提炼到 [`../spec/failure-models.md`](../spec/failure-models.md)，项目自身的科学/经验主张边界已进入 [`../governance/evidence-policy.md`](../governance/evidence-policy.md)；旧文件仍保留参考资料与尚未逐项核对的原始反模式清单；
- [`decisions.md`](decisions.md) 仍为历史决策与状态记录，后续将迁往治理层。

## 旧文件的当前作用

| 文件 | 当前解释 |
| --- | --- |
| [01-roles-and-abstraction.md](01-roles-and-abstraction.md) | 迁移源与历史详细展开；通用概念/评估语义已在 `spec/` 重述，角色与 L0–L4 已作为软件专项解释 |
| [02-five-phases.md](02-five-phases.md) | 迁移源与软件五阶段详细操作文本；通用关注点与专项结构已进入 `spec/` |
| [03-cognitive-mechanisms.md](03-cognitive-mechanisms.md) | 迁移源；其内容已分流到自适应、评估、交互指导、表示指导等层，仍需核对剩余详细规则 |
| [04-templates.md](04-templates.md) | 历史模板原貌；当前解释以 `guidance/templates.md` 的“载体而非规范”地位为准 |
| [05-antipatterns-and-boundaries.md](05-antipatterns-and-boundaries.md) | 迁移源：反模式已开始转为条件化失效模型，科学表述边界已进入治理层；参考资料待研究目录迁移 |
| [decisions.md](decisions.md) | 历史决策与项目状态；追溯用，不自动等于当前规范层级 |

## 执行保障边界

当前通用规范仍保留“不能只依赖人的记忆、AI 上下文或软性约定，需要可观察、可检查、可恢复的执行保障”这一需求，但不预设 Skill、状态文件、会话恢复、子代理、Hook 或其他具体实现形式。载体与保障系统应根据规范对象、失效模型和真实运行证据另行设计。
