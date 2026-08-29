# 人机协作研究与工程

本仓库探索长期人机协作中的规范、模型、证据、指导与工程机制，目标是在软件开发、研究、学习、数据分析等任务中，同时改善任务结果、人的实质判断与责任相关能力，以及人和 AI 作为组合系统的可靠性。

项目现在被维护为一个**研究导向的工程知识系统**：真实协作产生观察和线索；项目据此形成候选模型、假设和研究问题，通过外部研究、project study、field observation 与工程 pilot 持续校准；当前被采用的语义与规范独立维护在规格中；Skill、工具和其他 carrier 负责可执行试跑，但不会因被实现就取得规范或事实权威。

## 不变量

**规格内容是根本，但规格不是全部知识。** 当前规范回答“项目现在要求什么”；研究回答“什么机制似乎能解释、预测或区分协作现象”；指导回答“当前有哪些可替换做法”；工程 carrier 回答“怎样把候选或当前要求运行起来”。

任何目录、Skill、工具、study 或实验结果都不能仅凭物理位置自动取得更强权威。

## 建议阅读顺序

1. [`docs/overview.md`](docs/overview.md) — 当前项目导读
2. [`docs/spec/README.md`](docs/spec/README.md) — 当前维护的人机协作规格
3. [`docs/spec/norms.md`](docs/spec/norms.md) — 当前跨领域通用规范
4. [`docs/research/README.md`](docs/research/README.md) — 当前研究问题、候选模型、证据与 studies
5. [`docs/guidance/`](docs/guidance/README.md) — 可替换的交互、表示与模板做法
6. [`docs/governance/`](docs/governance/README.md) — 项目分类、证据边界、演进与决策历史
7. [`feedback/`](feedback/README.md) / [`insights/`](insights/README.md) — 低成本观察入口与轻量候选/lineage
8. [`docs/archive/`](docs/archive/README.md) — 历史全文、旧版本快照与已退出当前维护面的材料

## 目录角色

| 路径 | 角色 |
| --- | --- |
| `docs/spec/` | **当前维护的人机协作规格** |
| `docs/research/` | 主动 inquiry：问题、假设、模型、外部证据、project studies、field observation 与解释 |
| `docs/guidance/` | 已采用但可替换的交互、表示和模板方法 |
| `docs/governance/` | 项目自身的分类、关系、证据治理、演进与决策历史 |
| `feedback/` | 实战观察与摩擦的低成本入口；先保真，再决定去向 |
| `insights/` | 小型候选、设计直觉、lineage 与尚未形成独立 inquiry context 的推理 |
| `skills/` | 实验性可执行 Skill carrier 与行为 eval；非规范权威 |
| `tools/` / `tests/` | 研究或工程使用的可执行基础设施及代码验证 |
| `docs/archive/` | 历史全文、旧版本快照与已退出当前维护面的材料 |

## 目录不是本体

项目知识本质上是图状关系。目录只提供一个**可替换的主要维护/检索投影**：规格按权威与语义职责组织，研究按 inquiry cohesion 组织，feedback 按时间低成本捕获，Skill/工具按可执行责任组织。

因此目录可以在项目知识结构变化后再次迁移；迁移的目标是降低重建、权威判断和维护成本，而不是追求永久分类。

## 本仓库现在不是什么

- 不是 IDE 插件、固定工作流引擎或强制门禁；
- 不是已定型的 Skill / `AGENTS.md` 产品包；
- 不是科研论文仓库，也不把外部研究包装成对具体实现的自动证明；
- 不是所有知识必须按 `feedback → insight → research → spec` 晋升的流水线；
- 不把当前目录结构视为不可修改的封闭本体。
