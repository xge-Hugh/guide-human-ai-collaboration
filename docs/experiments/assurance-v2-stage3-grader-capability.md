# 执行保障 v2 Phase B：Stage 3 Grader 能力声明

> 地位：**不含秘密的候选能力与成本边界说明，不是 grader 选择或正式调用授权。**

## 1. 主路径候选：本地已配置 API 模型

- model / family：配置的 outbound model identifier 为 `deepseek-v4-flash`；服务端 snapshot 未知。它与 generator 属同一 DeepSeek-like 模型家族，不能仅凭另开请求宣称更强模型独立性。
- context isolation：现有 adapter 声明每条 record 使用独立 standalone Chat Completions 请求，不携带 session 或历史状态；这支持 Level 1 上下文隔离，但不能切断模型、训练或服务端路由的共同失效来源。
- repo / other outputs：API 只收到固定 grader renderer 产生的消息，不会被提供 repo、其他 variant/repetition 输出或 generator reasoning。provider/client 是否注入未披露上下文仍未知。
- reproducibility：实际 model-visible grader prompt 与最终原始输出可逐字保存在本地私有 artifact；renderer ID、源码/内容摘要和参数必须同时记录。provider alias、后端路由、snapshot、seed 与服务端注入使模型行为不能完全复现。
- reasoning：grader 只看 generator 最终 `content`；generator/grader 的 reasoning 文本都不保存或作为证据。provider 返回时可保存数值 reasoning-token usage。
- cost / privacy / retention：本地非秘密配置没有价格、配额或账户成本资料，货币成本未知。每条 grader call 会向同一 provider 发送 rubric/语义边界和 generator 原始响应；服务端 retention 与二次使用策略当前未声明，必须由人审查后才可批准。

因此，该路径当前只能作为 **Level 1 primary candidate**，尚未获准调用。

## 2. 不同家族本地 coding-agent 候选

- model / family：可选择与 generator 不同的 Codex 模型家族作为第二审查路径；具体 model/version 尚未冻结。
- context isolation：可以为单条 record 创建新任务上下文，但当前 coding-agent harness 仍带平台指令、工具与工作区能力。
- repo / other outputs：无法以当前 harness 技术性保证它不读取 repo、其他 outputs 或线程注入上下文，因此不能只因模型家族不同就标为 Level 2。
- reproducibility：显式 user prompt 和最终输出可保存，但平台/客户端注入、模型 alias 与工具环境使完整可见上下文和行为重现不充分。
- cost / privacy / retention：当前仓库没有可审查的价格、配额、数据保留或账户边界；在这些信息获批前不得作为正式 grader 自动运行。

该路径可在严格限制输入后作为 derived、disagreement、conclusion-sensitive 与 blind sample 的 **secondary human-supervised review candidate**，而不是当前 primary Level 2 证据。

## 3. 调用量与批准边界

10 cases × 3 variants × 3 repetitions 对应 90 次 generator 与 90 次 primary grader，零重试时主路径最多 180 calls。primary grader 的 1,024-token 输出上限对应 92,160 completion-token ceiling，另加输入；generator 的候选 4,096-token 上限对应 368,640 completion-token ceiling。

这是中等调用批量、按最坏输出上限为中高 token 暴露，不能据此推导货币价格。任何 secondary review calls 尚未冻结数量，必须在执行前加入人类批准的调用、货币、配额和 retention 硬上限。`execution_enabled` 在实际 grader、能力边界与成本/隐私获批前保持 `false`。
