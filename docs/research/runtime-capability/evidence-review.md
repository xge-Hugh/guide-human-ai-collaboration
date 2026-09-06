# Runtime capability evidence review

- **日期**：2026-09-06
- **状态**：`current research synthesis / mixed evidence`
- **目的**：把当前项目观察、assurance 结果与外部研究放在同一证据边界下，判断哪些主张已有支持、哪些仍只是候选机制。

> 本文件不是文献综述全集。它只保存会改变本 program 研究模型或 study 设计的外部证据。跨 program 的通用科学表述边界仍见 [`../external-evidence.md`](../external-evidence.md) 与 [`../../governance/evidence-policy.md`](../../governance/evidence-policy.md)。

---

## 1. 项目内部证据

### 1.1 Phase B：B1 有有限稳定化，B2 没有稳定增量

[`assurance-v2-phase-b-interpretation.md`](../assurance/studies/v2/assurance-v2-phase-b-interpretation.md) 的当前解释区分：

- B0：native/control；
- B1：B0 + 短、稳定 collaboration semantic boundaries；
- B2：B1 + 八部分 internal semantic reasoning scaffold。

当前结果支持一个**有限主张**：B1 对若干已有 base-model capability 产生了可观察但有限的稳定化；B2 没有在这些 cases 上显示稳定、可复现、成本相称的额外行为收益，有时增加 latency/reasoning cost，也可能出现更差行为。

不能据此推出：

- 复杂理论无用；
- B2 framework 在其他模型/任务上一定无效；
- resident prompt 永远优于 Skill；
- 更短 prompt 普遍更好。

对本 program 的主要增量是：

> **理论的概念价值与其作为 runtime context injection 的行为价值必须分开验证。**

这也是 guidance-experience 假设的早期项目证据：同一 project concern 的不同 representation 对运行行为有不同 marginal effect。

### 1.2 当前 local carrier 与 cloud workflow 的 field impression

当前 Cursor carrier 使用 resident kernel + conditional Skills；cloud 对话中则出现过另一种工作方式：先经 GitHub connector 主动阅读相关 project knowledge，再进入具体工作。

当前主观观察是：后者在若干长讨论中更容易产生接近项目理论的整体协调行为，而 current local Skill carrier 经常表现为局部、条件触发、需要人主动补充 metacognitive labor。

该观察只能作为 **field signal**：

- 模型、host、任务、context length、interaction history 等变量并未控制；
- cloud case 本身包含更长的共同推理与用户主动 exposure；
- “读项目后表现更好”可能来自信息量、顺序、model family、tool access 或更高推理预算等多个因素。

因此它支持 study question，不支持结论。

### 1.3 现有 Skill-learning diagnosis

[`../cognitive-coordination/design-diagnoses/skill-learning-capability-gap.md`](../cognitive-coordination/design-diagnoses/skill-learning-capability-gap.md) 已观察到：很多有效认知/学习机制虽然存在于 Skill 中，但仍依赖人主动指出学习机会、要求深挖模型或要求暴露证据，导致“内容存在”与“机制稳定发生”之间出现 gap。

本 program 将这个症状推广到 AI runtime capability，但不把原 diagnosis 的 human-learning claim 自动升级成一般 carrier 结论。

---

## 2. 外部证据：context 与 in-context capability

### 2.1 In-context learning 不等于权重学习

当前 LLM literature 普遍区分 inference-time context adaptation 与 parameter update。对本 program 最重要的不是某个单一 ICL mechanism，而是一个保守事实：**相同底层模型可以因 context 中的 instruction、demonstration 与 task evidence 呈现显著不同能力。**

相关入口：

- Brown et al., 2020, *Language Models are Few-Shot Learners*：https://arxiv.org/abs/2005.14165
- Dong et al., 2024/2025 survey, *A Survey on In-Context Learning*：https://arxiv.org/abs/2301.00234
- NAACL Findings 2025 关于 skill recognition / skill learning 的讨论：https://aclanthology.org/2025.findings-naacl.408/

对本项目的支持范围：context-conditioned capability 是合理研究对象；不能据此假设 prompt 能稳定“教会”任意新程序。

### 2.2 Context order 与 position 会改变表现

外部研究表明 few-shot example ordering 与 long-context position 可显著影响结果：

