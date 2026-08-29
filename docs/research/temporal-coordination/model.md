# AI 等待期与时间协调：从“响应延迟”到悬置认知承诺

- **日期**：2026-08-28
- **地位**：`candidate insight / field-derived clue`
- **语义类型**：认知协调 / HCI / 执行载体候选问题；不是当前规范、不是新工作流阶段、不是已验证设计
- **来源**：真实日常人机协作中的等待、分心、轮询与恢复摩擦；对照当前 cognitive coordination 模型、working-memory / interruption / prospective-memory 研究，以及 2026 CHI 的 Human–LLM latency 实验
- **当前证据强度**：真实 field observation + 多个相邻认知机制的外部支持 + 一项直接 Human–LLM latency 研究；尚不足以推出统一等待策略或固定时间阈值

## 1. 一句话主张

人机协作中的 AI 响应延迟不只是“时间成本”。当 AI 暂时占有协作话轮、但尚未返回可用信息时，人可能进入一种**悬置认知承诺（suspended cognitive commitment）**状态：当前任务尚未闭合，注意力又缺乏可继续作用的对象，同时人还可能需要维持“AI 完成后回来检查”的未来意图。

因此，一个候选的更深问题是：

> **高质量协作不仅要保护人在交互内容上的工作记忆，也要协调双方在时间上的可用性，使任务能够被低成本地悬置、释放和恢复，而不是让人长期处于半等待、半监控、半切换的状态。**

本文件暂把这一候选问题称为**时间协调（temporal coordination）**。

---

## 2. 原始 field clue：等待时“空出来的手”不等于空出来的认知资源

真实使用中，AI 响应时间会从很短变成明显可感知的等待。在等待较长时，人可能：

- 什么都不做，但持续盯着是否完成；
- 打开手机、社交媒体或其他高新奇输入；
- 切到另一项实质任务；
- 使用附着于主线程的 side chat 做局部解释/追问，或较少情况下另开一个独立聊天；
- 在当前任务内继续思考；
- 离开屏幕、喝水、走动或短暂休息。

表面看，AI 接管执行后似乎“释放了人的时间”。但实际体验可能相反：

- 切到其他任务后需要在两个未完成目标之间来回恢复；
- 手机/新任务占据注意力后，AI 输出返回时很难立即进入阅读与判断；
- 人会反复检查“AI 是否已经完成”，形成额外监控负担；
- side chat 虽然仍附着于主线程，却可能在主线程恢复前形成尚未闭合的辅助认知义务；另开独立聊天则具有更明显的注意分裂风险；
- 最终出现疲劳、无法跟上 AI 输出、协作质量下降，以及对等待是否结束的持续焦虑。

这说明：

> `AI 正在工作` ≠ `人的认知资源已经安全释放`

也不能反过来假设：

> `等待时间没有产出` = `协作效率低`

如果为了消灭“闲置”而持续塞入第二任务，可能把模型优化成**人类利用率最大化**，而不是**总协作认知成本最小化**。

### 2.1 新的 field observation：等待期间并非只有“做 / 不做”两种状态

进一步观察显示，等待期间实际存在更多可观察的人类行为：

- **手机低门槛切换**：手机通常就在手边；无输出和无明确动作对象时，人容易打开社交媒体或回复消息；
- **过程监看**：有可见 thinking / reasoning trace 时，人会观看 AI 的思考过程，并比较它是否符合自己的预期；
- **纸笔外化**：人有时会用纸笔记录未来线索或整理思路；书写较慢、字迹凌乱时会产生“数字时代却还在用纸”的不协调感，但当能够稳定、整洁书写时，主观上反而更平静；
- **side chat 辅助分支**：side chat 与另开独立聊天不同，它附着于当前主线程/材料；等待时可能被用来做局部解释、追问或整理疑问，但若主线程先返回，人会同时承担主线恢复与旁支收束；
- **流式阅读**：AI 一旦开始 streaming，人可能从“等待”切换为边生成边阅读、预测和判断，而不是等完整答案结束后再统一处理；
- **意图输入**：人在发送 prompt 前的打字、修改、删改、组织语言，本身也是协作中的认知活动，而不是中性的输入通道。

