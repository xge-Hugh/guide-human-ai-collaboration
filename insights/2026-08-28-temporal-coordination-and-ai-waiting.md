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
- 开 side chat 继续问同一主题；
- 在当前任务内继续思考；
- 离开屏幕、喝水、走动或短暂休息。

表面看，AI 接管执行后似乎“释放了人的时间”。但实际体验可能相反：

- 切到其他任务后需要在两个未完成目标之间来回恢复；
- 手机/新任务占据注意力后，AI 输出返回时很难立即进入阅读与判断；
- 人会反复检查“AI 是否已经完成”，形成额外监控负担；
- side chat 虽然主题相关，却可能引入新的子目标、解释模型或未闭合问题；
- 最终出现疲劳、无法跟上 AI 输出、协作质量下降，以及对等待是否结束的持续焦虑。

这说明：

> `AI 正在工作` ≠ `人的认知资源已经安全释放`

也不能反过来假设：

> `等待时间没有产出` = `协作效率低`

如果为了消灭“闲置”而持续塞入第二任务，可能把模型优化成**人类利用率最大化**，而不是**总协作认知成本最小化**。

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

## 6. 一个更具体的候选失效：human-as-polling-loop

如果系统无法可靠说明 AI 是否仍在工作、何时需要人回来，人的行为可能退化为：

```text
提交请求
→ 尝试做别的事
→ 想起 AI 可能完成
→ 检查
→ 没完成
→ 回到另一任务
→ 又想起
→ 再检查
→ ...
```

这时，人实际承担了一个系统本可承担的 completion-detection loop。

候选失效名：

> **Human-as-polling-loop：系统把“检测 AI 是否已完成”的持续责任隐式转嫁给人，使一个本可外置的未来意图持续占用注意与元认知监控。**

这与普通“等待太久”不同：即使总 latency 不变，只要有可靠 completion cue、任务安全悬置与低成本恢复，人的体验和认知负担可能已经显著不同。

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

## 8. side chat 不是天然正确答案

side chat 的吸引力在于它似乎“仍留在同一 working-memory context”。但至少存在三个 competing explanations：

1. **context-preserving hypothesis**：同主题继续思考帮助维持任务激活并产生新线索；
2. **goal-interference hypothesis**：第二对话生成新的解释、子问题和未闭合目标，反而增加恢复干扰；
3. **conditional hypothesis**：只有独立价值高、边界清晰、不会改变主线程输入假设的 side task 才有净收益。

因此不宜把“等待时开 side chat”写成默认 norm。

更好的问题是：

> **这个等待活动会降低还是增加主任务稍后恢复时的 reconstruction / interference cost？**

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

### H5 — side-chat conditionality

side chat 的价值取决于它是否产生独立可保留价值及是否引入竞争目标；“主题相同”本身不足以预测它是否有益。

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
- 若有 completion notification / 外置 return cue，行为是否改变。

不要求人工填写固定等待日志；只在自然出现高价值 observation 时保留。

### 暂不做

- 不给出“超过 X 秒就应该切任务”的统一阈值；
- 不把 side chat 写成标准动作；
- 不把 phone scrolling 单独上升为规范对象；
- 不因相邻认知科学证据就宣称 Human–LLM 等待机制已被证明；
- 不直接修改 live Skill；
- 不立即建立新的大规模实验。

---

## 12. 与当前 cognitive coordination 模型的候选关系

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
