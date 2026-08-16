# docs/

本目录是仓库的主要阅读面。当前正在从旧 `norm/` 结构迁往按语义职责分层的规格与治理结构；迁移期间以各目录 README 标明的权威边界为准。

| 路径 | 角色 | 何时读 |
| --- | --- | --- |
| [`spec/`](spec/README.md) | **当前维护的人机协作规格** | 要理解项目现行概念与通用规范 |
| [`governance/`](governance/README.md) | 项目分类、关系与演进方法 | 要维护、吸收反馈、重分类或追溯知识 |
| [`norm/`](norm/README.md) | 迁移中的旧规范目录 | 查尚未拆分的角色、工作流、机制、模板、反模式与决策历史 |
| [`overview.md`](overview.md) | 旧结构形成的导读 | 了解历史叙述；迁移完成前不作为当前架构入口 |
| [`human-ai-collaboration-reference-study.md`](human-ai-collaboration-reference-study.md) | 尚待迁移的保障机制研究与取舍 | 关心社区机制、研究依据与外推边界 |
| [`human-ai-collaboration-v1-implementation.md`](human-ai-collaboration-v1-implementation.md) | 尚待迁移的保障形式实验与试点结论 | 关心曾经如何试跑、证实/证伪了什么 |
| [`human-ai-collaboration-workflow.md`](human-ai-collaboration-workflow.md) | 旧单文件入口（跳转） | 兼容旧链接 |
| [`archive/`](archive/) | 全文快照与迁出笔记 | 核对历史与内容迁移 |

## 当前迁移原则

- 一个对象迁入 `spec/` 后，旧路径只保留跳转，不维护第二份正文；
- 尚未迁移的旧章节继续承载当前内容，但不能因为位于 `norm/` 就推断其中所有材料都是通用规范；
- `feedback/`、`insights/`、`skills/` 与 `tasks/` 继续保持各自的观察、候选、实验载体与工作状态职责；
- 目录表达主要归属与默认地位，重要的派生、实现、测试、专项化或取代关系通过轻量 Markdown 链接保留。

根目录 [`README.md`](../README.md) 提供仓库级导航。
