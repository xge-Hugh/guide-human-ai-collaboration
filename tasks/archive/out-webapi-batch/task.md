# SunWard.Out.WebApi Batch 重构任务

## 目的

把当前围绕 Changeset 形成的执行内核重构为中性的 Batch 基础能力，并在业务组织服务层同时开放普通 Batch 与原子 Changeset，使外部集成业务能够方便、清晰地使用 Dataverse Web API 批处理。

本任务同时作为轻量人机协作工作流的首个真实试点，但学习与流程维护不得明显阻塞业务交付。

## 范围

- 普通 Batch：允许独立请求部分成功，并返回稳定、可关联的逐项结果；
- 原子 Transaction：同组写操作通过协议 Changeset 共同成功或共同失败，保持现有严格业务行为；
- 混合 Batch：外层可以有序包含独立请求与 Transaction；
- 组织服务层提供便利调用与承载 `OrganizationRequest` 的通用 Batch/Transaction 入口，共享同一 Web API Batch 内核。

## 关键业务不变量

- 既有有效 endpoint 的业务行为不能因重构失效；
- 现有单独原子调用继续保持“全成功返回、明确拒绝抛业务拒绝异常、无法确认抛 `OutcomeUnknown`”；公共命名迁移为 `Transaction` / `TransactionException`，不保留同义 Changeset facade；
- PP18～PP21、SAP 发货回传和调拨出库的原子分组与业务编排本次不变；
- 普通 Batch 的部分成功不是异常情况，调用方必须能够消费逐项结果；
- `ContinueOnError` 只控制首错后是否继续，不提供回滚；
- 基础设施不推断业务幂等、补偿、对账或重试策略。

## 非目标

- 不重做 PP18～PP21 的业务原子边界与 Planner；
- 不提前建设通用策略、补偿或重试框架；
- 不把内部 HTTP、MIME、URL、Content-ID 等协议类型暴露给业务调用方；
- 不在本任务中建设跨产品工作流同步、Hook 或通用治理平台。

## 成功观察

- 既有 endpoint 与单独 Changeset 行为保持不变；
- 普通 Batch 能表达全部成功、部分失败、首错停止和结果未知；
- 公共调用不需要理解 `$batch`、MIME 或内部传输模型；
- 新增受支持的 Request 类型主要增加映射与校验，不重写发送和解析流程；
- 公共、组织语义、wire 和 MIME 各层不存在仅为可见性或字段复制而建立的重复 CRUD 类型。

## 协作与学习目标

- 人负责业务目的、不变量、公共语义和承重架构取舍；
- AI 负责代码调查、候选设计、影响分析和后续实现；
- 解释较底层 C# 实现时，先用基础循环或小例子建立语义，再按需介绍 LINQ 等简写；
- 不把语法熟悉度等同于架构判断能力，也不把单次表现固化成永久能力标签。

## 历史上下文

- [历史 Changeset 任务定义](../../out-webapi-transaction-task.md)
- [历史 Changeset 实施设计](../../out-webapi-changeset-impl.md)

历史文档保留协议语义、已有约束和历史取舍，但其中“仅完善 Changeset”及“已进入代码实施”的状态已被当前任务取代。
