# docs/

本目录是仓库的主要知识阅读面。不同子目录刻意采用不同的组织维度，因为它们承担不同的维护责任。

| 路径 | 角色 | 何时读 |
| --- | --- | --- |
| [`spec/`](spec/README.md) | **当前维护的人机协作规格** | 理解项目现在采用的概念、规范、自适应、评估、工作流、失效模型与领域专项 |
| [`research/`](research/README.md) | 主动 inquiry：模型、假设、证据、studies 与外部研究 | 理解机制为什么被提出、证据如何支持/限制它、目前仍未知什么 |
| [`guidance/`](guidance/README.md) | 可替换的交互、表示与模板做法 | 把规格落实成低摩擦操作，但不把配方误当规范 |
| [`governance/`](governance/README.md) | 项目分类、关系、演进、证据治理与决策历史 | 维护、重分类、吸收新证据或追溯项目自身变化 |
| [`overview.md`](overview.md) | 当前导读 | 快速建立项目结构和阅读路径 |
| [`archive/`](archive/README.md) | 历史全文、旧版本与已退出当前维护面的材料 | 核对历史表述、旧结构和内容演化 |

## 维护原则

- 物理目录表达主要维护/检索上下文，不自动决定事实强度、规范权威或永久概念所有权；
- `spec/` 保持当前权威阅读面集中，不要求读者从多个 research program 拼装现行规范；
- `research/` 按 coherent inquiry 组织，study/experiment 是 inquiry 内的认识活动，不再作为独立顶层语义域；
- `guidance/` 中的方法是可替换实践，不因实用而取得规范权威；
- research model、study result、carrier implementation 与 current norm 的地位相互独立；
- 重要关系用轻量 Markdown 链接保留，不维护完整知识图谱；
- 历史旧路径由 `archive/`、必要的当前关系链接与 Git 历史承担追溯，不保留无消费者的兼容拓扑。