这使问题从“等待期如何利用”扩展为一个更一般的观察：

> **人机协作不是离散的 user turn → AI turn → user turn。每个语义话轮内部都可能包含输入构造、悬置、监看、流式阅读、预测、记录、分支探索、整合和恢复等不同认知状态。**

因此，AI waiting 可能只是暴露了一个更大的**turn-level abstraction gap**：项目过去主要建模“讨论了什么、谁判断什么、何时进入下一关注点”，却较少建模**人和 AI 在一个话轮内部实际怎样占用、释放和重新配置认知资源**。

---

## 3. 当前项目为什么能够容纳它，但尚未真正描述它

当前项目已经有多个相邻概念：

- `docs/spec/norms.md` 在“轻量”中提到减少无相称价值的认知、行动、**等待**与维护成本；
- cognitive coordination 候选模型把工作记忆、注意力、疲劳预算与时间视为稀缺资源，并提出 cognitive allocation；
- reconstruction 关注中断、上下文衰减或跨会话后如何重建可用任务模型；
- Skill 已尝试在恢复、切换、分叉和状态变化时提供重建线索。

但这些规则主要回答：

- 人应该把注意力投入哪里；
- 中断后怎样恢复；
- 哪些信息值得外置；
- 哪些任务/判断应该由谁承担。

它们还没有明确回答：

> **当 AI 暂时不可交互，而当前共同任务又未闭合时，人是否应该继续维持任务激活？何时可以真正释放注意力？谁负责检测 AI 工作已经完成？恢复时需要什么线索？**

因此，“等待”目前更像成本项中的一个词，而不是一个具有自身失效模式的协作现象。

---

## 4. 研究校准：当前已有的相邻证据

以下证据只能校准机制边界，不能直接证明本项目最终应采用某一等待策略。

### 4.1 unfinished task switching / attention residue

Leroy (2009) 的两项实验显示，从未完成任务切换到下一任务时，前一任务相关认知活动可能残留，并损害后续任务表现。

- Sophie Leroy, *Why is it so hard to do my work? The challenge of attention residue when switching between work tasks*
- DOI: https://doi.org/10.1016/j.obhdp.2009.04.002

对本项目的邻近含义：AI 等待期内开启第二项实质任务不能被默认视为“免费并行”。

### 4.2 interruption resumption 与 working memory

Foroughi et al. (2016) 发现，中断持续时间越长，恢复原任务的 resumption lag 越大；较高 working-memory capacity 可减弱这一关系。

- DOI: https://doi.org/10.1037/xlm0000251

Labonté & Vachon (2021) 在动态任务中进一步指出，长中断后的恢复不仅依赖工作记忆，也涉及对任务环境的 reconstruction。

- DOI: https://doi.org/10.3389/fpsyg.2021.659451

对本项目的邻近含义：恢复成本不是“人专注一点就能消失”的摩擦；随着中断和环境变化，重建本身可能成为必要认知操作。

### 4.3 suspension 前的 preparation 可以帮助恢复

Trafton et al. (2003) 研究表明，在中断真正发生前有短暂 interruption lag、允许参与者准备恢复目标时，后续任务恢复可以改善。

- DOI: https://doi.org/10.1016/S1071-5819(03)00023-5

对本项目的邻近含义：若准备切去其他任务，一个极小的“返回点/等待对象/回来后要判断什么”外置，可能比事后重新读完整上下文更有价值。

### 4.4 prospective memory 与 intention offloading

Peper, Alakbarova & Ball (2023) 发现，在更高 prospective-memory load 下，提醒带来的收益更大；包含 target + action 的提醒改善未来意图执行，而没有观察到对 ongoing task performance 的代价。

- DOI: https://doi.org/10.1037/xlm0001191

