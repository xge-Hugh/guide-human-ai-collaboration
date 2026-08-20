# 执行保障 v2 Phase B：Stage 3 Grader 能力声明

> 地位：**不含秘密的候选能力与成本边界说明，不是 grader 选择或正式调用授权。**

## 1. 首选候选：直接不同系列无状态 API grader

- provider / model / family：transport 仍是本地配置的自定义隔离 provider，不宣称为官方 Qwen API；grader outbound model identifier 固定候选为 `qwen3.7-max`，按人工提供的 model ID/路由声明归为 Qwen 系列，但尚未由 API 响应验证；服务端 snapshot 未知。generator 继续使用 DeepSeek 系列的 `deepseek-v4-flash`。
- 配置边界：同一私有连接可以列出两个获准模型，但 generator 和 grader 必须分别显式选择 model ID；不能靠“列表第一个”或临时覆盖来决定角色。当前外部配置据人工说明只列出 DeepSeek，因此兼容性调用前还需把 Qwen 作为第二个模型加入，而不是替换 generator。
- context isolation：每条评分仅发送一个 standalone Chat Completions POST，不传 session、历史会话或其他输出。模型端没有 agent workspace、repository mount 或文件工具；它只接收 canonical grader packet 的固定渲染。
- visible context：只包含 case-specific normative/rubric context、隐藏语义边界、generator 最终响应、评分轴/允许值、N/A 条件和 JSON schema；不包含 generator reasoning、其他 variant/repetition、预期 B0/B1/B2 顺序、汇总或 prior grade。
- reproducibility：本地私有 artifact 保留 exact effective model-visible request、raw JSON output、renderer ID/content hash、配置/声明/provider-reported model identity、参数、elapsed time 和数值 usage。alias 解析、backend identity/seed、custom routing、snapshot 与服务端注入仍不可控。
- tools / reasoning：请求不发送 tools；候选兼容性条件显式 `thinking={"type":"disabled"}`，不发送 reasoning effort、temperature 或 top-p。无论 provider 是否额外返回 reasoning content，都不得保存或作为评分证据；只保存返回时的数值 reasoning-token usage。
- cost / privacy / retention：本地材料没有 Qwen 路由的价格、配额或 retention 声明。兼容性单调用和 90-call 正式 grader batch 都尚未获成本/隐私批准，不能从此前 DeepSeek generator smoke 的一次授权推导出来。

现有窄 Chat Completions transport 能表达该请求，但 `qwen3.7-max` 的可用性、`thinking=disabled` 接受情况、JSON-only 遵循、usage/identity 字段和无工具行为仍需一次**零重试、非效果证据**兼容性测试确认。测试配置已准备但保持 `execution_enabled=false`。

若该测试通过，可声明“不同模型系列 + 独立 standalone context”的 **Level 2 candidate**；不能声明 provider 级完全独立，因为 generator 与 grader 仍共享 custom routing、运营边界和可能的后端基础设施。

## 2. 可选次级隔离实验：Codex CLI + bubblewrap

独立 Codex CLI、仓库外 ephemeral cwd 和 filesystem namespace 仍可用于可选 secondary review/canary，但不再是 primary grader 的先决条件。其认证、模型网络、工具集合和完整 client-injected context 尚未验证，本轮不执行。

内置协作 sub-agent 共享文件系统，只能作为 bounded human-supervised reviewer，不能声称 repository isolation。

## 3. 同系列 Level 1 fallback

同一自定义 provider 上的 `deepseek-v4-flash` grader 能形成 standalone context，但与 generator 同系列，只支持 Level 1。它不是默认降级路径；只有后续人明确批准 fallback 的实验含义、成本和隐私边界后才能启用。

## 4. 调用量与批准边界

10 cases × 3 variants × 3 repetitions 对应 90 次 generator 与 90 次 primary grader，零重试时主路径最多 180 calls。primary grader 的 1,024-token 输出上限对应 92,160 completion-token ceiling，另加输入；generator 的候选 4,096-token 上限对应 368,640 completion-token ceiling。

这是中等调用批量、按最坏输出上限为中高 token 暴露，不能据此推导货币价格。任何 secondary review calls 尚未冻结数量，必须在执行前加入人类批准的调用、货币、配额和 retention 硬上限。`execution_enabled` 在实际 grader、能力边界与成本/隐私获批前保持 `false`。
