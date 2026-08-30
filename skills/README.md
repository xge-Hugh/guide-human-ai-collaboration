# skills/

此处保留项目的实验性 Agent Skills 源码。Skill 是规范与研究候选的**可能运行载体**，不是规范本身，也不是本仓库当前的最终产品入口。

当前包含两类：

- `guide-human-ai-collaboration/`：历史 live pilot；在 Issue #31 的 vNext 分支中保持不变，作为 comparison baseline。
- `human-ai-*/`：`pilots/collaboration-carrier-vnext/` 使用的独立 Skill family。每个 Skill 按语义责任单独触发，不通过 umbrella Skill 统一加载。

vNext 的 resident kernel、host adapter、routing/behavior eval 与 carrier 组合说明见 [../pilots/collaboration-carrier-vnext/](../pilots/collaboration-carrier-vnext/README.md)。

阅读当前规范请从 [../docs/overview.md](../docs/overview.md) 开始。Skill 的目录结构、可读性或 eval 定义存在，不代表运行时关键行为已经得到验证。