- Lu et al., ACL 2022, *Fantastically Ordered Prompts and Where to Find Them*：https://aclanthology.org/2022.acl-long.556/
- Liu et al., TACL 2024, *Lost in the Middle*：https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00638/119630/Lost-in-the-Middle-How-Language-Models-Use-Long

支持：context order/position 应成为实验变量，不能把“所有信息都在窗口里”当作等价可用。

不支持：固定把 collaboration theory 放在最前一定最好。

### 2.3 Model-generated contextual material 可能改善后续任务

相关工作表明模型可以自行生成 demonstrations / intermediate interpretation，再用其作为后续 context：

- Self-ICL, EMNLP 2023：https://aclanthology.org/2023.emnlp-main.968/
- Instruction induction, ACL 2023：https://aclanthology.org/2023.acl-long.108/

这些结果支持 **model-active context construction** 作为可检验方向，但任务形态与本项目不同，不能直接推广到 collaboration theory orientation。

---

## 3. 外部证据：非参数经验与程序积累

### 3.1 Reflection / episodic experience without weight update

- Reflexion, NeurIPS 2023：https://arxiv.org/abs/2303.11366
- ExpeL, AAAI 2024：https://arxiv.org/abs/2308.10144

它们显示 agent 可以把运行轨迹、反馈或语言化 insight 放入外部 memory，并在后续任务中改善行为，而不修改基础模型权重。

支持：system-level learning 不要求 parameter update。

限制：self-generated reflection 可能错误；其 task-success objective 也不同于本项目的 multi-objective collaboration quality。

### 3.2 从 episodes 提炼 reusable workflow / procedural memory

- Agent Workflow Memory (AWM), ICML 2025：https://arxiv.org/abs/2409.07429
- Voyager, 2023：https://arxiv.org/abs/2305.16291

这些工作支持一个结构性可能：

```text
raw trajectory
→ reusable procedure / skill-like artifact
→ future retrieval and composition
```

它们不证明本项目应该自动 distill 每个 interaction；反而强化“procedural artifact 可以是经验后的编译结果，而不是理论初始载体”的研究价值。

### 3.3 Dynamic / evolving skill systems

近期 agent-skill literature 越来越把 Skill 看成具有 creation、admission、retrieval、evaluation、refinement、maintenance 的 lifecycle，而不是孤立静态 prompt package。

相关线索包括：

- *Dynamic Agent Skills* survey/preprint, 2026：https://arxiv.org/abs/2607.10113
- *ProcMEM*, 2026：https://arxiv.org/abs/2602.01869
- *SkillEvolBench*, 2026：https://arxiv.org/abs/2605.24117
- *SkillCommit*, 2026：https://arxiv.org/abs/2608.15165

对本项目最重要的增量不是采用某一个 framework，而是三点：

1. applicability/activation 需要单独处理；
2. semantic similarity 不足以证明 procedures 可以安全 merge/generalize；
3. distilled skill 可能丢失 trajectory 中的关键 contextual cue。

因此本项目的 consolidation 需要 validation / rollback / provenance，而不是“AI 反思后自动写回”。

---

## 4. 外部证据：prompt / guidance 本身可作为优化对象

### 4.1 DSPy

DSPy 把 LM pipeline 的 instruction / demonstration 视为可根据 examples 与 metrics 编译/优化的程序参数，而不是必须由人一次性手写完成。

- ICLR 2024：https://proceedings.iclr.cc/paper_files/paper/2024/hash/f1cf02ce09757f57c3b93c0db83181e0-Abstract-Conference.html

支持：项目理论与其 runtime representation 不需要同构；runtime guidance 可以通过行为 evidence 被“编译”。

### 4.2 OPRO / Promptbreeder

- OPRO：https://arxiv.org/abs/2309.03409
- Promptbreeder, ICML 2024：https://proceedings.mlr.press/v235/fernando24a.html

这些工作把 prompt 本身当作可搜索/进化对象。

支持：resident/Skill text 不必被视为永久手工配置。

限制：本项目的 invariant / authority / human capability 目标不能只用 task score 优化；任何自动演化都需要 governance boundary。

### 4.3 GEPA

GEPA（ICLR 2026）利用 execution trajectory 与语言化反思提出、测试和保留 prompt/program variants，展示了“运行经验 → 改善 textual control conditions”的直接路线。

- https://proceedings.iclr.cc/paper_files/paper/2026/hash/0e9e708b6f48e14fd0ac29e167413f76-Abstract-Conference.html

