# 执行保障 v2 Phase B：实验负责人理解指南

> 地位：**实验理解与审查辅助材料，不是规范正文，不改变 Phase B 协议，也不是 runner 使用手册。**  
> 正式协议：[`assurance-v2-phase-b-protocol.md`](assurance-v2-phase-b-protocol.md)  
> Runner：[`../../tools/assurance_eval/README.md`](../../tools/assurance_eval/README.md)

本文件面向需要批准实验设计、理解证据并裁决边界，但不需要亲自实现或操作 Python runner 的实验负责人。

## 1. Phase B 实际在比较什么

首轮受控回放只比较三种**输入条件**：

- `B0`：普通任务上下文，不加载项目 v2 保障规则；它是模型自然行为基线；
- `B1`：B0 + 少量稳定协作边界；
- `B2`：B1 + 内部适用性 / 时机语义判断框架。

因此，B0/B1/B2 **共同拥有同一个规范评价目标**，但 B0 并没有收到这些规范作为提示。

真正应保持不变的是：

```text
同一 case / 用户信息
同一模型与可识别版本
同一公共 base instruction
同一 request renderer
同一采样 / reasoning / 输出预算设置
同一干净上下文要求
同一运行环境与记录方式
```

首轮理想情况下只改变 `variant`。

## 2. 三个实验源文件分别是什么

### generation packet

`assurance-v2-phase-b-generation.json`

描述被测模型可见的场景事实：

```text
packet_id
pre_context
user_message
```

这些是**刺激 / 输入案例**，不是保障模式。

当前编号 `p...` 对应事件级参考案例的受控回放包；不要把它们与 B0/B1/B2 的 variant 编号混为一谈。

### variants

`assurance-v2-phase-b-variants.json`

当前只有 B0/B1/B2 三个首轮变量。B3 属于条件性后续，不在首轮 JSON 变量中。

### rubrics

`assurance-v2-phase-b-rubrics.json`

这是隐藏评价边界，不是“AI 应该逐字说出的标准答案”。它描述：

```text
什么要求适用 / 不适用
最低充分保护是什么
最晚有用识别点在哪里
案例的裁决状态
```

同一语义保护可以由多种自然语言响应实现。因此 grader 应判断**语义是否实现**，而不是字符串匹配。

Generator 不能看到 rubric；grader 可以看到 rubric 和 generator 原始输出。

## 3. Request renderer 是什么

实验源中的 `pre_context` 是场景摘要，不一定等于真实历史对话。

Request renderer 的职责是把抽象 packet 变成模型 API 真正看到的 messages / request。

例如当前 Stage 2 smoke renderer 位于：

```text
tools/assurance_eval/transport_smoke.py
```

它把：

```text
pre_context
user_message
```

渲染为两条消息：

```text
system: 公共实验指令
user:   【前置上下文】...【用户当前消息】...
```

它故意不把场景摘要伪造成多轮历史对话。

Renderer 是**实验条件的一部分**。如果 renderer 改变，模型看到的实际刺激也改变，因此正式运行必须记录 renderer ID / 内容摘要，并在 B0/B1/B2 之间保持一致。

## 4. 一次正式记录如何形成

```text
checked-in case
      +
selected variant
      +
fixed common settings
      ↓
request renderer
      ↓
exact model-visible request
      ↓
generator model
      ↓
raw output
      ↓
separate grader packet
(rubric + raw output)
      ↓
axis-level grade
      ↓
mechanical summary
      ↓
human adjudication where required
```

Summary 不能替代 raw request / response。

## 5. 模型 snapshot 为什么要记录

模型名称可能是固定 snapshot，也可能只是由服务端动态解析的 alias。

Snapshot 不是“答案质量”的直接指标；一次短时间实验即使只有 alias，也仍然可以产生有价值的观察。

但版本身份影响：

- 以后能否真正复现；
- 数周或数月后 B0 变好 / 变差时，能否区分“模型变了”与“机制变了”；
- 多次运行之间是否可能混入服务端更新。

因此不知道 snapshot 时应明确记录 `unknown/null`，不能虚构版本。

## 6. Temperature 是什么

Temperature 是采样控制之一。一般而言：

```text
更低 → 输出概率更集中、通常更稳定
更高 → 输出分布更宽、通常更多样
```

