# 选择性跨层认知探针：历史证据回放与边界测试（2026-08-30）

> 地位：**project study / candidate-mechanism replay**。本记录用于检验“选择性跨层认知探针”是否比现有模糊的“按需下潜 / 适度展开”提供更强的解释、判别与设计价值；它不是 current spec，也不自动修改 live Skill。
>
> 来源：2026-08-29～30 关于抽象层、表示、学习、重建与 cognitive coordination 的连续项目讨论，并回放现有 Issue、feedback、Skill eval 与 research artifacts。

## 1. 决策相关未知

真正待判别的是：

> **当当前模型已经足以生成有意义的下层或异质表示时，是否应该允许 AI / 人暂时构造一个选择性的 epistemic probe，用它暴露、区分或重组当前模型，再把少量 consequential delta 带回当前焦点，而不把这种下潜误写成阶段切换、实现承诺或无限细化？**

如果该候选只是把现有“按需下潜、短反馈、认知分配”重新命名，则不值得成为独立机制。若它能产生现有文字难以稳定推出的新判断，则值得继续验证。

## 2. 冻结候选

### 2.1 任务表示图，而非认知阶梯

任务理解不视为沿单一抽象梯逐层完成，而视为多个**局部、可修正、可外化的 task representation** 形成图状关系。

节点可能包括业务目的、不变量、领域模型、流程模型、架构、接口、数据、代码、运行证据、数学/拓扑/形式结构，以及外部成熟概念或标准。

边可以表达：

- 上层对下层的约束、purpose 或 means-end；
- 下层对上层的证据、反例或修正；
- 表示之间的 translation / re-representation；
- 某结构对外部知识的 indexing / retrieval；
- 某桥接关系对未来理解的 reconstruction cue。

软件开发 L0–L4 仍可作为 domain routing heuristic，但不是认知模型必须逐级经过的唯一拓扑。

### 2.2 选择性跨层认知探针

在保持当前 workflow focus / focal cognitive question 的前提下，当另一表示预计能以更低总成本暴露 consequential relation 时，可以暂时构造、操纵、检查或检索该表示。

~~~
focal model M0
    ↓
identify uncertainty U
    ↓
select epistemic probe P
    ↓
externalize / discriminate / contact evidence / expose concept
    ↓
extract consequential delta Δ
    ↓
integrate Δ back into M0
    ↓
revise / bound / restructure / leave explicit unknown
    ↓
M1
~~~

**Probe 本身不改变 workflow focus，不自动进入实施，不自动取得行动授权。**

### 2.3 Epistemic return edge

一个 supporting branch / lower-level excursion 应存在返回关系：

> 为什么进入该表示，以及什么新关系会被带回当前焦点？

若探索持续产生自己的目标而不再服务当前 focal question，它可以升级为 independent branch；若既无返回价值也未成为明确新目标，则更像 distraction / agenda drift。

### 2.4 深度选择

不要求“只下一层”。选择依据是预计的 discriminating / model-building value 与 cognitive cost，而不是 adjacency。

但每次 probe 应尽量只承担一个主要 epistemic purpose，并在带回 delta 后重新判断是否需要第二次探针，避免一次下潜同时引入过多转换和整合负荷。

## 3. 与 cognitive-coordination 操作的关系

候选不是新增用户工作流，而是把现有操作组合成一个可运行的控制机制：

- **cognitive allocation**：哪里值得花认知资源；
- **externalization**：把隐藏关系变成可观察表示；
- **discrimination**：让 competing models 产生不同后果；
- **evidence contact / strategic exposure**：接触会改变判断的直接结构；
- **revision / bounding**：把 probe 结果带回当前模型；
- **activation / reconstruction**：保留少量 bridge cue，使未来可重新生成推理路径；
- **productive divergence**：probe 也可让不同解释更清楚，而不是强迫立即收敛。

## 4. Competing explanations

### H1 — cross-level epistemic control

历史失效的一部分来自 workflow focus、abstraction depth、representation 与 action commitment 被错误绑定；缺少“有 return edge 的选择性下潜”这一控制概念。

### H2 — existing norms are sufficient

现有“按需下潜 / 小批量闭环 / 充分即停止 / 表示服务关系 / 认知分配”已经足够；新模型只提供漂亮解释，不改变行为。

### H3 — generic overload only

问题主要只是信息太多、文字太长或 working-memory burden；只需缩短、分片或减少讨论。

### H4 — phase management only

软件案例主要是 phase / next_action / authorization 管理错误；只需更严格阶段边界，不需要 task-representation co-evolution。

## 5. 历史证据回放

### C1 — Issue #5：实施讨论“粗骨架 + 整包点头”过早闭合

粗骨架降低初始负荷，但随后把整套方案作为待批准草案，关闭进一步下潜入口。

H3 能解释负荷需要控制，H4 能解释阶段未正确退出，但两者不能很好回答：为什么不是继续在同一架构层补更多文字，而是有时应该用一个更具体的调用、状态、映射或反例来帮助人形成更清楚的上层实施判断？

