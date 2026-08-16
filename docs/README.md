# docs/

本目录是仓库的主要阅读面。当前结构按语义职责分为规格、指导、治理、研究、实验与历史。

| 路径 | 角色 | 何时读 |
| --- | --- | --- |
| [`spec/`](spec/README.md) | **当前维护的人机协作规格** | 要理解项目现行概念、规范、自适应、评估、工作流、失效模型与领域专项 |
| [`guidance/`](guidance/README.md) | 可替换的交互、表示与模板做法 | 要把规格落实成低摩擦操作，但不把配方误当规范 |
| [`governance/`](governance/README.md) | 项目分类、关系、演进、证据治理与决策历史 | 要维护、吸收反馈、重分类或追溯知识 |
| [`research/`](research/README.md) | 保障机制与相关研究 | 关心外部研究、成熟实践、机制依据与外推边界 |
| [`experiments/`](experiments/README.md) | 历史保障实现与试点 | 关心曾经如何试跑、观察到什么、尚不能证明什么 |
| [`overview.md`](overview.md) | 当前导读 | 快速建立规格层级和阅读路径 |
| [`archive/`](archive/README.md) | 全文快照与迁出材料 | 核对历史版本、旧表述和内容演化 |

旧 `docs/norm/`、旧单文件工作流入口，以及 reference-study / v1-implementation 的兼容跳转均已从当前树移除。历史正文与旧版本表述保存在 `archive/`；研究与实验的当前位置分别是 `research/` 与 `experiments/`。Git 历史仍保留旧路径本身。

## 维护原则

- 当前知识只在其主归属处维护，不保留无实际消费者的兼容目录或跳转文件；
- `guidance/` 中的方法、模板和表示是可替换实现，不因实用而取得规范权威；
- `research/`、`experiments/` 与历史决策提供依据、试验和追溯，不与当前规格争夺权威；
- `feedback/`、`insights/`、`skills/` 与 `tasks/` 保持各自的观察、候选、实验载体与工作状态职责；
- 目录表达主要归属与默认地位，重要的派生、实现、测试、专项化或取代关系通过轻量 Markdown 链接保留；
- 历史材料如需重新进入当前规格或指导，应按 [`governance/project-evolution.md`](governance/project-evolution.md) 重新分类和校准，而不是因旧版本曾采用就自动恢复权威。

根目录 [`README.md`](../README.md) 提供仓库级导航。
