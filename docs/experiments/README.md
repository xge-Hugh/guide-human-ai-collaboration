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
- [`assurance-v2-phase-b-variants.json`](assurance-v2-phase-b-variants.json)：B0/B1/B2 的固定实验变量；这里只是对照输入，不代表正式常驻规则已经选定。

v2 当前已完成 Phase A 的**结构性基线**并准备好 Phase B 的平台无关执行包；这仍不表示任何保障载体已经运行、通过或获得可靠性证据。下一步是在选定的最小 runner / 客户端上执行受控 B0/B1/B2 回放，并保留相对独立的评价路径。

实验正文保留试点发生时的若干旧目录名和文件名，以维持历史语境；它们不再是当前入口。旧结构到当前位置的对应关系见 [`../archive/README.md`](../archive/README.md)，当前规格与研究入口分别见 [`../spec/README.md`](../spec/README.md) 和 [`../research/README.md`](../research/README.md)。
