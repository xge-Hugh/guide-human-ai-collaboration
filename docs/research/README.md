# 研究

本目录是项目的**主动 inquiry 面**。它不仅保存外部研究，也保存项目自身正在形成和修订的研究问题、候选模型、假设、证据综合、field observation、study 设计与结果。

研究对象可以是 `current research model`，但这不等于当前规范。规范权威只由 [`../spec/`](../spec/README.md) 中的当前规格承担。

## 当前 research program

- [`assurance/`](assurance/README.md)：执行保障、carrier reliability、运行证据与相关 study；
- [`cognitive-coordination/`](cognitive-coordination/README.md)：任务模型、认知分配、修正、重建、战略性接触与相关候选机制；
- [`collaborative-relations/`](collaborative-relations/README.md)：人机协作中的非对称、依赖/相关性、责任与委托、分布式参与者状态、自我/他者模型、表示与状态协调、分配成本及其纵向反馈；
- [`runtime-capability/`](runtime-capability/README.md)：研究项目理论如何在不假定修改模型权重的前提下，经由模型内在能力、上下文构造、检索、提示/Skill、经验与外部持久化结构转化为可靠运行时能力；
- [`temporal-coordination/`](temporal-coordination/README.md)：AI waiting、任务悬置/恢复、rejoin collision 与 interaction timing；
- [`external-evidence.md`](external-evidence.md)：跨 program 使用的外部研究入口与科学表述边界。

## Program 与对象

Research program 是**主要维护/检索上下文**，不是永久本体边界或独占所有权。一个 construct 可以被多个 program 使用；只有当它形成独立、重复的维护压力时，才考虑新的共享研究位置。

不要为了每个小 hypothesis 创建目录，也不要建立 `shared/` 垃圾桶。Program 内可按实际需要维护 model/hypotheses、evidence synthesis、design diagnosis、studies、study instruments 与 interpretation，但不为对称制造空目录。

## Evidence boundary

本项目区分 field/observational evidence、project study/experimental evidence 与 external research evidence。它们都可能进入 research inquiry，但证明范围不同。

研究结论可以支持、缩窄或威胁 specification/guidance/engineering decision；不能因为写在 `research/` 就获得事实或规范权威。具体边界见 [`../governance/evidence-policy.md`](../governance/evidence-policy.md)。
