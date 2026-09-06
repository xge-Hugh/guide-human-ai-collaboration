# Static context carrier gap：resident kernel + conditional Skill 的能力转化缺口

- **日期**：2026-09-06
- **状态**：`candidate / design diagnosis`（不直接要求修改 current pilot）
- **触发观察**：当前 resident kernel + conditional Skill carrier 的结构质量已经明显优于旧版，但真实协作中仍常出现“理论在文件里、行为却没有稳定发生”；相较之下，在 cloud workflow 中先主动阅读项目内容再进入任务，主观表现更接近项目理论。
- **关联**：[`../model.md`](../model.md)、[`../evidence-review.md`](../evidence-review.md)、[`../../assurance/studies/v2/assurance-v2-phase-b-interpretation.md`](../../assurance/studies/v2/assurance-v2-phase-b-interpretation.md)、[`../../cognitive-coordination/design-diagnoses/skill-learning-capability-gap.md`](../../cognitive-coordination/design-diagnoses/skill-learning-capability-gap.md)

## 1. 结论先行

当前 carrier 的主要缺口不再适合描述成“Skill 内容不够完整”或“需要再加入更多理论”。

更深的诊断是：

> **resident kernel + conditional Skill 主要提供静态 context availability，但项目希望得到的是情境化 recognition、representation、operationalization、reactivation 与跨运行累计。两者不是同一对象。**

Phase B 已提供一个早期警告：增加更复杂的 runtime reasoning scaffold 并没有稳定产生相称行为增量。因此继续把更多 project model 压入 permanent prompt/Skill，可能重复同一种 translation failure。

---

## 2. 当前 carrier 已经做对什么

### 2.1 Resident kernel 适合承担少数高优先级 semantic boundaries

短、稳定、低歧义的 invariant/cue 可以持续存在于 context 中，提醒模型注意授权、epistemic integrity、human responsibility、proportionality 等项目 concern。

Phase B 的有限证据与当前 field experience 都不支持删除这个层。

### 2.2 Conditional Skill 能降低常驻 context cost

只有在模型判断相关时加载较丰富 procedure/reference，比把所有项目理论常驻 context 更符合 progressive disclosure，也更适合稳定、重复、窄范围的工作方法。

### 2.3 Skill 仍可以作为可替换实验表面

即使最终架构变化，Skill 仍是低成本 carrier probe：可测试 description、examples、procedure、reactivation 与 no-op boundary，而不需要把候选机制升级为 spec。

因此本 diagnosis 不是“Skill failure = discard Skill”。

---

## 3. 核心 gap

### G1. Knowledge availability 被误当成 mastery

当前结构容易隐含：

```text
project theory written into Skill
→ model reads it
→ model understands it
→ model recognizes when it applies
→ model behaves accordingly
```

其中每一条箭头都需要单独证据。

理论文本可以是正确的，但 model 可能：

- 没有在当前 task framing 中认为它相关；
- 只复述概念，不改变 judgment；
- 过度泛化，导致过度干预；
- 理解 procedure 却无法区分 boundary case；
- 在长上下文后失去该 representation 的 salience。

### G2. Selector bottleneck

Conditional Skill 需要模型先依据 name/description/context 判断 relevance，再加载 richer body。

但复杂协作理论的价值之一恰恰是改变“什么值得注意”。因此：

> **recognition 所需的知识可能在 selector 后面。**

增加 description 长度可以提高 recall，却也可能增加 semantic overlap、selector entropy 与 false positive。把全部 recognition logic 放回 resident kernel 又会重建 context saturation。

### G3. Static Skill 缺少 practice return edge

当前 Skill 通常是固定 artifact：

```text
episode A
→ Skill

episode B
→ same Skill

episode C
→ same Skill
```

除非人手工修改文件，否则系统不会因为过去“什么 cue 有效 / 什么 description 漏触发 / 哪个例子导致误用”而改善未来行为。

因此它更像 repeated manual presentation，而不是 cumulative proficiency。

### G4. Theory ontology 与 procedural representation 被混在一起

一个 canonical theory object 应优化完整性、证据、边界与可修订性；一个 runtime procedural representation 应优化 recognition、discrimination、action usefulness 与 context efficiency。

把前者压缩成 Skill，并期待它同时承担后者，会产生双重失真：

