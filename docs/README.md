# docs/

本目录是仓库的主要阅读面。当前结构按语义职责分为规格、指导、治理、研究、实验与历史；旧 `norm/` 只保留兼容入口，不再承载当前正文。

| 路径 | 角色 | 何时读 |
| --- | --- | --- |
| [`spec/`](spec/README.md) | **当前维护的人机协作规格** | 要理解项目现行概念、规范、自适应、评估、工作流、失效模型与领域专项 |
| [`guidance/`](guidance/README.md) | 可替换的交互、表示与模板做法 | 要把规格落实成低摩擦操作，但不把配方误当规范 |
| [`governance/`](governance/README.md) | 项目分类、关系、演进、证据治理与决策历史 | 要维护、吸收反馈、重分类或追溯知识 |
| [`research/`](research/README.md) | 保障机制与相关研究 | 关心外部研究、成熟实践、机制依据与外推边界 |
| [`experiments/`](experiments/README.md) | 历史保障实现与试点 | 关心曾经如何试跑、观察到什么、尚不能证明什么 |
| [`overview.md`](overview.md) | 当前导读 | 快速建立规格层级和阅读路径 |
| [`archive/`](archive/) | 全文快照与迁出材料 | 核对历史版本、旧表述和内容演化 |
| [`norm/`](norm/README.md) | 旧规范路径兼容与历史路由 | 跟随旧链接或定位旧章节当前去向 |
| [`human-ai-collaboration-workflow.md`](human-ai-collaboration-workflow.md) | 旧单文件入口（跳转） | 兼容旧链接 |

原 `human-ai-collaboration-reference-study.md` 与 `human-ai-collaboration-v1-implementation.md` 已分别迁入 `research/` 与 `experiments/`，旧路径只保留兼容跳转。历史决策已迁入 `governance/`。旧 Chapter 00–05 的当前语义均已进入新结构，原路径仅用于路由，原文保存在 `archive/`。

## 维护原则

- 当前知识只在其主归属处维护，不通过兼容路径维护第二份正文；
- `guidance/` 中的方法、模板和表示是可替换实现，不因实用而取得规范权威；
- `research/`、`experiments/` 与历史决策提供依据、试验和追溯，不与当前规格争夺权威；
- `feedback/`、`insights/`、`skills/` 与 `tasks/` 保持各自的观察、候选、实验载体与工作状态职责；
- 目录表达主要归属与默认地位，重要的派生、实现、测试、专项化或取代关系通过轻量 Markdown 链接保留；
- 历史材料如需重新进入当前规格或指导，应按 [`governance/project-evolution.md`](governance/project-evolution.md) 重新分类和校准，而不是因旧版本曾采用就自动恢复权威。

根目录 [`README.md`](../README.md) 提供仓库级导航。