Gilbert (2015) 等 intention-offloading 研究也表明，人会根据记忆负荷和分心可能性策略性地建立外部提醒。

- PMID: https://pubmed.ncbi.nlm.nih.gov/25404057/

对本项目的邻近含义：如果 AI 完成事件能够由系统可靠外置，人不必持续把“稍后回来检查”保留为内部监控责任。

### 4.5 直接 Human–LLM latency 证据

Tan, Messerschmidt, Yin & Nov (CHI 2026) 控制 Human–LLM 交互中的 time-to-first-token（2 / 9 / 20 秒）。行为指标总体对 latency 较稳健，但 latency 显著影响用户对输出质量的感知。中等等待有时被用户用于重新阅读指令或规划下一步；较长等待有时转化为 frustration 或 reliability concern。

- Felicia Fang-Yi Tan et al., *The Impact of Response Latency and Task Type on Human-LLM Interaction and Perception*
- DOI: https://doi.org/10.1145/3772318.3790716
- arXiv: https://arxiv.org/abs/2604.06183

这项研究的重要性不是证明“9 秒最好”，而是直接支持：

> **Human–LLM latency 可以改变交互意义与用户行为，因此不应只被建模为越短越好的系统性能指标。**


### 4.6 主动理解支援的相反边界：timing 有价值，但 explanation 也会增加复杂度

Liu et al. (CHI 2026) 在知识密集型数字任务中发现，与错位或随机触发相比，时机与用户困难更对齐的 adaptive LLM clarification / explanation 可以改善准确率并减少 missed-help。

- DOI: https://doi.org/10.1145/3772318.3791191

但 Westphal et al. (2023) 的 human–AI decision experiments 发现，额外 explanation 也可能提高 perceived task complexity，并使部分用户结果变差。

- DOI: https://doi.org/10.1016/j.chb.2023.107714

对本项目的含义不是“AI 应主动讲更多”，而是：

> **理解支援的价值取决于时机、强度、表示和交互成本；如果支援要求人维护第二条对话义务，或者 explanation 本身继续增加信息密度，它可能抵消原本想减少的认知负担。**

---

## 5. 候选机制：时间协调不是新的 workflow phase

不建议增加一个“等待阶段”。等待可以出现在 framing、deliberation、act、assure、reflect 的任何位置，而且不同工具/API/agent 的等待形态不同。

更合理的候选对象是一个横跨工作流的 temporal coordination control，关注**认知耦合（coupling）**而不是固定秒数。

初步可区分三种状态：

### 5.1 紧耦合短等待 / synchronous micro-wait

特点：

- 当前认知单元仍高度激活；
- AI 很可能很快返回；
- 开启新目标的切换成本可能高于等待成本。

候选默认：允许什么都不做、继续保持上下文、低负荷思考或短暂休息，不要求人为制造“生产性等待”。

### 5.2 有感知但仍属于同一认知回合的 bounded pause

特点：

- 等待已经足以产生无聊、漂移或检查冲动；
- 当前问题仍强耦合；
- 人可能有少量高价值同任务活动。

候选活动可以包括：

- 重读当前问题；
- 记一条自己目前的预测/疑问；
- 标记“什么证据会改变我的判断”；
- 低负荷身体活动或短休息。

这里不应默认要求 side chat；只有当 side chat 的结果即使主回复稍后返回仍具有独立价值时，它才可能是合理分支。

### 5.3 松耦合长等待 / asynchronous delegation

特点：

- 继续维持任务激活本身已经成为负担；
- 人有理由投入另一项实质任务；
- 回来时需要重建，而不是假装上下文仍完整在线。

候选操作：

1. **suspend**：外置最小 return state；
2. **release**：由系统承担完成检测，而不是让人轮询；
3. **resume**：完成后通过最低成本 reconstruction cue 重新激活目的、等待对象和下一判断。

这里真正的设计目标不是“教人多任务处理”，而是允许**安全脱耦**。

