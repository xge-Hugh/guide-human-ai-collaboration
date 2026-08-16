# docs/

本目录是仓库的主要阅读面。当前正在从旧 `norm/` 结构迁往按语义职责分层的规格、指导与治理结构；迁移期间以各目录 README 标明的权威边界为准。

| 路径 | 角色 | 何时读 |
| --- | --- | --- |
| [`spec/`](spec/README.md) | **当前维护的人机协作规格** | 要理解项目现行概念、规范、自适应、评估、工作流与领域专项 |
| [`guidance/`](guidance/README.md) | 可替换的交互、表示与模板做法 | 要把规格落实成低摩擦操作，但不把配方误当规范 |
| [`governance/`](governance/README.md) | 项目分类、关系与演进方法 | 要维护、吸收反馈、重分类或追溯知识 |
| [`norm/`](norm/README.md) | 迁移中的旧规范目录 | 查尚未完全拆分的机制、模板、反模式与决策历史 |
| [`overview.md`](overview.md) | 当前导读 | 快速建立规格层级和阅读路径 |
| [`human-ai-collaboration-reference-study.md`](human-ai-collaboration-reference-study.md) | 尚待迁移的保障机制研究与取舍 | 关心社区机制、研究依据与外推边界 |
| [`human-ai-collaboration-v1-implementation.md`](human-ai-collaboration-v1-implementation.md) | 尚待迁移的保障形式实验与试点结论 | 关心曾经如何试跑、证实/证伪了什么 |
| [`human-ai-collaboration-workflow.md`](human-ai-collaboration-workflow.md) | 旧单文件入口（跳转） | 兼容旧链接 |
| [`archive/`](archive/) | 全文快照与迁出笔记 | 核对历史与内容迁移 |

## 当前迁移原则

- 一个对象完成全文迁移后，旧路径只保留跳转，不维护第二份正文；
- 已完成语义提炼但尚未搬完细节的旧章节继续作为迁移源，目录 README 必须说明其剩余职责；
- `guidance/` 中的方法、模板和表示是可替换实现，不因实用而取得规范权威；
- `feedback/`、`insights/`、`skills/` 与 `tasks/` 继续保持各自的观察、候选、实验载体与工作状态职责；
- 目录表达主要归属与默认地位，重要的派生、实现、测试、专项化或取代关系通过轻量 Markdown 链接保留。

根目录 [`README.md`](../README.md) 提供仓库级导航。
