# Runtime capability formation：从静态理论注入到模型能力协调

- **日期**：2026-09-06
- **状态**：`candidate / research model`（不是当前规范，不直接规定最终 carrier architecture）
- **来源**：2026-09-02～06 项目讨论中对 21 个 heuristic clues 的扩展/收敛、当前 resident kernel + conditional Skill 的 field impression、Phase B 解释，以及 in-context learning、agent memory、dynamic skill、prompt/program optimization 等外部研究线索
- **关联**：[`../cognitive-coordination/model.md`](../cognitive-coordination/model.md)、[`../assurance/studies/v2/assurance-v2-phase-b-interpretation.md`](../assurance/studies/v2/assurance-v2-phase-b-interpretation.md)、[`design-diagnoses/static-context-carrier-gap.md`](design-diagnoses/static-context-carrier-gap.md)、[`evidence-review.md`](evidence-review.md)

## 一句话主张

项目理论转化为运行时能力，不应被理解成“把完整理论写进 prompt/Skill”。对于一个已经具备较强一般能力、但参数通常不可由项目直接修改的模型，更合理的候选问题是：**如何以最小外部结构，让相关潜在能力和项目特定知识在正确情境中被识别、构造、检索、重激活、验证，并让历史运行证据改善未来引导。**

---

## 1. 起点：知识可用不等于能力组织

当前 carrier 的一个基本假设是：只要理论以 resident rule、Skill body 或 reference 的形式在运行时可见，模型就能在需要时把它转化为正确行为。

本轮讨论形成一个更强的候选区分：

> **knowledge availability ≠ capability organization**

“知道一个理论”“能解释一个理论”“能在陌生情境中识别它适用”“知道如何操作它”“能区分边界/反例”“能在长期运行中越来越稳定地使用它”是不同能力。

人类专家类比只用于暴露结构，而不是声称 AI 以相同机制学习。专家熟练度通常不是逐字保存一本理论手册；它更像概念、例子、反例、recognition cues、程序、失败模式和应用边界形成相互连接的组织。静态 Skill 更接近每次给一个能力较强的学生一份 manual，并要求其先凭简短 description 判断要不要打开，再临时学习和执行。

这个类比提示：当前问题可能不只是“Skill 写得不够好”，而是 carrier 把理论掌握中多个不同环节压缩成了一次 context injection。

---

## 2. 三个能力位置

本模型暂时区分三种 capability locus：

### 2.1 Parametric capability

基础模型训练后已经拥有的一般知识、语言能力、关联、推理模式与任务程序。项目不能假定这些能力弱，也不应重复外置已经可靠存在的认知。

### 2.2 Context-conditioned capability

模型在当前 inference context 中，因指令、例子、理论阅读、任务证据、历史记录或模型自己主动检索/重述而形成的临时工作表示与行为倾向。

它不等于模型权重改变，但可能显著改变模型如何解释后续任务、调用既有能力和组织推理。

### 2.3 Externally persistent capability

跨会话或长任务可持续存在的外部结构，例如 canonical project corpus、resident cues、Skill/程序、retrieval index、episodic records、validated guidance、evaluation history 与其他 memory/service。

候选架构不应默认第三层越强越好。更合理的目标是：外部结构补足 parametric/context-conditioned capability 无法稳定承担的部分。

---

## 3. Intrinsic-first：先识别模型—项目能力边界

在为某一项目机制增加外部复杂度前，先问：

1. 基础模型是否已经会做这件事？
2. 它是否会在没有提示时稳定做？
3. 一个很小的 semantic cue 能否可靠激活它？
4. 它主要缺少的是 recognition、discrimination、project-specific knowledge、grounding，还是 persistence？
5. 外部结构的增量是否高于 token、延迟、attention dispersion、ritualization 与 anchoring cost？

因此同一个 collaboration construct 可能落在不同情况：

```text
already strong
→ no external intervention

latent but not reliably activated
→ compact cue / orientation

can act but discriminates boundaries poorly
→ examples / counterexamples / procedural support

project-specific or evidence-sensitive
→ targeted canonical retrieval

requires cross-session accumulation
→ external memory / validated guidance
```

这构成候选的 **model–project capability boundary**。Carrier 不应把某一代模型的暂时短板固化成普适协作原则；model substitution 应成为未来验证方法之一。

---

## 4. Recognition 是独立能力

Skill 系统常隐含：

```text
current context
→ short description decides relevance
→ load richer Skill
```