---

## 6. 修正后的候选失效：blocked-progression polling

新的 field observation 修正了一个先前过强的解释：现代 agent 工具往往**已经有 completion notification**（弹窗、声音或系统通知），但人仍可能主动检查 AI 是否完成。因此 polling 不能主要归因于“系统没有通知”。

更符合观察的候选序列是：

```text
当前推进依赖 AI 返回
→ 人暂时没有可继续的主任务动作
→ 又不确定这段空档是否值得投入另一件事
→ 尝试低门槛替代活动 / 保持部分任务激活
→ 想尽快恢复主线
→ 主动检查 AI 是否已经足够接近完成
→ 未完成则重新进入等待/替代活动
```

候选失效暂改称：

> **blocked-progression polling：当下一步依赖对方返回，而等待时长和可安全投入的替代活动不明确时，人因为“继续等待还是切走”的协调冲突而反复检查进展，即使完成通知本身已经存在。**

这更接近现实世界等待一个会决定自己下一步的人：最终消息可能会通知，但等待者仍会反复看邮件、消息或状态，因为真正未解决的是**行动依赖 + 时间不确定性 + 注意分配冲突**。

等待不确定消息的心理研究提供相邻证据：等待本身可产生焦虑、分心和 expectation volatility；但这些研究多针对重要现实结果，不能直接外推为 Human–LLM polling 机制。它们至少提醒项目：

> `知道最终会收到通知` ≠ `等待期间可以完全释放认知承诺`

因此 completion cue 仍可能有价值，但它不再被视为这一问题的充分解法。

---

## 7. 这可能暴露 assurance carrier 的新边界

该问题很可能不能只靠 Skill / prompt 解决。

尤其在：

- first token 之前；
- 模型推理期间；
- 长工具调用期间；
- agent / background-style delegation 期间；

模型本身往往无法持续与人交互。

因此某些协作保障需求可能属于**interaction substrate / UI / event layer**，例如：

- 可靠 completion notification；
- 能区分“仍应保持同步”与“可以安全离开”的状态信号；
- 不要求人不断轮询的等待机制；
- 回来时提供最小 reconstruction cue；
- 必要时提供进度/当前 activity 的可观察性，但不制造虚假精确 ETA。

这提供一个值得后续验证的架构后果：

> 并非所有 collaboration norm 的最佳 carrier 都是 resident prompt / Skill / injected framework；有些规范对象可能只能由 UI/event-level mechanism 可靠保障。

当前只把它记为 candidate architectural implication。

---

## 8. side chat 必须与 second separate chat 分开建模

新的 field clarification 修正了先前一个重要混淆。

### 8.1 second separate chat：真正的并行会话

second separate chat 指另开一个完整、独立的聊天窗口/会话。它有自己的未闭合目标、上下文和返回点，因此更接近传统 task switching / attention splitting。

真实使用中，这种行为相对少见，尤其在需要集中注意的高认知项目里会被主动避免，因为人已经预期到同时维护两个完整聊天会让两边质量下降。

### 8.2 side chat：附着于主线程的辅助交互

side chat 不等于第二个独立聊天。它更像附着于当前主线程或当前材料的 auxiliary surface，目的通常不是开启另一项业务任务，而是：

- 解释当前段落/术语；
- 追问一个局部关系；
- 暂存一个疑问；
- 生成一个例子或预测；
- 在不污染主线的情况下检查一个局部理解。

因此不能把 side chat 的成本简单写成“切到另一个任务”。

但它仍会产生自己的 interaction obligation：人需要组织问题、等待、阅读、决定是否继续，并把结果重新接回主线。

### 8.3 候选失效：rejoin collision

等待期间使用 side chat 时可能出现：

~~~text
主线程仍在等待
→ 人开始组织 side-chat 问题
→ side prompt 尚未发送 / side response 尚未闭合
→ 主线程先返回并开始 streaming
→ 人突然同时拥有两个待处理认知对象
~~~

