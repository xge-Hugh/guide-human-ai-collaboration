# 轻量人机协作规范

本仓库沉淀一套面向长期研发的人机协作**规范草案**：交付可靠的同时，保留人的独立判断、可观察贡献与渐进学习。

## 不变量

**规范内容是根本。** Agent 入口、Skill、任务状态等只是可选的体现或保障形式；本仓库尚未决定最终以何种形式落地，当前目标是让浏览者读懂规范主张什么，而不是提供开箱即用工具。

## 本仓库现在不是什么

- 不是 IDE 插件、工作流引擎或强制门禁
- 不是已定型的 Skill / `AGENTS.md` 产品包
- 不是「克隆即可在任意项目启用」的安装说明

仓库里仍保留 `skills/` 与 `tasks/`，那是试点期的**实验载体与证据**，请勿当作产品入口。

## 建议阅读顺序

1. [docs/overview.md](docs/overview.md) — 一两屏导读：问题、主张、阶段与常见误解  
2. [docs/norm/README.md](docs/norm/README.md) — 规范正文（按章节阅读）  
3. （可选）[docs/human-ai-collaboration-reference-study.md](docs/human-ai-collaboration-reference-study.md) — 保障机制的社区参考与取舍  
4. （可选）[docs/human-ai-collaboration-v1-implementation.md](docs/human-ai-collaboration-v1-implementation.md) — 保障形式实验笔记（非规范正文）

文档角色总表见 [docs/README.md](docs/README.md)。重组前全文快照：[docs/archive/workflow-v0.15.md](docs/archive/workflow-v0.15.md)。

## 目录角色

| 路径 | 角色 |
| --- | --- |
| `docs/norm/` | **规范正文**（权威） |
| `docs/overview.md` | 导读（非第二事实源） |
| `docs/*-reference-study.md` / `*-v1-implementation.md` | 研究与保障形式实验 |
| `docs/archive/` | 历史全文与从正文迁出的试点/保障笔记 |
| `skills/` | 实验性 Skill 载体，形态未决 |
| `tasks/` | 本规范自身的演进任务与试点证据归档 |

## 状态

草案。正在以「可读雏形」整理文档；「拿来用」的保障形式另议。