它不是“聪明程度”旋钮，也不保证 `temperature=0` 完全确定；服务端实现、并行计算、模型路由等仍可能产生差异。

Phase B 需要多次 repetition 的原因之一，就是不要把一次随机生成当作机制表现。

首轮比较中，temperature 等采样条件应在 B0/B1/B2 之间保持相同并记录。若 reasoning / thinking 模式使 temperature 不生效，也应把这一事实记录为平台条件，而不是假装 temperature 仍被控制。

## 7. Thinking / reasoning 与可见 CoT 要分开

至少区分三件事：

1. 模型产生答案必然经过内部计算；
2. provider 可能提供“thinking / reasoning mode”，它会实质改变推理路径、token 使用和模型行为；
3. provider 可能额外返回 `reasoning_content` / 可见 CoT。

可见 CoT 不应被当作模型内部真实因果过程的直接证明，也不应成为 Phase B 的主要评分对象。

Phase B 主要评价**最终第一响应是否在正确时机实现了语义保护**。

但是 thinking mode 本身若会改变模型行为，就属于需要固定并记录的实验变量。首轮不应在 B0/B1/B2 之间同时切换 thinking mode。

## 8. 输出 token 上限不是只有“截断”作用

Stage 2 smoke 的 `256` token 上限只用于 transport 验证，实际已经出现 `finish_reason=length`，所以不能直接复用为正式响应质量实验。

正式 Phase B 应选择一个足够高、使正常案例极少因长度终止的固定输出预算，并在所有 variant 间保持一致。

同时不要假设“越无限越中性”：外部 harness 研究显示，在某些模型 / 环境中 output budget 本身可能改变生成轨迹。因此预算必须被视为可观察实验条件并记录；若以后怀疑其影响，再做单独消融。

## 9. Grader 独立性如何理解

- 同一生成器自评：Level 0，只用于调试；
- 同一模型、独立会话 / 隔离上下文：Level 1；
- 不同模型家族、不同验证路径或人类盲评：更强的 Level 2 候选。

“本地 Agent 与 generator 不是同一模型家族”能够减少部分共享失败来源，但不能自动证明 grader 正确。

实验负责人应重点参与：

- grader 分歧；
- `derived` 案例；
- 会改变 B0/B1/B2 结论的边界；
- 一部分 grader 一致结果的盲抽查。

## 10. B3 与后续 Phase 不要混成一条等级链

B3 不是“B2 更强版”的必经阶段。

只有当 B2 已经稳定识别要求适用，但具体响应仍经常 `partial` 时，才有理由测试 B3：**按需提供更详细局部规则 / 参考**。

“progressive disclosure”可以是 B3 的一种候选实现方式，但不是 B3 的语义定义。

而 Phase C / D / E / F 是不同保障问题的后续实验，例如连续性 / 状态、客观高后果门禁、责任—能力适配与学习、长期轨迹综合。它们不是 B0→B1→B2→B3 的继续编号。

## 11. 实验负责人在 Stage 3 前应能回答什么

不要求背诵脚本。能够基于配置 / artifact 回答下列问题即可：

```text
这次 B0/B1/B2 唯一改变了什么？
模型实际看到了什么？
什么信息被隐藏？
使用了哪个模型 / 哪些身份未知？
采样、thinking、输出预算固定成什么？
一次 repetition 指什么？
原始 evidence 在哪里？
grader 看到了什么、没看到什么？
哪些结果必须升级给人裁决？
什么结果支持 B1/B2 有边际价值？
什么结果不能支持这种结论？
```

能够回答这些，已足以履行实验负责人的实质判断责任；不需要同时承担 Python 实现责任。

## 12. 外部参考如何进入项目

外部 harness / prompt / agent 项目可以提供候选机制和实验方法，但不能因为“某项目得分高”直接成为本项目保障架构。

优先抽取：

```text
它改变了什么变量？
如何做对照 / 消融？
环境和模型如何记录？
有什么重复运行 / 独立复现？
观察到的是能力、轨迹、任务分数还是协作保障？
哪些结论只适用于特定模型 / harness？
```

外部研究的价值首先是帮助我们发现**可能漏控的变量和可复用实验方法**，其次才是候选载体机制。