这里真正的负担不是主题切换，而是 interaction-state concurrency。

候选失效名：

> **rejoin collision：辅助分支尚未闭合时，主线程重新变得可行动，使人同时承担主线恢复、旁支收束和跨线程整合。**

这可以解释一个看似矛盾的现象：side chat 与主线程高度相关，本来是为了降低理解负担，却可能因为返回时机冲突而增加 working-memory maintenance。

因此当前最有区分力的问题是：

> **side chat 提供的理解/预测价值，是否足以抵消 branch management、rejoin collision 和 reconciliation 的成本？**

这与 second separate chat 是两个不同研究问题。

---

## 9. 候选设计原则：不要最大化人的等待期利用率

目前最值得保留的一条设计倾向是：

> **协作系统不应把 AI latency 中人的每一秒都视为待利用的空闲容量。**

休息、看窗外、走动、暂时不输入信息，可能是正确的认知分配。

“productive waiting” 如果变成新规范仪式，可能产生新的失败：

- 强迫人生成额外问题；
- 为了显得高效而开启低价值 side task；
- 增加元认知监控；
- 将系统 latency 的责任转化成人的自我管理责任；
- 让人误以为“什么都不做”是低质量协作。

因此目标应更接近：

> **minimize suspension + monitoring + resumption cost**

而不是：

> **maximize human utilization during AI latency**

---

## 10. 可被检验的 competing hypotheses

若后续要进入 field observation / runner / HCI experiment，不应先假定“某种等待方式最好”。

至少可以比较：

### H1 — context preservation

短等待中保持当前问题激活，比切换到无关任务更有利于理解 AI 随后输出和继续决策。

### H2 — low-demand incubation

在某些开放/创造任务中，低负荷离屏活动可能比持续监视或高新奇输入更有利于后续思考；但这不应外推到所有分析任务。

### H3 — safe release

长等待中，如果系统提供可靠 completion cue + return state，完全释放注意力可能优于持续轻度监控。

### H4 — polling tax

即使 latency 总时长相同，需要人主动检查完成状态的条件会增加主观负担、检查次数、恢复成本或对后续输出的跟随困难。

### H5 — side-chat rejoin cost

side chat 即使与主线程共享主题，也可能因为辅助分支尚未闭合而与主线程返回发生 rejoin collision；其净价值取决于理解/预测收益是否超过 branch management 与 reconciliation 成本。

### H6 — carrier boundary

部分 temporal-coordination 失效无法由模型内部 normative kernel 稳定修复，而需要 UI/event-level assurance。

---

## 11. 后续应观察什么，而不是立刻改什么

### 优先 field signals

在真实日常协作中自然观察：

- AI 长等待时人实际做了什么；
- 是否出现手机/窗口切换；
- 是否反复检查完成状态；
- 返回后需要多久重新进入原问题；
- AI 输出已经开始/完成时，人是否错过阅读起点；
- 是否需要重新问“我们刚才在做什么”；
- side chat 是否产生帮助、冲突还是新未闭合分支；
- 等待结束后主观疲劳、烦躁或上下文丢失；
- 即使已有 completion notification，人是否仍主动轮询，以及轮询发生在什么心理/任务条件下；
- 有可见 thinking trace 时，人是否用它做预测/校准，还是被它持续占据注意；
- 人是等完整答案后阅读，还是在 streaming 中边读边形成判断；
- 手写/键入/仅在脑中思考分别怎样影响主观平静、线索保留和恢复；
- side chat 与 second separate chat 分开记录；side chat 重点观察是否出现主线程先返回造成的 rejoin collision，以及辅助支援是否真的改善理解/预测；
- 若有外置 return cue、进度状态或更明确的 safe-to-leave signal，行为是否改变。

不要求人工填写固定等待日志；只在自然出现高价值 observation 时保留。

### 暂不做

