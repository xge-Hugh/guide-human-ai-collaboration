# Human-AI Collaboration Carrier vNext Pilot

> 状态：**experimental implementation / validation carrier**  
> 对应：Issue #31  
> 分支：`pilot/collaboration-carrier-vnext`

本 pilot 不把“重写一个更大的 Skill”作为目标。它从当前项目语义重新派生一个**最小可组合运行载体**，用于观察：稳定常驻边界、按需 Skill、host capability 与研究候选机制如何组合，是否能在首次合适机会产生预期行为，同时减少不必要触发、等待与人的补偿性元认知劳动。

## 1. 当前决策

### 1.1 旧 Skill 暂时保留，不 patch，也不删除

`skills/guide-human-ai-collaboration/` 在本分支保持不变，作为 current-Skill comparison baseline。

保留它不是承诺长期兼容。若 vNext 经行为与 field pilot 后成为替代方案，且没有已识别 consumer，应按项目演进规则删除或归档旧载体，而不是永久维护两套无权威拓扑。

### 1.2 Runtime instruction 使用 English

新 resident kernel 与所有新 Skill 正文使用 English，以提高跨 host / model 的可移植性。

项目维护文档仍可使用中文。**不预设语言差异对触发与执行无显著影响**：本 pilot 在 routing eval 中保留 English / Chinese 成对案例，用实际行为检查 English metadata 是否仍能从中文请求正确触发。

### 1.3 不建立 umbrella/router Skill

Agent Skills 的 discovery metadata 本身已经提供按需路由面。为了避免“触发总 Skill → 加载全部语义”的历史耦合，本 pilot 让每个 Skill 直接声明自己的正触发、负触发与责任边界。

### 1.4 不实现通用 state/recovery Skill

AI / task-context continuity 交给 host/product 的 conversation history、project context、branching、memory/retrieval 或等价机制。

项目仍保留：
- claim / source / provenance conflict 的认识论语义；
- 会改变行动的 collaboration-state / authorization 边界；
- cognitive-coordination research 中关于 human reconstruction 的候选问题。

本 pilot 不建立通用 `state.json` 恢复协议。

## 2. Semantic source set

### Current requirements

- `docs/spec/norms.md`
- `docs/spec/model.md`
- `docs/spec/adaptation.md`
- `docs/spec/evaluation.md`
- `docs/spec/workflows.md`
- `docs/spec/failure-models.md`
- `docs/spec/domains/software-development.md`

### Governance / evidence boundaries

- `docs/governance/evidence-policy.md`
- `docs/governance/project-evolution.md`
- `docs/research/assurance/studies/v2/assurance-v2-phase-b-interpretation.md`

### Research candidates and carrier decisions

- `docs/research/cognitive-coordination/model.md`
- `docs/research/cognitive-coordination/studies/cross-level-epistemic-probing-replay-2026-08-30.md`
- `docs/research/temporal-coordination/model.md`
- `docs/research/temporal-coordination/studies/temporal-coordination-field-observation.md`

Only **selective cross-level epistemic probing** is implemented as an explicitly candidate Skill in this first bundle.

**Temporal coordination is deliberately not implemented as a Skill.** Its current field-study boundary says that waiting, silent execution, side-chat/rejoin collision, and similar interaction-state phenomena may require an interaction/substrate carrier that can observe or instantiate the relevant state. Forcing those phenomena through a model Skill would test the wrong carrier. If that research branch reaches prototype threshold, it should become a separate interaction/substrate pilot and return evidence to the temporal-coordination model.

Reconstruction, strategic exposure, productive divergence, and other cognitive-coordination candidates remain research concepts unless a current-spec rule independently implies the same local behavior. This is intentional: the pilot tests carrier selection, not maximal conversion of research vocabulary into runtime instructions.

## 3. Carrier architecture

