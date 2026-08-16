# 旧规范路径兼容与历史路由

> 本目录不再承载当前人机协作正文。它只用于兼容旧链接、说明旧章节的当前去向，并提供历史追溯入口。
>
> 当前规格见 [`../spec/`](../spec/README.md)；可替换指导见 [`../guidance/`](../guidance/README.md)；项目治理见 [`../governance/`](../governance/README.md)。

## 权威边界

- 本目录中的 Chapter 00–05 与 `decisions.md` 都是**兼容路由**，不是第二份事实源；
- 当前主张以 `spec/`、`guidance/`、`governance/`、`research/` 等对应现行文件为准；
- 旧章节原文已保存在 `archive/` 或治理历史中，用于核对来源与演化；
- 历史上“已采纳”的做法不因保存在旧文档中自动恢复为当前通用规范。

## 旧路径映射

| 旧路径 | 当前去向 | 历史原文 |
| --- | --- | --- |
| [`00-purpose-and-principles.md`](00-purpose-and-principles.md) | [`../spec/norms.md`](../spec/norms.md)；相关概念见 [`../spec/model.md`](../spec/model.md) | [`../archive/workflow-v0.15.md`](../archive/workflow-v0.15.md) |
| [`01-roles-and-abstraction.md`](01-roles-and-abstraction.md) | `spec/model.md`、`spec/evaluation.md`、`spec/domains/software-development.md`、通用规范 | [`../archive/norm-01-roles-and-abstraction-v0.16.md`](../archive/norm-01-roles-and-abstraction-v0.16.md) |
| [`02-five-phases.md`](02-five-phases.md) | [`../spec/workflows.md`](../spec/workflows.md) 与 [`../spec/domains/software-development.md`](../spec/domains/software-development.md) | [`../archive/norm-02-five-phases-v0.16.md`](../archive/norm-02-five-phases-v0.16.md) |
| [`03-cognitive-mechanisms.md`](03-cognitive-mechanisms.md) | `spec/adaptation.md`、`spec/evaluation.md`、`spec/failure-models.md`、`guidance/` 与软件专项 | [`../archive/norm-03-cognitive-mechanisms-v0.16.md`](../archive/norm-03-cognitive-mechanisms-v0.16.md) |
| [`04-templates.md`](04-templates.md) | [`../guidance/templates.md`](../guidance/templates.md) | [`../archive/norm-04-templates-v0.16.md`](../archive/norm-04-templates-v0.16.md) |
| [`05-antipatterns-and-boundaries.md`](05-antipatterns-and-boundaries.md) | `spec/failure-models.md`、`governance/evidence-policy.md`、`research/scientific-basis.md` 及相关指导/专项 | [`../archive/norm-05-antipatterns-and-boundaries-v0.16.md`](../archive/norm-05-antipatterns-and-boundaries-v0.16.md) |
| [`decisions.md`](decisions.md) | [`../governance/decisions.md`](../governance/decisions.md) | [`../governance/decision-log-v0.16.md`](../governance/decision-log-v0.16.md) |

完整的重组前单文件快照见 [`../archive/workflow-v0.15.md`](../archive/workflow-v0.15.md)。

## 执行保障边界

当前通用规范仍保留“不能只依赖人的记忆、AI 上下文或软性约定，需要可观察、可检查、可恢复的执行保障”这一需求，但不预设 Skill、状态文件、会话恢复、子代理、Hook 或其他具体实现形式。载体与保障系统应根据规范对象、失效模型和真实运行证据另行设计。