- 过度压缩可能丢掉 theory nuance；
- 为保真而写太长又会变成 runtime textbook。

### G5. 当前 carrier 低估 base-model capability

很多协作能力可能已经存在于模型中，只是 activation/reliability 不足。如果如此，完整教程式 Skill 会重复模型已有能力并增加 reasoning burden。

Carrier 需要先分辨：

```text
not capable
vs
capable but not activated
vs
capable but poorly discriminated
vs
capable but missing project-specific knowledge
vs
capable but missing persistence
```

当前 static package 很难表达这些不同问题。

### G6. Context timing / ordering 没有成为显式设计变量

理论在任务之前进入 context、任务之后进入 context、在长任务中被 reactivated，可能产生不同 representation。

当前 Skill 结构主要把“加载时机”交给 relevance routing，却没有独立研究：

- orientation before task framing；
- task-first selective retrieval；
- long-context attention refresh；
- active vs automatic context construction。

### G7. “AI 自己读项目再工作”的能力没有被利用

当前 Skill 主要向模型提供预编译 representation。Cloud field impression 提示另一条路线：让模型主动阅读 canonical project material、构造自己的当前 representation，再进入任务。

这可能利用模型已有的 retrieval、analogy、instruction induction 与 in-context adaptation，而不是要求 Skill author 预先完成所有 theory-to-runtime compilation。

当前证据不足以断言这条路线更好，但 carrier 没有把它作为 first-class option。

### G8. Experience 没有被表示成 model-specific guidance evidence

即使当前 pilot 出现稳定失败/成功，也主要被人解释后手工修改 carrier。

缺少一个明确对象：

> 在 model M、state S、theory T 下，guidance G 产生了 behavior/outcome O。

没有这个对象，B1/B2、field pilot、Skill description 误触发等经验难以积累成可复用的 runtime knowledge。

---

## 4. 这与旧 Skill-learning diagnosis 不同

[`skill-learning-capability-gap.md`](../../cognitive-coordination/design-diagnoses/skill-learning-capability-gap.md) 的核心问题是：**对人的学习与责任相关能力支持，仍主要依赖条件式 Skill 触发和人的 metacognitive labor。**

本 diagnosis 的对象是另一条轴：

> **AI carrier 本身如何把项目 theory 变成可靠 runtime capability。**

两者可以互相支持，但不应合并：

- 一个 AI carrier 可以很好激活 collaboration reasoning，却仍错误地替代 human learning；
- 一个 Skill 可以很好保护 human construction，却仍只在错误 selector 条件下触发。

---

## 5. 候选修正方向（不是 vNext 方案）

当前更合理的研究方向不是立刻增加更多 Skill，而是测试一组互补机制：

### P1. Resident layer 只保留 high-leverage invariant / activation cue

优化 semantic leverage，而不是理论完整度。

### P2. 增加 model-active orientation

在适当任务起点，让模型主动查询项目 map / canonical knowledge，形成当前任务所需的 collaboration representation。

### P3. Skill 缩窄为 procedural / reactivation surface

让 Skill 更强调：

- observable recognition cues；
- discriminating examples/counterexamples；
- how-to-use；
- boundary/no-op；
- canonical return links。

### P4. Canonical corpus 保持独立

不把全部 theory 复制进 Skill。通过 connector/MCP/search/repository access 进行 targeted retrieval，并保持 provenance。

### P5. 把 context order / timing 变成 assurance variable

测试 theory-first、task-first、orientation→task→reactivation 等不同轨迹。

### P6. 建立 guidance experience object

保存经过评估的 model-specific elicitation evidence，并允许它改进 cue/procedure/retrieval，而不是直接改 canonical theory。

### P7. Model substitution test

同一 candidate carrier 在不同强度/家族模型上运行，观察哪些 scaffold 随 base capability 增强而失去价值，从而识别 temporary compensator。

---

## 6. 不应立即做什么

本 diagnosis 当前不支持：

- 删除 resident kernel；
- 删除 Skills；
- 把全部项目知识在每次会话开始时全部加载；
- 自动让 AI 修改 Skill / theory；
- 建立复杂 memory/MCP 系统后再验证需求；
- 把 cloud 主观体验当成 causal proof；
- 把 Phase B 解释成“简短 prompt 永远最好”。

合理的下一步是通过 discriminating study 找出每种机制实际提供的 marginal capability。
