# 历史归档

本目录保存已经退出当前维护面的**历史全文、旧版本快照与迁出材料**。这些文件用于追溯来源、比较语义变化和核对旧决策，不因被保留而继续取得当前规范或指导权威。

当前知识请从 [`../spec/`](../spec/README.md)、[`../guidance/`](../guidance/README.md)、[`../governance/`](../governance/README.md) 与 [`../research/`](../research/README.md) 进入。

## 主要归档

| 文件 | 内容 |
| --- | --- |
| [`workflow-v0.15.md`](workflow-v0.15.md) | 重组前的单文件完整规格快照；包含 Chapter 00 等历史来源 |
| [`norm-01-roles-and-abstraction-v0.16.md`](norm-01-roles-and-abstraction-v0.16.md) | 旧角色、抽象层与能力层次章节原文 |
| [`norm-02-five-phases-v0.16.md`](norm-02-five-phases-v0.16.md) | 旧五阶段章节原文 |
| [`norm-03-cognitive-mechanisms-v0.16.md`](norm-03-cognitive-mechanisms-v0.16.md) | 旧横切认知机制章节原文 |
| [`norm-04-templates-v0.16.md`](norm-04-templates-v0.16.md) | 旧模板章节原文 |
| [`norm-05-antipatterns-and-boundaries-v0.16.md`](norm-05-antipatterns-and-boundaries-v0.16.md) | 旧反模式、科学边界与参考资料章节原文 |
| [`assurance-and-pilot-notes-from-workflow-v0.15.md`](assurance-and-pilot-notes-from-workflow-v0.15.md) | 从旧单文件拆出的保障与早期试点记录 |

历史决策表另保存在 [`../governance/decision-log-v0.16.md`](../governance/decision-log-v0.16.md)。旧目录和兼容跳转不继续保留在当前树；需要精确查看旧路径时使用 Git 历史。

## 旧结构到当前结构

| 历史对象 | 当前去向 |
| --- | --- |
| Chapter 00：目标与原则 | [`../spec/norms.md`](../spec/norms.md)；相关概念区分见 [`../spec/model.md`](../spec/model.md) |
| Chapter 01：角色与抽象 | [`../spec/model.md`](../spec/model.md)、[`../spec/evaluation.md`](../spec/evaluation.md)、[`../spec/domains/software-development.md`](../spec/domains/software-development.md) |
| Chapter 02：五阶段 | 通用关注点见 [`../spec/workflows.md`](../spec/workflows.md)；软件五阶段见 [`../spec/domains/software-development.md`](../spec/domains/software-development.md) |
| Chapter 03：横切认知机制 | [`../spec/adaptation.md`](../spec/adaptation.md)、[`../spec/evaluation.md`](../spec/evaluation.md)、[`../guidance/`](../guidance/README.md)、[`../spec/failure-models.md`](../spec/failure-models.md) 及软件专项 |
| Chapter 04：模板 | [`../guidance/templates.md`](../guidance/templates.md) |
| Chapter 05：反模式与科学边界 | [`../spec/failure-models.md`](../spec/failure-models.md)、[`../governance/evidence-policy.md`](../governance/evidence-policy.md)、[`../research/scientific-basis.md`](../research/scientific-basis.md) |
| 旧 `decisions.md` | 当前解释见 [`../governance/decisions.md`](../governance/decisions.md)；原表见 [`../governance/decision-log-v0.16.md`](../governance/decision-log-v0.16.md) |
| reference study | [`../research/assurance-mechanisms.md`](../research/assurance-mechanisms.md) |
| v1 implementation experiment | [`../research/assurance/studies/v1/assurance-v1.md`](../research/assurance/studies/v1/assurance-v1.md) |

## 使用原则

- 历史文本回答“当时项目如何表述/决定”，不自动回答“现在项目主张什么”；
- 若历史材料与当前正文冲突，以当前正文及明确的 `narrows / supersedes / reclassified` 关系为准；
- 若想把历史做法重新带回当前项目，应重新经过分类、证据校准和必要的规范判断，而不是直接复制旧结论。