但很多复杂理论的价值恰好在于改变“什么看起来相关”。如果识别 applicability 所需的丰富知识被放在 Skill 内部，就出现一个 selector bottleneck：模型需要先识别相关，才能获得帮助它识别相关的内容。

因此本模型把 **knowing when** 与 **knowing how** 分开：

- recognition：当前情况与哪些理论、先例、风险或程序可能相关？
- operationalization：一旦相关，什么 distinctions、questions、evidence contact、procedures 或 no-op 才有价值？

未来系统可以让 resident cues、orientation、retrieval、examples、Skill descriptions 与历史 cases 共同承担 recognition，而不是强迫一个静态 description 完成全部路由。

---

## 5. Context 不只是容量，而是状态构造

Context engineering 在本 program 中不只指“少放一些 token”。一个工作上下文至少有这些变量：

```text
content
selection
order
 timing
persistence / refresh
who constructs it
```

尤其区分：

- **situation/task context**：目标、证据、约束、环境、承诺与未知；
- **collaboration context**：角色、授权、责任、认识论边界、相关项目理论；
- **resource context**：Skill、工具、retrieval interface、workflow；
- **history context**：过去决定、失败、validated guidance、未解决分支。

这些 context 不是天然互斥。Collaboration context 可能改变 task representation，从而产生正向交互；也可能因过长、过度显著或无关而分散任务注意。

因此提出候选概念 **context orchestration**：

> 在协作轨迹中，管理上下文的构造、顺序、主动探索、重激活、压缩与丢弃，使模型在当前阶段保持最有价值的工作表示。

这比单轮 prompt engineering 更接近一个 temporal control problem。

---

## 6. Model-active context construction

本轮 field impression 中，一个重要对比是：

```text
local carrier:
resident kernel + conditional Skill

cloud workflow:
先通过 GitHub connector 主动阅读项目相关内容
→ 再进入具体协作
```

后者的主观表现明显更接近项目理论。这个观察不能证明因果，但产生一个可检验 hypothesis：

> 与“被动注入预编译理论”相比，让模型先主动检索、阅读、比较和构造自己的当前表示，可能更有效地激活 parametric capability，并让理论在任务 framing 形成前进入工作状态。

这不是把 AI in-context adaptation 等同于人类 active learning。更保守的候选术语是 **model-active context construction**：模型通过检索、解释、生成例子、识别疑问或选择下一份材料，参与构造后续 inference 所依赖的上下文。

候选 ordering 包括：

```text
theory → task

task → theory

compact orientation → task → relevant reactivation

minimal task signal → active theory orientation → full task
```

顺序本身应视为实验变量，而非固定礼仪。

---

## 7. Skill 的角色被缩窄，而不是被否定

本模型不推出“主动阅读取代 Skill”。Skill 可以承担不同的编译后角色：

- 稳定、重复、窄范围的程序性知识；
- examples / counterexamples / boundary conditions；
- 长上下文中的 attention refresh / reactivation；
- 对 canonical corpus 的导航入口；
- 被运行证据证明足够可靠后的 compact shortcut。

因此一个 Skill-like artifact 更可能是：

> **how to think/use here 的 procedural representation**

而不是：

> **完整理论 ontology**。

这也意味着 Skill 可能是学习/验证后的产物，而不是理论转化的起点。

---

## 8. Canonical knowledge、retrieval 与 external state

项目完整理论应优化 fidelity、provenance、revision 与 authority，而不是每轮 context efficiency。Canonical corpus 可以通过 targeted retrieval 提供 return edge：当 compact cue、Skill 或模型自构表示不够确定时，回到权威来源。

MCP、connector、search tool 等在这里主要是 access surface；它们本身不是 knowledge/memory architecture。实际 state 可以由 repository、index、case store、evaluation records 或其他 service 持有。

Retrieval 的问题也不只是“有没有这份文件”，而包括：

```text
是否知道要找
用什么 cue 找
找到哪一层 representation
什么时候继续深挖
什么时候返回当前 task model
```

因此 retrieval 与 recognition/cognitive allocation 有直接关系。

---

## 9. Guidance experience：经验可以描述如何引导模型

对于一个已较强的模型，跨任务积累的高价值 experience 不一定是“重新教会它理论”。一个更适合本项目的候选对象是 **guidance / elicitation experience**：

```text
(model M,
 collaboration state S,
 relevant theory T,
 guidance/context G,
 behavior B,
 observed outcome O)
```

