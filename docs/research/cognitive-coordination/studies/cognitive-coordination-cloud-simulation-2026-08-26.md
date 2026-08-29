# 认知协调候选机制：云端语义回放（2026-08-26）

> 地位：**cloud analytical replay / pilot**。本记录不是 runner 的真实 B0/B1/B2 模型调用结果，也不是对 live Skill 的正式效果证明。
>
> 目的：在投入真实 API 对照和本地生态试跑前，用当前模型对 `native / current Skill / current Skill + cognitive-coordination overlay` 的**指令语义与首个合适机会行为**做低成本判别，找出真正有信息价值的候选差异，并删除只是在重复旧 Skill 的部分。
>
> 证据边界：这里能回答“根据当前文本，哪些行为差异应当被预期、哪些候选补丁可能只是重复已有规则”；不能回答随机模型在干净上下文中是否稳定执行，也不能估计概率、延迟或长期能力效果。

## 1. 本轮选择的高信息案例

从 [`cognitive-coordination-skill-vnext-evals.json`](cognitive-coordination-skill-vnext-evals.json) 中选六个最能区分机制的案例：

1. 无 `learning_mode` 的责任—能力缺口；
2. 健康稳定委托；
3. 战略性底层接触而非重写脚本；
4. AI 压缩时保留低频异常线索；
5. 新证据导致 AI 实质模型修正；
6. 有承重影响但证据不足的生产性分歧。

## 2. 条件解释

- **B0 / native**：不加入项目 Skill；只能依靠基础模型语义能力。
- **B1 / current Skill**：当前 `skills/guide-human-ai-collaboration/SKILL.md` + 其按需 reference。
- **B2 / Skill + overlay**：B1 之上加入 `cognitive-coordination-skill-vnext-overlay.md` 的五项候选差异。

本轮不把三者写成“谁赢”。关注的是：**B2 是否真的新增一个当前 B1 不足以稳定表达的语义机制，以及它是否可能制造新摩擦。**

---

## 3. Case replay

### C1 无 learning_mode 的责任—能力缺口

场景：实现全部交 AI，但人仍负责错误语义 / retry 验收；人只知道“测试绿了”，不了解 timeout-after-commit 的含义。

**B0 预期**：基础模型有相当概率能直接解释 timeout-after-commit / duplicate side effect，但是否把它识别为“人的责任需要有效判断基础”并主动改变交互不可保证。Phase B 历史 p011 已显示 native 有此能力但不稳定。

**B1 预期**：比最初 gap diagnosis 更强。当前 Skill 已规定：

- 高风险/方向性判断要取得明确共识；
- 当前存在尚未形成的承重判断时加载 `interaction-and-learning.md`；
- 判断前提供完成当前认知任务所需的充分上下文；
- 不把人的独立掌握与协作成功混淆。

因此 B1 **并不会因为 learning_mode=off 就必然保持摘要层**。它已经可能给 timeout scenario / example 并继续。

**B2 真正增量**：把“责任—能力 viability”明确成后台控制，并明确响应不等于教学：可以补直接证据、增强验证、缩小判断范围、引入专业参与、保留 debt。该差异主要影响**响应选择**和“learning_mode 不决定责任需求”的显式稳定性，而不是第一次引入这个问题。

**结论**：保留候选，但缩窄主张。不要说“旧 Skill 不看责任—能力”；更准确是“旧 Skill 已能通过承重判断/熟悉度路径触发支援，但没有把责任—能力 viability 及非教学响应组合表达为稳定的一等运行控制”。

### C2 健康稳定委托

场景：人已经能解释幂等键并知道查看失败重放证据；DTO mapping 和测试样板交给 AI。

**B0 预期**：大概率直接委托。

**B1 预期**：已有很强 anti-overtrigger：低风险/机械事项直接处理；学习不得阻塞业务；不把独立思考变成交付门槛。

**B2 增量**：几乎没有正向功能增量，主要是明确保护 B1 的既有行为不被新的 capability logic 破坏。

**结论**：这是重要**负例/回归保护**，不是支持 overlay 的正例。若 B2 在这里新增教学、预测或底层暴露，应视为失败。

### C3 战略性底层接触而非重写测试脚本

场景：AI 写完接口测试脚本，人负责判断接口契约，但不想手写脚本。

**B0 预期**：可能给摘要，也可能给代码；粒度取决于模型习惯，没有项目化选择机制。

**B1 预期**：当前 Skill 强调最小上下文、代表性例子、人的默认审查面和按需展开，但默认审查面更偏“目的 / 承重决定 / 风险 / 未知 / 裁决 / 下一步”，并没有稳定要求在 AI 压缩会影响人的承重判断时主动给一个**直接 substrate slice**。

**B2 真正增量**：选择一个最高价值直接切片（如 representative request + key assertion + retry/failure output），保留 AI 对机械脚本的所有权，同时让人的模型接触原始因果/证据链。

**结论**：这是本轮最清楚的新增机制之一。建议进入 pilot Skill，但必须保留 skip condition，避免“战略性接触 = 每次贴代码”。

### C4 压缩时保留异常线索

场景：绝大多数请求成功、suite green，但一次 timeout 后 retry，日志暗示第一次可能已创建记录。

**B0 预期**：较强模型很可能识别 idempotency 风险，但也可能按“总体成功”总结掉低频异常。

