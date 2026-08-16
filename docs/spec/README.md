# 当前人机协作规格

> 地位：本目录承载项目对**人机协作本身的当前维护知识**。其中不同文件回答不同问题；只有规范性文件定义“可接受协作必须满足什么”。
>
> 项目如何分类、吸收、修订这些知识，见 [`../governance/project-evolution.md`](../governance/project-evolution.md)。

## 当前迁移状态

本目录正在从旧 `docs/norm/` 分阶段迁入。迁移期间不建立两个并列权威：

- 已完成迁移的内容，以本目录对应文件为当前权威；
- 已完成**语义提炼但尚未完成全文物理迁移**的内容，以本目录解释其通用/专项地位，旧章节继续承载尚未搬完的详细规则；
- 尚未迁入的旧章节，仍按 [`../norm/README.md`](../norm/README.md) 标明的地位解释；
- 旧路径若已完成全文迁移，只保留兼容跳转，不再维护第二份正文。

当前规格文件：

| 当前文件 | 回答的问题 | 迁移状态 |
| --- | --- | --- |
| [`norms.md`](norms.md) | 通用协作必须满足什么、哪些认识论边界不能越过、哪些通用机制保护这些条件 | 原 Chapter 00 已完成全文迁移 |
| [`model.md`](model.md) | 用什么概念和相互区分来描述协作 | 已从 Chapter 00/01 及跨章审查中提炼；不新增规范要求 |
| [`adaptation.md`](adaptation.md) | 风险、可逆性、不确定性、压力、熟悉程度、学习目标与协作状态如何调节投入和保障 | 已从 Chapter 03 提炼通用自适应语义；旧章仍保留部分实现配方 |
| [`evaluation.md`](evaluation.md) | 任务结果、人的能力、协作能力与载体运行表现如何区分，什么证据支持什么结论 | 已提炼通用评估语义；旧 Chapter 01/03 仍保留部分历史展开 |
| [`workflows.md`](workflows.md) | 可跨领域复用的任务关注点与依赖关系是什么 | 已从软件五阶段抽取通用工作流模型 |
| [`failure-models.md`](failure-models.md) | 哪些条件/机制会使协作违反规范或失去预期价值 | 已从 Chapter 05 反模式与真实反馈中抽取条件化失效模型；不是反模式的机械反转 |
| [`domains/software-development.md`](domains/software-development.md) | 软件开发中角色、抽象层、五阶段与证据实践如何专项化 | 已建立专项结构；旧 Chapter 01/02 仍暂时保留更细的历史操作文本，待后续完整迁移核对 |

可替换的交互、表示与模板做法见 [`../guidance/`](../guidance/README.md)。项目自身的科学/经验主张边界与历史决策见 [`../governance/`](../governance/README.md)；研究依据与历史保障实验已分别迁入 [`../research/`](../research/README.md) 与 [`../experiments/`](../experiments/README.md)。

当前主要剩余迁移工作是**旧 Chapter 01–05 的详细文本核对**：确认其独有内容已进入正确的规格、指导、治理、研究或历史位置后，再把旧文件转为兼容入口或归档。不会为了目录完整性预建空分类。

## 权威与关系

物理位置提供默认地位，但不能表达全部关系。重要关系可在正文中用普通 Markdown 明示，例如：`derived from`、`threatens`、`tests`、`implements`、`specializes`、`narrows/supersedes`。只记录若丢失会导致权威误判、追溯断裂或重复推导的关系。

Skill、任务状态、模板、UI、Agent、Hook、评测器等可以实现、表示或检验本规格，但不因成为载体而自动取得规范权威。