| Responsibility | Carrier | Status | Why |
| --- | --- | --- | --- |
| Stable authority / epistemic / proportionality boundaries | `resident-kernel.md` | current-spec projection | Phase B supports testing a short resident boundary layer as a reliability stabilizer |
| Responsibility ↔ capability response | `human-ai-responsibility-capability` Skill | current-spec projection | Important but conditional; should not add teaching/assessment overhead to every task |
| Evidence / provenance / independence / assurance | `human-ai-evidence-assurance` Skill | current-spec projection | Activated when claims, review, conflict or validation actually bear on decisions |
| Software workflow specialization | `human-ai-software-collaboration` Skill | current domain specialization | Software semantics should not occupy cross-domain resident context |
| Retrospective / collaboration evaluation | `human-ai-reflection` Skill | current-spec projection | End-of-task reflection is conditional and should not become a universal closeout ritual |
| Selective cross-level epistemic probing | `human-ai-cognitive-probing` Skill | **research candidate** | Provides a discriminating runtime test without promoting the mechanism to a norm |
| Temporal waiting / side-chat / rejoin coordination | separate interaction/substrate pilot if evidence threshold is met | **research candidate; excluded here** | The phenomenon can occur while the model is silent or at UI-level state boundaries, so a Skill is not an adequate primary carrier |
| Conversation history / task continuity / branch restoration | host/product capability | delegated | Not a distinctive project collaboration mechanism |
| External repository / web / system evidence | MCP / plugin / native tools when available | capability only | Tools provide access; they do not decide semantic authority |
| Deterministic carrier validation | `scripts/validate_bundle.py` | maintenance support | Good use of scripts: syntax/integrity, not semantic judgment |
| Hooks | none in first bundle | deliberately excluded | Add only if field/runner evidence shows a deterministic first-opportunity miss worth enforcing |

A valid on-demand decision is therefore often **“use no additional carrier.”**

## 4. Resident vs on-demand boundary

The resident kernel contains only rules whose omission can silently damage authority, evidence boundaries, risk acceptance, or substantive human responsibility across domains.

It intentionally does **not** contain:
- a fixed workflow;
- phase × abstraction coupling;
- a cognitive-method checklist;
- a state schema;
- retrospective procedure;
- software-specific roles;
- a mandatory learning mode;
- cross-level probing logic.

Those responsibilities either route to a Skill or remain outside the first pilot.

## 5. Skill family

The family is intentionally independent:

- `skills/human-ai-responsibility-capability/`
- `skills/human-ai-evidence-assurance/`
- `skills/human-ai-software-collaboration/`
- `skills/human-ai-reflection/`
- `skills/human-ai-cognitive-probing/`

No Skill requires the others to activate. Multiple Skills may legitimately co-activate when a task has multiple independent semantic responsibilities, but one Skill must not be loaded merely because another was loaded.

## 6. Host adapters

`resident-kernel.md` is the carrier-neutral source for the resident treatment.

- Codex-like host: use `adapters/codex/AGENTS.md`.
- Host with a system/developer instruction surface: inject the exact resident-kernel content there.
- Host without an always-on instruction surface: the experiment is not equivalent to the resident-kernel treatment; record that as a different carrier condition instead of silently treating a Skill as equivalent.

The Codex adapter is intentionally an exact mirror and is checked by the validation script.

## 7. Old behavior → new owner mapping

The old eval suite remains the broad regression baseline. The vNext decomposition changes **where** behavior comes from:

| Legacy behavior family | vNext owner |
| --- | --- |
| simple facts / low-risk mechanical work / no ceremony | resident kernel + negative Skill triggers |
| substantive human decision space / no rubber-stamp approval | resident kernel |
| responsibility-capability mismatch / learning intensity | responsibility-capability Skill |
| evidence strength / source conflict / independent review | evidence-assurance Skill |
| software phase dependencies / implementation authorization | software-collaboration Skill |
| retrospective appointments / no action-item quota / attribution | reflection Skill |
| state initialization / state lifecycle / generic recovery | host concern; not ported as project Skill |
| cross-level probing / epistemic return edge | cognitive-probing Skill, candidate only |

## 8. Evaluation

### Routing

`evals/routing.json` tests whether the correct Skill set activates—and whether **no Skill** activates in negative cases. It includes paired English / Chinese prompts for selected triggers.

### Behavior

`evals/behavior.json` contains a small discriminating set rather than copying the entire old suite. The old `skills/guide-human-ai-collaboration/evals/evals.json` remains the regression corpus.

Evaluation should distinguish:
- semantic review;
- activation/routing;
- first-opportunity behavior;
- negative/over-trigger behavior;
- reasoning/latency cost where observable;
- field pilot compensation labor and cognitive burden;
- model feedback.

Do not infer carrier validity from this directory structure alone.

## 9. Promotion / deletion rule

This pilot is not a replacement yet.

A later promotion decision should require evidence that the new composition:
1. preserves current-spec boundaries at least as reliably as the old Skill;
2. improves decision-relevant routing or first-opportunity behavior;
3. does not materially increase negative-case triggering or hidden cost;
4. produces useful field evidence for the cognitive candidate rather than merely expressing it cleanly.

If promoted, delete/archive the old Skill unless a concrete compatibility consumer remains. If the candidate mechanism fails, remove or narrow the candidate Skill rather than patching the resident kernel to protect it.
