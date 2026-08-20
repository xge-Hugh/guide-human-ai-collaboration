# 实验记录

本目录保存为检验项目假设、载体形态或执行保障方式而进行的**实验性实现与试点记录**。

实验记录说明“曾经怎样尝试、观察到什么”，不自动取得当前规格权威。载体结构、试点成功和最终任务结果也不能单独证明运行保障可靠；相关主张边界见 [`../governance/evidence-policy.md`](../governance/evidence-policy.md)。

当前内容：

- [`assurance-v1.md`](assurance-v1.md)：首版保障形式的设计、试跑与结论记录；
- [`assurance-v2.md`](assurance-v2.md)：基于当前责任—能力与长期成长规范的执行保障实验计划，先定义保障函数、验收轴与实验顺序，不预选技术载体；
- [`assurance-v2-reference-cases.md`](assurance-v2-reference-cases.md)：v2 Phase A 的初始语义参考案例集；当前 FM-01～FM-20 均已有直接案例和关键近邻反例，暂未出现必须升级的人类规范裁决；
- [`assurance-v2-mechanism-matrix.md`](assurance-v2-mechanism-matrix.md)：按保障函数比较候选机制形态，并定义 Phase B 的最小可解释对照，不把完整产品/框架直接当实验变量；
- [`assurance-v2-phase-b-protocol.md`](assurance-v2-phase-b-protocol.md)：Phase B 的受控回放 / 生态试跑协议，固定信息隔离、独立评价与结果解释；
- [`assurance-v2-phase-b-generation.json`](assurance-v2-phase-b-generation.json) / [`assurance-v2-phase-b-rubrics.json`](assurance-v2-phase-b-rubrics.json)：生成侧测试包与隐藏评价边界，物理分离以降低答案泄漏；
- [`assurance-v2-phase-b-variants.json`](assurance-v2-phase-b-variants.json)：B0/B1/B2 的固定实验变量；这里只是对照输入，不代表正式常驻规则已经选定；
- [`assurance-v2-phase-b-variants.zh-CN.json`](assurance-v2-phase-b-variants.zh-CN.json)：与英文语义源分离并记录 provenance 的中文原生 B0/B1/B2 候选；
- [`assurance-v2-runner-handoff.md`](assurance-v2-runner-handoff.md)：本地 Agent 实现最小可重复 runner 的三方协作与验收契约，明确实现权限、证据隔离和升级边界，不把 runner 结构误当保障本身；
- [`assurance-v2-experiment-owner-guide.md`](assurance-v2-experiment-owner-guide.md)：面向实验负责人的实现—证据桥接说明，解释实验源、renderer、模型参数、证据链和 grader 独立性，不要求负责人承担 Python 操作责任。
- [`assurance-v2-stage3-review-proposal.md`](assurance-v2-stage3-review-proposal.md) / [`assurance-v2-stage3-formal-proposal.json`](assurance-v2-stage3-formal-proposal.json)：Stage 3 首批受控回放的可读与机器可读候选配置；仍保持执行禁用；
- [`assurance-v2-stage3-cloud-review.md`](assurance-v2-stage3-cloud-review.md)：对首版 Stage 3 提案的云端审查记录；
- [`assurance-v2-stage3-grader-capability.md`](assurance-v2-stage3-grader-capability.md)：不含秘密的 grader 隔离、复现、成本与隐私能力边界；
- [`assurance-v2-thinking-compatibility-smoke.json`](assurance-v2-thinking-compatibility-smoke.json)：thinking-enabled 一次调用兼容性 smoke 的禁用候选配置；它不是 Phase B 效果证据。

v2 当前已完成 Phase A 的**结构性基线**、Phase B runner 的 fake 管线和一次明确标记为非效果证据的真实 transport smoke。Stage 3 候选已按云端审查完成离线修订，但 thinking smoke 的成本/隐私、正式预算、grader 与解释细则仍待人批准；当前没有 B0/B1/B2 的正式效果证据，也未授权正式调用。

实验正文保留试点发生时的若干旧目录名和文件名，以维持历史语境；它们不再是当前入口。旧结构到当前位置的对应关系见 [`../archive/README.md`](../archive/README.md)，当前规格与研究入口分别见 [`../spec/README.md`](../spec/README.md) 和 [`../research/README.md`](../research/README.md)。
