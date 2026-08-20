# 执行保障 v2 Phase B：外部 Grader Packet Bridge

> 地位：**离线 bridge 与隔离能力审计；不是 scorer 执行授权，也不是正式评分结果。**

## 1. 当前隔离结论

内置协作 sub-agent 可以使用新任务上下文和不同模型，但所有 agent 共享当前容器、文件系统和工作目录；spawn 接口没有 cwd、mount、文件系统 deny 或工具禁用参数。因此，`fork_turns=none` 只能消除对话继承，不能证明 scorer 看不到 repository、其他 outputs 或平台注入上下文。它不能作为已证明的 packet-isolated primary grader。

本机独立 Codex CLI 支持新进程、显式 model、`--ephemeral`、`--ignore-user-config`、`--ignore-rules`、仓库外 `-C`、stdin 输入和 final-output 文件捕获。这能形成更强的 bounded context，但 `read-only` sandbox 主要限制写入，不自动证明 repository 不可读。

主机存在 `bubblewrap`，所以可进一步构建只挂载 runtime、单个 packet 和空 output 的文件系统 namespace。不过 Codex 的认证、模型网络、工具集合和完整 client-injected context 尚未在该 namespace 内完成无评分验证。当前结论是：**技术上存在 Level 2 candidate 的实现路径，但尚未实现/证明，因此不能升级独立性声明。**

## 2. 最强可行候选

后续经人审查的 scorer launcher 应同时满足：

1. 每条 record 创建新的 `0700` 临时目录，位于 repository 外；
2. 只把一个 self-contained `grader_packet.json` 以只读方式暴露给 scorer；
3. 新建且 ephemeral 的 Codex process，不 resume/fork，不加载用户/项目 rules、skills、plugins 或 MCP；
4. 外层 namespace 不挂载 repository、正式 run artifacts、其他 grader outputs 或用户 home；
5. 显式记录 requested model/family、CLI version、可见 injected context、sandbox manifest 与 snapshot unknown；
6. exact packet bytes 和 final JSON bytes 均保存 SHA-256；
7. scorer 无权写 generator record；trusted importer 只追加独立 grade artifact；
8. 用随机 canary 证明 repository/其他 outputs 在 scorer namespace 中不可打开；
9. 模型服务之外的 egress、认证注入与工具可见性需要单独收窄和验证。

全部成立后，可以称为“不同模型家族 + packet/filesystem 隔离的 Level 2 candidate”，仍不能声称完全独立：平台 system instructions、client 实现、认证/TLS、provider routing/retention、共同训练来源和 rubric 设计仍是残余共同来源。

## 3. Runner-side bridge

[`grader_bridge.py`](../../tools/assurance_eval/grader_bridge.py) 只执行离线操作：

```text
canonical fixture / future immutable generator evidence
        ↓
export one grader_packet.json (0600)
        ↓
external scorer execution (本阶段不执行)
        ↓
raw scorer JSON + declared provenance
        ↓
exact schema / allowed values / N/A cross-field validation
        ↓
new append-only imported_grade.json (0600)
```

Importer 会核验 packet/output byte hash、拒绝重复 JSON key、缺失/额外轴和非法 N/A 组合，并再次确认 packet 未改变。它不会覆盖或修改 generator evidence。外部 provenance 的 packet/output hash 由 bridge 验证；执行环境字段仍标为 `externally_declared_not_bridge_verified`，不能靠 scorer 自述自动升级独立性。

## 4. 未执行的兼容性 fixture

[`assurance-v2-grader-contract-compatibility-fixture.json`](assurance-v2-grader-contract-compatibility-fixture.json) 固定使用 `p004` 的 clear / not-applicable rubric 和一条合成 checklist 响应。它包含恰好一个 self-contained scorer packet：case-specific context、隐藏 acceptance boundary、generator final response、逐轴允许值和 required JSON schema。

Fixture 不含 generator reasoning、variant identity/排序、其他 repetition/variant、实验 summary 或 prior grader result。状态为 `prepared_not_executed`；它不是 generator evidence，也没有 scorer output。