这是 **guidance experience** 最接近的外部 precedent 之一：经验可以用于改善如何 elicitation 一个 fixed/slowly-changing model，而不一定写入模型参数。

但 GEPA 主要优化 benchmark/task objective；本项目必须额外保持 human agency、responsibility-capability、epistemic quality 与 cost 等评价维度。

---

## 5. 外部证据：retrieval 与 context allocation

### 5.1 Retrieval 并非越多越好

- FLARE, EMNLP 2023：https://aclanthology.org/2023.emnlp-main.495/
- Self-RAG, ICLR 2024：https://proceedings.iclr.cc/paper_files/paper/2024/hash/25f7be9694d7b32d5cc670927b8091e1-Abstract-Conference.html
- Adaptive-RAG, NAACL 2024：https://aclanthology.org/2024.naacl-long.389/

这些工作共同支持：retrieval 可以根据当前 need 自适应触发，indiscriminate retrieval 可能无益甚至有害。

这与本 program 的 recognition/context orchestration 假设一致，但不能自动证明让 model 自己选择 theory retrieval 一定优于外部 selector。

### 5.2 长期 memory 仍需要 indexing / retrieval / reading engineering

LongMemEval（ICLR 2025）把长期 memory 问题分解为 indexing、retrieval 与 reading，并观察到长历史下显著性能下降。

- https://proceedings.iclr.cc/paper_files/paper/2025/hash/d813d324dbf0598bbdc9c8e79740ed01-Abstract-Conference.html

支持：外部 state 存在不等于可用；recognition cue 与 retrieval representation 本身也是 runtime capability 的组成部分。

---

## 6. 人类学习类比：只作为 heuristic，不作为机制证明

本轮讨论用“专家 vs 每次拿 manual 的学生”“active learning vs passive exposure”帮助发现结构，但项目必须保持 species/mechanism boundary。

人类证据：

- Freeman et al., PNAS 2014 active-learning meta-analysis：https://www.pnas.org/doi/10.1073/pnas.1319030111
- generation effect 等学习研究表明自生成通常可增强人类记忆/理解。

这些证据可以启发：主动生成、检索、解释、比较可能比纯暴露更有价值。

但不能直接推出 LLM 会以相同机制形成长期 memory。对 AI 更安全的表述是：**model-active context construction 可能改变当前 inference state 和后续 capability expression，需要单独实验。**

---

## 7. 当前证据矩阵

| Candidate claim | 当前证据 | 当前地位 |
| --- | --- | --- |
| 完整理论注入不等于可靠 runtime mastery | Phase B + Skill field friction + external ICL/skill evidence | `supported as diagnosis, mechanism open` |
| base model capability 是 carrier 效果的重要变量 | B1 interpretation + broad ICL evidence | `supported / needs model-specific mapping` |
| context order/position 会影响行为 | strong external evidence | `supported generally; project-specific effect unknown` |
| model-active reading/orientation 可能优于被动注入 | project field signal + adjacent external evidence | `candidate` |
| recognition/applicability 应单独评估 | static Skill bottleneck + dynamic/procedural memory literature | `strong candidate` |
| external experience 可在不改权重下改善 system behavior | Reflexion/ExpeL/AWM/GEPA 等 | `supported generally` |
| guidance experience 是本项目高价值 memory object | external analogues + Phase B reinterpretation | `candidate / project-specific` |
| runtime experience 不应直接改 canonical theory | epistemic/governance reasoning + skill evolution warnings | `strong design boundary` |
| 最终 carrier 应是 thin coordination architecture | current synthesis | `candidate` |

---

## 8. 对下一轮 study 的证据要求

优先区分以下 competing explanations：

1. **content quantity**：cloud reading 更好只是因为读到更多信息；
2. **ordering**：理论先进入 context 改变 task framing；
3. **model-active construction**：主动读/总结本身产生独立增量；
4. **reactivation**：Skill 主要价值来自长任务中的 attention refresh；
5. **model family**：差异主要来自 base model，而不是 carrier；
6. **guidance accumulation**：经验证的历史 cue/procedure 是否能在新案例迁移。

Study 不应只记录 task success，还应测：

- missed intervention / over-intervention；
- authorization / responsibility / evidence failures；
- task quality；
- human reconstruction / judgment basis；
- token、latency、tool-call 与 reasoning cost；
- cross-model robustness；
- no-op quality。