它记录：在什么模型和情境下，哪种 cue、context order、example、procedure、retrieval、question、tool call 或 no-op 更容易产生期望的 collaboration behavior。

例如 Phase B 可以被重新读取为一种早期 guidance evidence：短 resident semantic boundaries 似乎能稳定部分 base capability，而更复杂的 runtime reasoning scaffold 没有显示稳定、成本相称的额外行为收益。

这类经验最终可能改进：

- resident activation cues；
- Skill description / procedure；
- retrieval index；
- context ordering；
- model-specific routing；
- future study design。

但它不应直接覆盖 canonical theory。

---

## 10. External learning loop 与验证边界

如果模型权重不变，项目仍可能通过外部 state 形成 **system-level learning**：

```text
runtime episode
→ preserve observation
→ reflection / candidate explanation
→ compare across cases
→ behavioral validation
→ promote to reusable guidance / recognition cue / procedure
→ future behavior changes
```

关键是：

> `runtime experience → theory` 不应存在无验证直连。

模型可能错误解释成功/失败，也可能将语义相似但行为机制不同的 cases 过度抽象。因此需要区分：

- episode；
- reflection；
- recognition cue；
- procedural abstraction；
- guidance evidence；
- canonical theory revision proposal。

不同对象需要不同 admission threshold、provenance 与 rollback 能力。

---

## 11. 薄实现、强架构

当前候选方向不是建立一个与基础模型竞争的“第二大脑”。更可能的目标是：

```text
capable pretrained model
        │
        ├─ compact resident orientation / invariants
        ├─ model-active orientation and retrieval
        ├─ procedural / reactivation surfaces
        ├─ canonical external knowledge
        ├─ validated guidance / experience state
        └─ assurance / evaluation
```

外部层主要负责：

- activation；
- context assembly；
- grounding；
- persistence；
- validated accumulation；
- invariant control。

模型仍承担大部分 situated reasoning。Architectural richness 因此不等于每轮运行时都加载更多内容。

---

## 12. 与 cognitive coordination 的关系

Cognitive coordination 研究 activation、externalization、discrimination、evidence contact、revision、reconstruction、strategic exposure、productive divergence、cognitive allocation 与 cross-representation probing 等认知函数。

Runtime capability program 研究另一个问题：

> **在真实模型/host/carrier 中，什么机制让这些函数在适当时机可靠出现？**

例如：

- `reconstruction` 是 cognitive construct；如何让 AI 在长上下文/跨会话中恢复相关 representation，是 runtime capability 问题；
- `cross-level probing` 是认知控制；什么 resident cue 或 retrieval policy 能及时激活 probe，是 runtime capability 问题；
- `responsibility-capability` 是 collaboration/cognitive concern；某模型是否只需一个 cue 就能识别它，则属于 model–project capability boundary。

两者可相互引用，但不互相吞并。

---

## 13. 当前最重要的可检验假设

### H1 — capability elicitation > theory repetition

当基础模型已拥有大量相关 general capability 时，compact discriminating cues / examples / orientation 可能比完整理论重复注入具有更高的行为增量/成本比。

### H2 — model-active orientation has independent value

在信息量近似相同的情况下，让模型主动检索/阅读并形成当前表示，可能不同于自动注入相同内容；差异可能来自 task representation construction，而不只是可用 token。

### H3 — ordering changes collaboration behavior

`collaboration context → task`、`task → collaboration context`、`orientation → task → reactivation` 可能产生不同的 task framing、intervention rate、miss rate 与 cost。

### H4 — recognition deserves independent evaluation

Skill/procedure body 正确不代表 runtime capability 成立；必须单独测是否在需要时被激活、在不需要时保持 no-op。

### H5 — validated guidance can accumulate without weight updates

跨案例保存和验证 model-specific guidance，可能使 system-level behavior 随时间改善，即使基础模型参数未变化。

### H6 — stronger models should require different external scaffolds

如果某机制只补偿特定 model generation 的短板，则 model substitution 后其增量应下降；这可帮助区分 universal collaboration requirement 与 implementation compensator。

---

## 14. 当前不做的结论

本模型目前**不证明**：

- 主动阅读普遍优于 Skill；
- 某种 memory graph / vector store / MCP 是最佳实现；
- context ordering 有唯一固定最佳顺序；
- foundation model 中存在可由某个关键词确定性调用的“理论模块”；
- 系统应让 AI 自主修改 project theory；
- 最终 carrier 必须包含所有上述层；
- 人类学习机制可以直接映射到 Transformer inference。

这些都需要进一步 study。