- 不给出“超过 X 秒就应该切任务”的统一阈值；
- 不把 side chat 写成标准动作；
- 不把 phone scrolling 单独上升为规范对象；
- 不因相邻认知科学证据就宣称 Human–LLM 等待机制已被证明；
- 不直接修改 live Skill；
- 不立即建立新的大规模实验。

---

## 12. 更大的候选：从 turn-taking 模型到 interaction-state 模型

AI waiting 的价值可能在于暴露了一个比 temporal coordination 更大的建模缺口。

传统对话表示容易把一次协作压缩为：

```text
human message
→ AI response
→ human message
→ AI response
```

但真实协作更可能是：

```text
形成意图
→ 输入/修改表达
→ 提交
→ 等待
→ 监看/漂移/记录/切换
→ AI 开始 streaming
→ 边读边预测/判断
→ 暂停理解
→ 可能 side branch
→ 回主线程整合
→ 形成下一行动
```

这些不是必须变成新 workflow phases。它们更像**interaction microstates / cognitive states**：可跨任何业务关注点出现，而且只有在它们会改变认知负担、判断质量、可恢复性或系统设计时才值得显式建模。

因此目前有两个层级不同的候选：

- **temporal coordination**：处理双方不同步、等待、悬置与恢复；
- **interaction-state model**：更广泛描述一个协作话轮内部，人如何输入、等待、观察、阅读、外化、分支、整合与恢复。

当前不应急于把第二个候选扩展成完整 taxonomy。AI waiting 只是第一个明确暴露该 gap 的 field clue；未来只有其他真实观察（例如 streaming 阅读、prompt 构造、thinking-trace 监看、side-chat comprehension）反复显示它们能解释现有模型解释不了的失效，才值得进一步抽象。


### 12.1 候选设计方向：support without branch ownership

新的 side-chat 观察提出一个比“是否保留 side chat”更有价值的设计问题：

> **能否提供理解修复、memory chunking、上下文压缩和局部解释，同时不要求人创建并管理一个新的对话义务？**

这里暂称为 cognitive sidecar。它不是固定 UI，也不是“再放一个 AI 在旁边”。它描述一种功能边界：

- 支援尽量原位、低交互、可忽略；
- 默认不要求人先诊断自己的理解断点并写高密度 prompt；
- 一个局部解释不自动变成必须继续的第二线程；
- 支援结束后应自然回到 parent locus；
- explanation 采用 progressive disclosure，而不是一次性增加更多复杂内容。

低风险候选载体可能包括：

- 选中一句后的“一键解释 / 举例 / 为什么重要 / 记忆块”；
- 长输出附近极少量 chunk anchor；
- 主线从长等待恢复时的一句 reconstruction cue；
- ephemeral scratchpad：辅助解释默认不进入永久会话；
- 不要求回复的被动式理解提示；
- 只有在证据较强时才出现的可关闭 proactive clarification。

这与项目已有的 shared conversational initiative 和 companion-learning 候选相邻：支援不应长期依赖人自己发现机会、再用高成本输入请求。但新的约束是**支援本身不能制造新的 branch-management 负担**。

当前不建立产品需求，也不认为 proactive support 天然更好；4.6 的研究边界提示，解释和主动介入本身也可能增加 task complexity。

---

## 13. 手写与手机：先保留现象，不做神经故事

“拿起手机”与“拿起纸笔”在等待期形成了有意义的行为对照，但当前应谨慎解释。

### 手机

研究支持 boredom、habitual checking、内部 mental cues 与 spontaneous smartphone checking 有关；数字内容快速切换还可能增加 attentional failure 和 boredom。这里更稳妥的语言是**低摩擦、习惯化、即时可获得的注意替代**，而不是简单归因于“dopamine”。多巴胺参与 reward learning，但“因为多巴胺所以刷手机”对本项目而言过于粗糙，无法产生可判别设计。

### 纸笔