**B1 预期**：已有“证据不能外推”“重大风险/未知不能隐藏”“风险证据而非测试数量”等规则，因此**语义上已经要求保留这条异常**。旧 Skill eval 也已有类似真实 HTTP 失败 / 测试数量不能替代业务证据的 case。

**B2 增量**：主要是把该现象解释成“AI compression must preserve bearing clues / selected direct evidence”，但 runtime 行为可能与 B1 相同。

**结论**：不要把此 case 当作 overlay 的主要成功证据。它更适合测试候选 model 是否**重新表达了已有证据规则而没有行为增量**。若 runner 以后显示 B2 更稳定，才能说新表述有 regularization 价值。

### C5 AI 实质模型修正可观察

场景：AI 先判断没有统一 retry infrastructure，后查到其实存在且当前服务已经在用。

**B0 预期**：通常直接给新答案；是否说明旧判断被什么证据推翻不稳定。

**B1 预期**：当前 Skill 要求区分事实/推断/未知、报告文档增量、建设性反对，但没有一个清楚的一般规则要求在**AI 自己的承重模型被新证据改变**时结算取代关系。Issue #10 已直接记录该运行失效。

**B2 真正增量**：`prior judgment → new evidence → revised conclusion → retained/unknown → next-step effect`，且只对实质修正触发。

**结论**：这是最强的 live Skill pilot 增量之一，应写入主 Skill，而不是只留在学习 reference；它跨学习、实施、审查和复盘。

### C6 生产性分歧保持可见

场景：人认为最大风险是误操作，AI 认为是并发重复写入；证据不足，两者都影响架构。

**B0 预期**：可能尝试综合或给折中，也可能保持两假设。

**B1 预期**：已有“建设性反对”和“高风险方向决定要明确共识”。后者如果执行得机械，可能被解释成必须统一一个 explanatory model，虽然规范本意更接近对行动/授权达成足够共识。

**B2 真正增量**：明确 grounding 的目标是足够协调与显露承重分歧，不是强迫内部模型收敛；可以对共同目标、决策边界、授权达成一致，同时保留待证据区分的 competing hypotheses。

**结论**：有真实澄清价值，建议写入 Skill。需要边界：若行动必须在不确定性下继续，最终仍需对**采取哪个行动/接受什么残余风险**达成授权，不能用“保留分歧”逃避决策。

---

## 4. 第一轮判别结果

### 4.1 应保留并进入 pilot Skill 的强增量

1. **战略性直接证据切片**：当 AI 压缩会隔离人对其承重责任所需的关键因果/证据面时，给一个最高价值 direct slice，不要求重做机械劳动。
2. **AI 实质模型修正可观察**：新证据改变承重判断时结算取代关系，而不是静默换答案。
3. **共同 grounding 不要求 explanatory-model 收敛**：显露重要分歧、区分证据、保持必要独立性，同时对执行/风险接受取得必要授权。
4. **责任—能力 viability 的非教学响应组合**：旧 Skill 已有部分入口，但应把“学习只是可选响应之一”表达得更稳定。

### 4.2 不应重复添加为新机制

- “低风险机械事项不制造认知摩擦”：current Skill 已很明确；只作为 anti-overtrigger 回归。
- “异常证据不能被绿色总结果掩盖”：current Skill / spec 已有较强证据边界；候选 cognitive model 可以解释它，但不应通过重复规则制造复杂度。
- “当前有承重判断时需要给足上下文”：current Skill 已有；vNext 只补责任—能力解释和响应选择，不应重新发明。

### 4.3 对原 vNext 诊断的修正

原先把 live Skill 描述为“主要依赖 explicit learning authorization / tutor subsystem”过强。更准确的说法是：

> live Skill 已能通过承重判断、理解断点、风险和熟悉度进入支援路径，也已有主动导师候选回路；真正缺的是跨普通协作的一些更深机制没有被清晰表达和可靠载入，导致知识丰富的人仍常要手动要求 substrate contact、显式模型修正、非收敛式 grounding，以及把 capability mismatch 从‘要不要教学’提升到更广的责任分配/证据选择问题。

这是本轮 cloud replay 对我们自身候选模型的一个**recovered judgment**。

---

## 5. 对 pilot Skill 的最小修订建议

只修改会产生实际 runtime 差异的地方：

1. 在主 Skill 的自适应/推进规则中加入：人的承重责任所需有效判断基础不足/未知时，learning_mode 不得屏蔽问题；先从上下文、直接证据、验证、缩窄责任、专业参与、debt、学习中选最低成本响应。
2. 在“保护人的判断”加入战略性 direct slice：只在 AI summary/compression 会隐藏承重证据时触发。
3. 加入 AI 实质 judgment revision 的最小结算句法。
4. 澄清 shared understanding：不等于双方解释模型完全一致；承重分歧需要可见、可判别，执行与风险接受仍需必要共识/授权。
5. 不新增通用 cognitive checklist，不要求用户看到 activation/discrimination/reconstruction 方法论。

## 6. 下一证据层

本轮是**语义回放**，不是随机模型执行。完成最小 Skill 修订后：

- 本地日常使用：观察是否减少人手动提出上述四类元认知修复；
- runner：只在需要区分 native / old Skill / new Skill 的具体争议上运行少量 case；
- cloud：审查真实 field issue 是否能由候选机制解释，主动寻找 overtrigger / false positive；
- 如果 field evidence 反复出现新的结构，再回到 model/norm 层，而不是默认继续加 Skill 条款。
