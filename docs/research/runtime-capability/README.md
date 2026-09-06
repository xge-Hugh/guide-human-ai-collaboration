# Runtime capability research

本 program 研究：在人和 AI 已经拥有当前项目规范与理论、但底层模型参数通常不可由项目直接修改的条件下，**项目知识如何转化为可靠、成本相称、可持续改进的运行时协作能力**。

这里关注的不是“再写一个更完整的 Skill”，也不是假定基础模型缺少一般推理能力。核心问题是：一个已经较强的模型，如何在具体协作情境中及时识别相关理论、构造有用表示、检索权威知识、调用或重激活已有程序，并让历史运行证据改善未来的引导方式。

当前核心对象：

- [`model.md`](model.md)：runtime capability formation 的候选研究模型；
- [`evidence-review.md`](evidence-review.md)：项目内部观察、Phase B 结果与外部研究的证据综合；
- [`design-diagnoses/static-context-carrier-gap.md`](design-diagnoses/static-context-carrier-gap.md)：当前 resident kernel + conditional Skill 为什么可能只能提供有限稳定化，而不能等同于理论掌握或累计熟练度。

## 与其他 program 的边界

- [`../cognitive-coordination/`](../cognitive-coordination/README.md) 研究人和 AI 的任务模型、认知分配、证据接触、修正、重建与跨表示探针。本 program 不接管这些认知机制本身；它研究这些机制**如何被模型可靠激活和承载**。
- [`../assurance/`](../assurance/README.md) 研究 carrier reliability 与可执行验证。Runtime-capability hypothesis 可以由 assurance study 检验，但不能因有一个实现或 eval 就获得成立地位。
- [`../../spec/`](../../spec/README.md) 仍是当前规范权威。这里的 intrinsic-first、context orchestration、guidance experience 等均是 research candidates，不直接产生新的用户义务或 AI 义务。
- `skills/`、pilot、MCP、memory、prompt、retrieval service 等是可能的实现面，不是本 program 的概念边界。

## 当前研究问题

1. 哪些协作能力已经存在于基础模型中，只需要被识别、激活或校准？
2. 哪些能力真正需要项目特定知识、外部证据、程序性表示或跨会话持久化？
3. 上下文的内容、顺序、时机、选择者与重激活方式如何改变模型对任务和协作理论的工作表示？
4. Skill、resident rule、主动阅读、检索、例子、counterexample、工具与 memory 应分别承担什么最小职责？
5. 运行经验能否被表示成“什么引导在什么模型/情境下有效”，并经验证后改善未来 capability elicitation？
6. 如何防止外部架构重复模型已经擅长的认知，从而增加 token、延迟、仪式化和错误锚定？
7. 如何让外部持久化结构积累能力而不让模型自己的未经验证反思直接污染 canonical theory？

## Authority boundary

这是 research program，不是 carrier specification。当前模型主要提供问题分解、候选机制与可检验假设；最终 runtime architecture 仍需要 project study、field evidence 与 assurance 共同约束。