H1 给出不同设计：保持 implementation-discussion focus；选择一个最有判别力的局部 probe；只带回改变方案判断的 delta；不把 probe 变成代码实施。

**结果：supports H1 as a design discriminator。**

### C2 — IF-038：讨论阶段交融被误读为可编码

task understanding 与 implementation discussion 可以交融，但 AI 一度把“讨论不形式分关”解释成可以开始编码；入参、覆盖、配对等承重语义仍未闭合。

这直接支持：workflow-focus transitions 与 representational depth / action commitment 不是同一维度。

H4 能说明“不能过早编码”，但 H1 进一步允许：即使仍在 task-understanding / discussion focus，也可以检查代码、架构或调用链作为 epistemic probe，只要未把结果固化为真实系统承诺。

**结果：strong structural support for orthogonality; not proof of effectiveness。**

### C3 — Issue #10：未验证上游前提便推进下游保障设计

AI 以技术连续性替代认知顺序，有限抽查后直接推进 assurance design；人拉回仓库审查后才发现真实结构问题。

H1 提供重要反例：向下或向后续模型移动只有在 probe 有明确 epistemic return edge 时才合理；技术路径连续本身没有认知授权。

**结果：supports a necessary boundary / falsification guard。**

### C4 — Issue #9：学习插槽需要动态调节

同一个人在业务错误语义、语言 API、编译模型、DI、机械检索等不同抽象/任务位置上需要不同支援；固定练习层级失真。

H1 与 current capability model 可以共同推出：probe target depth 与 representation form 应按当前 capability evidence 选择；实践不是为了“做题”，而是为了让某个关系可外显、可判别或可迁移；低价值机械动作可继续委托 AI。

H3 只能说“别让人太累”，无法选择什么 action 值得保留。

**结果：supports H1 + capability coupling。**

### C5 — Issue #2：完整候选清单让人从建构滑向选择

AI 一次给出完整候选框架，人的任务退化为接受 / 删除 / 补漏。

该案例提供 probe-size 边界：epistemic probe 应是未闭合、局部、可产生关系的材料；一次构造完整 lower / alternate representation 可能反而提前封闭人的模型建构。

**结果：supports bounded probe size; rejects “more representation is better”。**

### C6 — Issue #1 / reconstruction-surface：固定 goal/now/next 不足

后续研究已发现恢复线索应按实际 reconstruction risk 选择，并允许为空。

H1 产生新解释：高价值 cue 不只是状态字段，而可能是 bridge relation，例如：

~~~
business invariant
→ discriminating example
→ architecture consequence
~~~

未来看到其中一个节点时，可以重新激活推理路径。该 cue 也可能成为外部知识的 retrieval / index key。

**结果：supports a cross-time consequence of H1; delayed human reconstruction remains unvalidated。**

### C7 — side-chat rejoin collision

Side chat 可以支持理解，但主线程恢复时，人可能同时承担主线恢复、旁支收束和 reconciliation。

H1 给出 branch criterion：supporting branch 有 epistemic return edge；independent branch 有自己的目标；UI / side chat 只是可能的 carrier，不是机制本身。

该案例也警告：即使 branch 有认知价值，其 interaction-management cost 也可能使总收益为负。

**结果：supports return-edge concept + cost boundary。**

### C8 — negative cases

当前 Skill eval 已明确要求低风险机械事项直接处理，简单事实不启动工作流，已有上下文不反复展示恢复视图。

若 H1 导致每次都构造另一表示、每个概念都要求实践、每个阶段都必须下潜一次，则它失败。

**结果：H1 must be event-triggered and allowed to choose no probe。**

## 6. 判别结果

### 6.1 H1 不是纯粹重命名

现有规范确实已经包含按需下潜、表示服务当前关系、小批量反馈、认知分配、充分相对于目的，以及不让技术连续性替代议程。

但这些规则仍留下一个实际歧义：

> **怎样判断“按需”？为什么这次应该换到另一个抽象 / 表示，而不是继续当前层？换了以后是否意味着进入下一阶段？什么时候必须回来？**

H1 提供了至少四个现有文本没有清楚组合出的判别条件：

1. workflow focus 与 representational depth 正交；
2. probe 选择看 epistemic / discriminating value，而非层级 adjacency；
3. lower / alternate representation 默认是 epistemic probe，不是 implementation commitment；
4. supporting excursion 需要 epistemic return edge。

因此当前结果更接近：

> **H1 提供了对现有 norms / guidance 的机制性解释与一个真实 runtime control abstraction；它不是新价值原则，也不需要被写成人可见流程。**

### 6.2 “只是认知负担”不足

正确处理不总是“更短”。有时需要一个更具体的例子、直接证据、形式模型或人的实际小动作；有时应完全不增加表示。

目标应是提高 information / model-change value per cognitive cost，而不是机械减少内容。

### 6.3 “只是阶段管理”不足

