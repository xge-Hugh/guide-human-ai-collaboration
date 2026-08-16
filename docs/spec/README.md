# 当前人机协作规格

> 地位：本目录承载项目对**人机协作本身的当前维护知识**。其中不同文件回答不同问题；只有规范性文件定义“可接受协作必须满足什么”。
>
> 项目如何分类、吸收、修订这些知识，见 [`../governance/project-evolution.md`](../governance/project-evolution.md)。

## 当前规格组成

| 当前文件 | 回答的问题 | 当前定位 |
| --- | --- | --- |
| [`norms.md`](norms.md) | 通用协作必须满足什么、哪些认识论边界不能越过、哪些通用机制保护这些条件 | 跨领域通用规范 |
| [`model.md`](model.md) | 用什么概念和相互区分来描述协作 | 当前语义模型；不因定义维度而自动新增规范义务 |
| [`adaptation.md`](adaptation.md) | 风险、可逆性、不确定性、压力、熟悉程度、学习目标与协作状态如何调节投入和保障 | 当前通用自适应模型 |
| [`evaluation.md`](evaluation.md) | 任务结果、人的能力、协作能力与载体运行表现如何区分，什么证据支持什么结论 | 当前评估模型 |
| [`workflows.md`](workflows.md) | 可跨领域复用的任务关注点与依赖关系是什么 | 当前通用工作流模型；不规定固定阶段数 |
| [`failure-models.md`](failure-models.md) | 哪些条件/机制会使协作违反规范或失去预期价值 | 当前失效模型目录；不是反模式的机械反转 |
| [`domains/software-development.md`](domains/software-development.md) | 软件开发中角色、抽象层、五阶段与证据实践如何专项化 | 当前软件开发领域专项 |

可替换的交互、表示与模板做法见 [`../guidance/`](../guidance/README.md)。项目自身的科学/经验主张边界与历史决策见 [`../governance/`](../governance/README.md)；研究依据与历史保障实验分别位于 [`../research/`](../research/README.md) 与 [`../experiments/`](../experiments/README.md)。

旧 `docs/norm/` 已完成退役：其中 Chapter 00–05 与 `decisions.md` 仅保留兼容路由；原始正文和旧版本材料保存在 [`../archive/`](../archive/)。旧表述若与当前规格冲突，以本目录当前正文及明确的缩窄/取代关系为准。

## 权威与关系

物理位置提供默认地位，但不能表达全部关系。重要关系可在正文中用普通 Markdown 明示，例如：`derived from`、`supports`、`threatens`、`tests`、`implements`、`specializes`、`narrows/supersedes`。只记录若丢失会导致权威误判、追溯断裂或重复推导的关系。

Skill、任务状态、模板、UI、Agent、Hook、评测器等可以实现、表示或检验本规格，但不因成为载体而自动取得规范权威。

本目录不是封闭分类体系。若未来出现现有模型无法无失真表达的重要问题，可按项目演进方法增加、拆分或重分类知识对象，而不是为了保持当前目录形式强行归类。