handwriting 与 typing 在速度、sensorimotor involvement、编码方式和学习结果上确有研究差异，但现有证据主要来自教育/记忆任务。当前 field observation 更直接：纸笔虽然慢、字迹会造成摩擦，却有时让人主观更平静，并形成不受屏幕信息流干扰的外部思考表面。

因此目前不主张“等待时应该手写”，只保留两个待区分的解释：

- **externalization hypothesis**：把未闭合想法写到外部介质上，降低 working-memory maintenance；
- **pace / attentional-boundary hypothesis**：更慢且单一的物理交互减少信息切换，使人更容易稳定在一个认知对象上。

如果以后发现数字笔记也能产生同样效果，则“手写”本身可能不是机制；如果只有纸笔稳定出现，则再研究载体差异。

---

## 14. 新候选：punctuated oversight，而不是 continuous monitoring / complete disengagement 二选一

新的 field hypothesis 是一个看似反直觉但可被外部研究约束的方向：

> **在人机协作中，人未必应持续观看 AI 的每一步执行；低价值执行期间释放注意，可能比持续监督更能保护后续理解与判断所需的认知资源。**

但该命题不能直接写成“只看最终结果”。

### 14.1 continuous monitoring 的已知成本

human–automation 研究长期发现，持续监控本身会受到 vigilance decrement 影响，而且监督自动化并不是零负荷任务。监控者可能在持续努力的同时降低异常检测能力。

- Parasuraman (1987), *Human-Computer Monitoring*
- DOI: https://doi.org/10.1177/001872088702900609
- Gouraud et al. (2017), *Autopilot, Mind Wandering, and the Out of the Loop Performance Problem*
- DOI: https://doi.org/10.3389/fnins.2017.00541

这支持一个项目级边界：

> `human is watching` ≠ `human judgment is being protected`

持续 watching 可能消耗 attention，却没有增加有区分力的 evidence contact。

### 14.2 rest / low-interference window 的相邻支持

wakeful-rest 研究显示，学习后的安静清醒休息相对干扰任务可改善后续记忆保持；micro-break meta-analysis 也发现短休息对 vigor / fatigue 有小而稳定的改善。

- Weng et al. (2025), DOI: https://doi.org/10.3758/s13423-025-02665-x
- Albulescu et al. (2022), PMID: https://pubmed.ncbi.nlm.nih.gov/36044424/

这些证据不能直接证明“AI 等待会恢复 working memory”，也不能说明所有 mind wandering 有益。更谨慎的候选解释是：

- 低干扰窗口可能减少新的 retroactive interference；
- 短休息可以降低部分主观疲劳；
- 不持续监看可以避免把 attention 继续锁定在低价值执行上。

### 14.3 complete disengagement 的反向风险

automation literature 同时存在 out-of-the-loop performance problem：如果人长期只作为末端接管者，却没有足够 situation / system understanding，异常发生时可能更慢发现问题、更难诊断或接管。

因此：

> `continuous monitoring is costly` ≠ `end-only review is always sufficient`

### 14.4 候选中间机制：punctuated oversight

当前更合理的候选是**punctuated oversight / checkpointed engagement**：

```text
承重方向 / 输入契约
→ 人形成必要模型与判断
→ AI 承担低价值批量执行
→ 人可以释放持续监控
→ 在 evidence-bearing checkpoint 重新进入
→ 查看一个最高价值直接证据 / 状态变化 / 异常
→ 作出下一承重判断
→ 再次释放
→ 最终验收
```

它与现有 strategic exposure 很接近：人的价值不在于观察每一步，而在于**在会改变模型、风险或责任的地方接触足够直接证据**。

因此后续 field observation 应区分：

- continuous thinking-trace monitoring；
- complete leave-and-return；
- punctuated checkpoint review。

真正要比较的是后两种方式能否在降低 fatigue / monitoring burden 的同时，保持或改善 judgment readiness、异常检测与结果理解。

---

## 15. 新候选：graded disengagement / attentional downshift

新的 field observation 修正了 practice-first 方法中的另一个隐含假设：休息、外置、轻活动等行为不一定彼此独立，也不一定适合被当成互斥条件。

