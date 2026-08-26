# 决策驱动的证据循环：候选项目演进方法

- **日期**：2026-08-26
- **地位**：`candidate project-governance method`
- **语义类型**：项目演进 / 证据路由方法；不是人机协作规范，不是固定工作流，也不是正式 assurance architecture
- **来源**：认知协调候选模型的 A/B/C 审计、独立研究校准、Skill cloud 语义回放、最小 pilot Skill 修订与 field-pilot 启动
- **当前证据强度**：一次完整真实项目循环显示出实际判别价值；不足以升级为当前治理方法

## 1. 核心问题

项目已经拥有多种认识工具：概念分析、反例、外部研究、cloud 分析、真实 Skill 试跑、受控 runner、独立审查、历史 Issue/feedback、原始代码/日志/来源等。

候选方法不要求所有问题经过同一套阶段，而解决一个更具体的问题：

> **当一个真实项目决定被某项未知阻塞时，应该用哪一种最低成本、足以区分 competing explanations 的证据方法；取得结果后，怎样把机制放回真实环境继续产生新线索？**

因此重点不是“完整实验流程”，而是**证据方法的按需路由**。

## 2. 候选循环

```text
现有模型 / 规范 / 历史观察 / field clue
                ↓
识别一个会改变真实项目决定的未知
                ↓
形成 competing explanations / candidate mechanism
                ↓
选择最低成本且足够判别的方法
                ↓
概念审计 / 反例 / 研究 / cloud semantic replay /
原始证据检查 / runner / 独立审查 / 纵向观察 ...
                ↓
缩窄、修正、保留或拒绝候选
                ↓
若需要现实接触：放入可逆 pilot carrier
                ↓
真实生态使用
                ↓
新的 clue / failure / unexpected success / friction
                ↓
只有存在新决策价值时再次进入循环
```

循环不是固定阶段表。任一节点都可跳过；如果已有证据足以决定，就直接行动。

## 3. 第一轮 pilot 实际发生了什么

### 3.1 初始候选

认知协调模型使项目怀疑旧 Skill 对责任—能力问题过度依赖 explicit learning / tutor subsystem，并提出五项候选 runtime 增量。

### 3.2 低成本 cloud 判别先于 Skill 重写

在真正修改 Skill 前，使用 6 个高信息历史/构造案例对 `native / current Skill / current Skill + overlay` 做语义回放。

该回放不是随机模型效果实验，只回答：

- 新候选是否真的增加当前 Skill 尚未表达的行为；
- 哪些只是用新理论重新命名旧规则；
- 哪些变化最可能产生新的 runtime 差异；
- 哪些 negative cases 必须保留以防 over-trigger。

### 3.3 方法产生了 recovered judgment

回放发现原诊断过强：旧 Skill 已能通过承重判断、风险、熟悉度和 interaction-and-learning 进入支援路径，也已有很强的机械任务 anti-overtrigger。

因此没有把整个 cognitive-coordination overlay 写入 Skill，而只保留四类更清楚的增量：

1. 责任—能力 mismatch 的**非教学响应组合**；
2. AI 压缩可能遮蔽承重证据时的**战略性直接证据切片**；
3. 新证据改变 AI 承重判断时的**实质模型修正结算**；
4. grounding 允许**生产性未决分歧**，而不是要求 explanatory model 完全收敛。

这次缩窄直接减少了潜在重复规则和触发复杂度。

### 3.4 可逆 field carrier

四类增量随后进入实验性 Skill，而不是直接进入规范或最终 assurance architecture。Skill 的目的在这里是让候选机制接触真实长上下文、工具、业务责任、异常细节和人的日常工作，从而产生 synthetic replay 难以预先构造的新线索。

## 4. 三类主要 instrument 的不同认识功能

### Skill / pilot carrier：偏 discovery

优势：真实生态、组合复杂、会遇到未知未知；适合发现“有什么值得解释”。

弱点：变量混杂、随机、无法单独归因机制。

### Runner：偏 discrimination

优势：可控制 `native / carrier / mechanism` 差异、保存原始证据、比较首次机会行为和成本；适合回答 competing explanations。

弱点：synthetic case 可能遗漏真实生态结构；存在 grader 与测量脆弱性；不适合因为工具已经存在就测试一切。