阶段管理能阻止未经授权的实施，但不能回答 task understanding 中是否可以看代码、learning 中是否应该做实践、business model 是否可以借 formal model 修正、如何选择非相邻 abstraction，以及如何把 probe 结果转成未来 reconstruction cue。

## 7. 最小控制模型

~~~
Focal concern F
    ↓
Is there a decision-relevant uncertainty U?
    ↓ no → continue current representation
    ↓ yes
Would another representation likely expose U
more effectively than further same-representation reasoning?
    ↓ no → continue / seek evidence in place
    ↓ yes
Select minimal probe P
(depth × domain model × representation × action amount)
subject to capability, risk and cognitive cost
    ↓
Observe consequential delta Δ
    ↓
Return Δ to F
    ↓
revise / bound / restructure / preserve unknown
    ↓
optionally retain one high-value bridge cue
    ↓
stop; another probe needs another reason
~~~

这只是后台控制模型，不是逐项 checklist。

## 8. 候选失效模型

1. **same-representation saturation**：当前表示已能生成高信息 probe，却继续同层穷举；
2. **premature concretization**：probe 被静默当成实现承诺；
3. **probe overload**：新表示的转换 / 整合成本超过判别价值；
4. **depth ritual**：机械“下一层”，不按信息价值选 representation；
5. **missing return edge**：探索没有带回当前 focal model；
6. **representation fixation**：方便的下层模型反向扭曲业务问题；
7. **cue pollution**：保留过多 hook，未来重建反而更难；
8. **capability mismatch**：probe 使用了人无法有效整合的表示；
9. **agenda drift**：supporting branch 静默变成新目标；
10. **false epistemic action**：动作只是忙碌 / 练习形式，没有新增模型或证据价值。

这些目前是 candidate failure modes，不自动加入 current failure-model catalog。

## 9. 对 AI recovery 的边界结论

本次回放进一步支持把三类问题拆开：

### A. AI / task-context continuity

历史 state.json、恢复顺序、上下文迁移等属于 host / product / agent infrastructure concern。项目可以声明依赖“足够的 task / context continuity 与 provenance”，但不应把自建 AI memory / recovery protocol 视为核心人机协作理论。

### B. Claim / source conflict

文档、代码、人的确认、AI 推断冲突时如何判断 authority / evidence 仍属于 project epistemology，不能删除。

### C. Human model reconstruction

如何用少量 cue 让人重新生成足以判断、预测或行动的模型属于 cognitive coordination，而且可能从 recovery-time 问题扩展为 **reconstructability-by-design**：

> 初次理解时形成的 bridge relation，可以同时服务当下模型修正和未来重新激活。

因此不建议继续把 state / conflict / recovery 作为一个统一 Skill concern。

## 10. Skill refactor branch 的地位

当前 live Skill 已积累来自多个阶段的补丁与 reference，并包含明显 host-specific state / recovery 语义。新的认知模型尚未成为它的整体组织原则。

因此“重构一个能反映当前项目成果的 Skill”应建立为 **independent branch / implementation inquiry**，而不是在本研究里直接修改。

它与本研究有双向 return edge：

~~~
cognitive model
→ derives candidate runtime behavior
→ future Skill refactor
→ field / runner behavior
→ evidence
→ revise cognitive model
~~~

Skill 可作为 validation carrier，但不应反过来让“Skill 好不好写”决定认知模型是否成立。

## 11. 下一证据层

本轮是 historical replay，能支持“该机制具有新增判别价值”，不能支持“该机制在运行时提高效果”。

下一步最低成本证据路线：

1. 从真实开发中捕捉 2–3 个自然出现的 probe opportunity；
2. 记录 native / current-Skill 实际是继续同层、整包收敛，还是选择了有 return edge 的 probe；
3. 若存在可区分争议，再构造少量 runner cases 比较 current Skill、current Skill + minimal cross-level control，以及 over-trigger negative case；
4. 优先观察：首次机会是否选择高信息 probe；人是否需要主动要求“换个表示 / 看代码 / 举个例 / 别直接实现”；probe 是否真正产生 delta 并回到 focal model；是否降低同层认知饱和而不增加 integration burden；是否产生 fixation / agenda drift；
5. human reconstruction / delayed learning 需要跨时间证据，不能由即时主观“更清楚”证明。

## 12. 当前判断

本轮结果支持把该候选从“对话中有吸引力的概念”提升为：

> **cognitive-coordination research program 内值得独立验证的 candidate control mechanism。**

它当前最有价值的贡献不是增加原则数量，而是把 selective / on-demand / appropriate depth 这类容易产生解释分歧的规范语言，连接到一个可被讨论、实现、反驳和测试的后台判断模型。

尚不足以写入 current universal norms、把所有 abstraction hierarchy 改成 graph ontology、重构 live Skill、宣称实践 / preview / cross-level probe 普遍提升学习，或宣称 human reconstructability 已被验证。

下一步应继续按 decision-driven evidence cycle 取得运行证据，而不是再扩大理论边界。