对一个已经持续高强度投入的任务，人可能很难从：

```text
高密度对话 / 预测 / 判断 / working-memory maintenance
→ 直接静止休息
```

瞬间完成脱离。

更符合真实习惯的候选序列可能是：

```text
高参与
→ 外置一个 return cue / label
→ 较低信息密度的桥接活动（如纸笔）
→ quiet rest / stretch / walk
→ checkpoint re-entry
```

这里暂称为 **graded disengagement / attentional downshift**。

### 15.1 外部研究能支持什么

现有证据支持该序列中的几个组成部分，但**还不能证明这个完整梯度本身是最佳方案**：

- task-switching 研究显示，切换存在稳定成本，提前准备可以降低但不能完全消除 switch cost；
- interruption/resumption 研究支持在离开前建立一个 return goal；
- psychological-detachment 研究显示，从高要求工作中真正 mentally disengage 并不总是容易；
- micro-break 研究支持短休息对 fatigue / vigor 的小幅平均收益；
- wakeful-rest 研究显示低干扰休息在部分记忆任务中有益，但效应异质，尤其不能直接外推为“恢复 working-memory 容量”。

因此，“高刺激 → 中刺激 → 无刺激”目前更适合作为人的**主观体验模型**。在项目中更可操作的机制语言是：

> **逐步降低 task-state maintenance、信息输入与 interaction obligation，而不是要求认知系统瞬间从高度耦合切到完全 disengaged。**

### 15.2 为什么纸笔可能成为 bridge，而不是单独的 note-taking 技术

纸笔在这里可能具有三种不同作用：

1. **externalization**：把 return cue 从 working memory 移到外部；
2. **task closure / transition cue**：用一个可见动作标记“当前不再需要继续内部维持”；
3. **lower-input bridge**：仍保留与任务的轻度接触，但不继续接收 streaming、通知或高密度数字信息。

关于 handwriting 与 typing 的学习研究结果并不一致：2024 meta-analysis 在大学课堂笔记情境中发现 longhand 在 achievement 上有小优势而 typing 记录量更高；另一项 meta-analysis 则认为总体学习结果差异接近零，数字设备的额外 distraction 可能解释部分差异。因此不能把纸笔本身神化。

当前更值得验证的是：

> **纸笔是否因为“外置 + 单一表面 + 较慢节奏”而成为从高耦合 AI 交互到休息之间的有效过渡介质。**

### 15.3 新的 field comparison

未来不必把 practice A/B/C 当成互斥实验条件。更自然的比较是：

- 直接继续监控；
- 直接休息；
- **先 park / paper，再休息**；
- 先 park / paper，再做低需求身体活动；
- 完全离开后只在 checkpoint 返回。

观察重点是：

- 哪种方式最容易真正停止内部 rehearsal；
- 哪种方式 re-entry 最轻；
- 哪种方式既减少 fatigue，又不造成 out-of-the-loop；
- 中间 bridge 是否只是额外仪式，还是确实帮助 disengagement。

如果 bridge 经常被跳过且没有损失，就应删除；如果它反复使 release 更容易，它才值得进一步抽象。

---

## 16. 与当前 cognitive coordination 模型的候选关系

如果后续证据支持，该 insight 可能不是独立大理论，而是对现有 cognitive allocation + reconstruction 的一个时间维扩展：

```text
cognitive allocation
    问：人的稀缺认知资源此刻值得投到哪里？
        ↓
temporal coordination
    问：当双方在时间上不可同时可用时，任务应保持激活、轻耦合还是安全悬置？
        ↓
suspension / release / resumption
    问：怎样外置未来意图、避免轮询，并低成本重建？
```

它还可能反向补强一个更一般的项目主张：

> **协作质量不仅取决于谁做什么，也取决于双方何时可用、任务如何跨不可用窗口保持可恢复性。**

当前保留为 field-derived candidate，不晋升为规范。