### Cloud analysis / independent conceptual review：偏 model challenge 与 synthesis

优势：可以跨 artifacts 重建模型、找重复规则、产生反例、查研究、解释 field observation。

弱点：容易形成同源理论闭环；不能把语义分析当随机运行效果证据；cloud reviewer 也不是天然独立真理源。

这些角色不是永久产品边界。最终 assurance architecture 可以是 composite，并按 assurance object 的性质选择常驻 prompt / `AGENTS.md`、Skill、状态、工具脚本、Hook、evaluator 或其他 carrier。

## 5. 方法选择原则

候选总原则：

> **使用能够解决当前 decision-relevant uncertainty 的最低成本证据方法。**

示例：

- 当前文件已经明确存在/不存在某规则 → 直接读文件，不跑多轮 API 实验；
- 两个 prompt/carrier 是否造成 first-opportunity 行为差异 → 小规模 runner replay；
- 一个认知机制是否有外部理论/实证邻近支持 → research calibration；
- 长期重建性/能力轨迹 → 需要跨时间观察，单次 replay 不足；
- generator 是否收到 hidden rubric → deterministic runner test，而不是统计推断；
- 新机制在真实工作是否产生 unexpected clue → field pilot。

严谨不等于总是使用最重的方法；主张强度应与所选方法能支持的范围一致。

## 6. 与 A/B/C 的关系

A/B/C 可作为**候选模型本身需要系统性压力测试时**的一种后台方法：

- A：检查能否解释/压缩已知证据而不强迫解释；
- B：主动找反例、边界、坏建议和成本；
- C：要求产生不是事后重述的新后果。

但 A/B/C 不是项目循环的固定前置阶段。许多局部问题可以直接从 field clue 进入证据检查、修复或 runner discrimination。

## 7. 该方法自身的边界与失败条件

候选循环若出现下列现象，应被缩窄、暂停或修订，而不是递归增加更多阶段：

- 分析/记录很多，但很少改变真实项目决定；
- cloud 每次都为自己之前的理论找到支持；
- 每个 field observation 都被硬套到现有 candidate model；
- runner 因为已经存在而被用于测试所有规范；
- pilot carrier 不断累积候选机制，却很少删除失败机制；
- 维护 protocol、artifact 和 eval 的成本超过减少的误判/返工/认知负担；
- 多个 instrument 只是重复同一信息来源，却被误称为独立证据；
- 方法开始要求人为制造 field observation 或填写固定问卷；
- 逻辑上还能再做一层 meta-analysis 被误认为必须继续。

### Meta-level stop rule

> 只有当再上升一层会暴露新的承重区别、反例、预测、证据解释或真实决定时，才把当前方法本身作为新的 inquiry object。

“还能继续反思”本身不是继续的理由。

## 8. 当前可支持与不可支持的结论

### 当前可支持

- 第一轮真实项目循环中，cloud semantic replay 在低成本下发现了候选设计与旧 Skill 的重复，并促成一次实质缩窄；
- 该缩窄在 field deployment 前避免了更大的 Skill 重写；
- 把 pilot carrier / runner / cloud 分成 discovery / discrimination / challenge 的认识功能有实际解释价值；
- project method 可以在不采用固定实验模板的前提下保持证据边界。

### 当前不可支持

- 不能声称该循环普遍优于其他项目演进方法；
- 不能声称 Skill field pilot 已证明四项新机制有效；
- 不能声称 runner / cloud / Skill 三件套是最终项目架构；
- 不能要求未来每项 norm 或 insight 都走此循环；
- 不能因为方法第一次成功修正自己就认为它“自证正确”。

## 9. 何时考虑晋升为当前治理方法

至少需要未来真实维护中出现多个独立实例，证明该循环反复能够：

- 在投入更贵实现/实验前删除或缩窄错误候选；
- 把 field clue 路由到合适的证据方法，而不是默认升级实验；
- 产生会改变项目决定的 discriminating evidence；
- 保持 observation / model / norm / implementation / evidence 的地位边界；
- 控制维护和认知成本；
- 在失败时允许自身被缩窄或替代。

若这些实例出现，再考虑把核心 routing principle 纳入 `docs/governance/project-evolution.md`。在此之前，本文件只作为 candidate method 和后续实例的比较基准。
