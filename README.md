# 人机协作规格与演进实验

本仓库探索一套可跨软件开发、研究、学习、数据分析等领域使用的**通用人机协作规格**，并用真实任务持续校准其工作流、指导与执行保障方式。

## 不变量

**规格内容是根本。** Agent 入口、Skill、任务状态、模板、UI 或其他技术只是可选的体现、检验或保障形式；具体载体不能自动取得规范权威。

仓库同时保留观察、候选主张、研究、实验和历史，用来解释当前知识从何而来、还缺什么证据以及如何继续修订。

## 建议阅读顺序

1. [`docs/spec/README.md`](docs/spec/README.md) — 当前维护的人机协作规格
2. [`docs/spec/norms.md`](docs/spec/norms.md) — 当前跨领域通用规范
3. [`docs/spec/model.md`](docs/spec/model.md) — 参与者、角色、权威、协作状态、证据、表示、独立性等概念区分
4. [`docs/spec/adaptation.md`](docs/spec/adaptation.md) / [`evaluation.md`](docs/spec/evaluation.md) / [`workflows.md`](docs/spec/workflows.md) — 自适应、评估与任务推进模型
5. [`docs/guidance/`](docs/guidance/README.md) — 可替换的交互、表示与模板做法
6. [`docs/governance/`](docs/governance/README.md) — 项目演进、证据边界与决策历史
7. （按需）[`docs/research/`](docs/research/README.md) / [`docs/experiments/`](docs/experiments/README.md) — 研究依据与历史保障实验
8. （历史追溯）[`docs/archive/`](docs/archive/README.md) — 历史全文、旧版本快照与迁出材料

## 目录角色

| 路径 | 角色 |
| --- | --- |
| `docs/spec/` | **当前维护的人机协作规格** |
| `docs/guidance/` | 可替换的交互、表示和模板方法；不是通用合规条件 |
| `docs/governance/` | 项目自身的分类、关系、演进、证据治理与决策历史 |
| `docs/research/` | 外部研究与成熟实践的证据/机制研究；不自动取得规范权威 |
| `docs/experiments/` | 项目曾运行的实验性保障实现与试点记录 |
| `docs/overview.md` | 当前导读，非第二事实源 |
| `docs/archive/` | 历史全文、旧版本快照与迁出材料 |
| `feedback/` | 实战观察与摩擦入口；内容先保真，再决定去向 |
| `insights/` | 候选主张与设计解释，非当前规格 |
| `skills/` | 实验性 Skill 载体与行为 eval；非规范权威 |
| `tasks/` | 本项目演进任务状态与历史试点证据 |

## 本仓库现在不是什么

- 不是 IDE 插件、工作流引擎或强制门禁；
- 不是已定型的 Skill / `AGENTS.md` 产品包；
- 不是“克隆即可在任意项目启用”的安装说明；
- 也不把当前分类体系视为不可修改的封闭本体。

当前处于规格持续校准与执行保障探索阶段。新发现可以被吸收、缩窄、重分类或搁置；只有当前维护的规格内容应被当作项目现行立场。
