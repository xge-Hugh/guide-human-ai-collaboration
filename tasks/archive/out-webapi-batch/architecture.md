# 实施讨论：SunWard.Out.WebApi Batch 内核重构

> 状态：承重方案已确认，进入代码实施

任务目的、范围、业务不变量和协作目标以 [任务定义](task.md) 为准。本文件只保存实施心智模型、架构决定、理由、风险与验证方法，不重复维护任务状态。

本次采用的核心判断标准是：按变化原因划分职责；协议机制复用，业务语义分离。

## 1. 已确认的协议事实与设计输入

### 1.1 协议事实

- `$batch` 是一次 HTTP 传输容器；外层 item 可以是独立 `application/http` 请求，也可以是嵌套 `multipart/mixed` Changeset。
- Changeset 是一个原子写入单元；其中不允许 GET。
- `ContinueOnError` 只决定一个 Batch item 失败后是否继续处理后续 item，不提供回滚。
- 未继续执行的请求与明确执行失败的请求不是同一状态。
- 网络中断、取消来源不明或响应无法可靠解析时，客户端可能无法确认已执行范围。

### 1.2 人类提出的承重风险

`ContinueOnError=false` 仍可能产生“前项已提交、失败项被拒绝、后项未执行”的部分状态。若业务没有幂等、对账、补偿或断点续跑能力，fail-fast 会留下难以恢复的残局，不能被描述成更安全或接近原子性的模式。

## 2. 候选架构比较

### 2.1 方案 A：继续以 Changeset 执行器为内核

在现有 `ExecuteBatchAsync` 中增加普通 Batch 分支，遇到不同调用模式时决定返回结果或抛 `ChangeSetException`。

优点：

- 表面文件改动较少；
- 容易复用当前异常与结果代码。

问题：

- 中性传输层继续知道 Changeset 业务异常；
- 普通 Batch 和 Changeset 的结果规则会交织在同一个方法中；
- `ContinueOnError`、缺失响应和部分成功容易继续被全成功校验误判；
- 新增其他 Batch 使用方式时需要继续增加条件分支。

结论：不采用。它保留了本次重构要消除的根因。

### 2.2 方案 B：中性 Batch 内核 + 分离的语义解释

底层只编码、发送、解析并返回实际观察到的 Batch 响应；普通 Batch 和单独 Changeset 在上层使用不同规则解释同一类中性结果。

优点：

- 与 Web API 协议结构一致；
- MIME、HTTP 与业务异常解耦；
- 普通 Batch 可以保留部分成功；
- 单独 Changeset 可以保持现有严格契约；
- 后续新增请求映射或 Batch item 类型时不需要重写传输内核。

代价：

- 需要明确区分中性传输结果与公共业务结果；
- 需要重构当前 Codec 的全覆盖校验和 `ChangeSetException` 抛出位置。

结论：推荐。

### 2.3 方案 C：通用执行管线 + 可插拔策略

把验证、映射、发送、关联、错误处理和重试都抽象为通用 stage / policy。

优点：

- 理论扩展性高；
- 可以组合多种执行策略。

问题：

- 当前只有普通 Batch 和 Changeset 两种明确语义；
- 引入策略框架会增加类型、控制流和理解成本；
- 幂等、补偿和重试没有通用业务规则，无法由基础设施安全实现。

结论：暂不采用。未来出现第三种真实语义后再根据重复变化提取抽象。

## 3. 推荐的逻辑分层

```text
业务调用层
├─ 普通 Batch 入口
└─ 单独 Changeset 入口（保持现有契约）
              │
              ▼
组织请求映射与语义层
├─ SDK / 公共请求 → 中性传输操作
├─ 普通 Batch 结果解释
└─ Changeset 严格结果解释
              │
              ▼
中性 Batch 传输内核
├─ Batch → IndependentRequestItem | ChangeSetItem
├─ HTTP POST /$batch
└─ 返回实际收到的 item / operation 响应
              │
              ▼
MIME Codec、HTTP、IFD/ADFS 鉴权
```

这是逻辑职责图，不要求每个方框对应一个新 service 或 interface。编码时优先在现有 `WebApiOrganizationService`、`CrmWebApiClient` 和 `ChangeSetCodec` 中形成清楚的方法边界，只有出现独立变化理由时才新增类型。

## 4. 中性传输内核契约

### 4.1 输入职责

中性内核接收已经完成组织语义映射的传输 Batch：

- 有序顶层 item；
- 每个 item 是一个独立传输请求或一个原子 Changeset；
- 已规范化且唯一的 item ID、operation ID 和 Content-ID 关联；
- 明确的外层继续策略；
- 按真正 wire 子请求数量校验上限。

它不接收 SDK `Entity`、`OrganizationRequest`、业务 DTO 或 Planner。

### 4.2 输出职责

只要服务端响应能够可靠解析和关联，中性内核就返回观察事实，不因子请求非 2xx 直接抛业务异常：

- 收到的成功子响应；
- 收到的明确拒绝子响应；
- 顶层 item 与内部 operation 的关联；
- 响应头、脱敏后的错误信息及上游状态码；
- 没有收到响应的预期 item / operation。

中性内核不能直接把“没有响应”解释为 `NotExecuted` 或“结果未知”。解释需要结合外层继续策略、已收到的失败位置和响应完整性证据。

### 4.3 传输级异常

以下情况由中性内核抛 Batch 传输级异常，而不是 `ChangeSetException`：

- 写 Batch/Transaction 开始发送后发生网络失败或取消；
- 响应 MIME 无法可靠解析；
- Content-ID / 顺序无法唯一关联；
- 响应形态不足以判断哪些操作已执行；
- 外层响应无法证明整批在执行前被拒绝。

写 Batch/Transaction 在发送前收到调用方取消时继续抛 `OperationCanceledException`；一旦开始发送，取消也无法证明 CRM 未执行，因此保守归为结果未知。复用 `$batch` 承载的只读长查询没有副作用，调用方主动取消仍保持 `OperationCanceledException`。发送前参数或白名单错误继续使用参数校验或 `NotSupportedException`，不伪装成上游失败。

## 5. 两种语义解释

### 5.1 普通 Batch

普通 Batch 返回与请求顶层 item 一一对应、顺序稳定的结果，状态至少包括：

- `Succeeded`：该 item 已明确成功；
- `Rejected`：该 item 已执行并被上游明确拒绝；
- `NotExecuted`：有充分证据表明因 stop-on-error 而未执行。

若无法在 `NotExecuted` 与“可能执行但响应未知”之间可靠区分，则整个调用必须报告结果未知，不能猜测。

`ContinueOnError=true` 时，明确的子项失败留在结果中，不导致整个普通 Batch 调用抛原子事务异常。

### 5.2 单独 Transaction

单独 Transaction 仍通过只有一个 `ChangeSetItem` 的传输 Batch 执行，但由严格解释规则收窄结果：

- 全部操作明确成功：返回有序 `IReadOnlyList<CrmOperationResult>`；
- 服务端明确拒绝 Changeset：抛 `TransactionException(Rejected)`；
- 无法可靠确认原子提交结果：抛 `TransactionException(OutcomeUnknown)`。

因此是“同一传输机制、不同公共契约”，不是在中性传输层识别调用者后切换行为。

### 5.3 混合 Batch 中的 Transaction

Changeset 在普通 Batch 中是一个顶层 item：

- 全部成功时该 item 为 `Succeeded`，可携带 Changeset 成功结果；
- 任一内部操作导致原子回滚时，整个 item 为 `Rejected`，并尽可能携带失败 operation ID；
- `ContinueOnError` 只控制失败 Changeset 之后的其他顶层 item 是否继续；
- 不把 Changeset 内其他操作伪造成逐项成功或逐项未执行。

## 6. 继续策略与恢复责任

公共调用层不应把 `ContinueOnError` 暴露成一个看似无害且带默认值的布尔参数。推荐用能够暴露语义的枚举或等价类型，例如：

```csharp
public enum BatchFailureBehavior
{
    Continue,
    Stop
}
```

`AllOrNothing` 不属于该枚举；原子性必须由 Changeset 的结构表达。

失败策略的公共调用方式已经确认：

- 通用 `ExecuteBatchAsync` 的 Batch 模型显式携带 `BatchFailureBehavior`；
- `BatchCreateAsync`、`BatchUpdateAsync` 等便利 CRUD 提供默认 `Continue` 的简短重载；
- 同名重载允许调用方显式传入 `Continue` 或 `Stop`，不要求仅为了首错停止而改用通用 Batch；
- 默认重载只转发到显式策略重载，不复制执行逻辑。

例如：

```csharp
Task<BatchOperationsResult> BatchUpdateAsync(
    IReadOnlyList<Entity> entities,
    CancellationToken cancellationToken = default);

Task<BatchOperationsResult> BatchUpdateAsync(
    IReadOnlyList<Entity> entities,
    BatchFailureBehavior failureBehavior,
    CancellationToken cancellationToken = default);
```

无论采用哪个重载，文档必须说明：

- `Stop` 不回滚已成功项；
- 不应在缺乏幂等保证时整体重试部分成功的 Batch；
- 基础设施不自动补偿或推断安全重试范围。

## 7. 公共入口的推导方向

公共 API 在分层确认后再冻结，但应满足：

- `ICrmOrganizationService.ExecuteBatchAsync(...)` 是普通 Batch 默认入口；
- 公共原子入口命名为 `ExecuteTransactionAsync(Transaction)`；现有六个调用方迁移到该入口，但业务分组与异常语义不变；
- 独立 Batch item 优先使用调用方熟悉的 SDK `OrganizationRequest` 表达；
- Create / Update 等便利方式只是构造受支持 `OrganizationRequest` 的薄封装，不新增平行执行内核；
- 不保留只识别本地包装类型的万能 `ExecuteAsync(OrganizationRequest)`；它没有增加能力，只会与强类型 Batch/Transaction 入口形成重复分派层；
- 不支持的 Request 类型在发送前拒绝；
- 不向业务层暴露 HttpMethod、URL、JSON、MIME boundary 或 Content-ID。

首期 Request 白名单和公共结果类型仍需结合真实调用示例收敛。一个公共独立 item 若会展开成多个非原子 wire 请求（例如包含多个 RelatedEntities 的 Associate），必须显式限制、拆成多个顶层 item，或公开其部分结果；不能隐藏部分成功。

## 8. 对现有代码的最小影响路径

1. 保留现有 Batch item 的真实协议拓扑，将 internal 结构收敛为 `TransportBatch → IndependentRequestItem | ChangeSetItem`，避免与公共类型冲突。
2. 将 MIME codec 调整为保留顶层 item 结构，不在 Codec 中强制所有预期成功响应完整覆盖。
3. 调整 `CrmWebApiClient.ExecuteBatchAsync`：子响应非 2xx 作为中性观察结果返回；传输失败改用 Batch 级异常。
4. 在组织服务层分别实现普通 Batch 与 Transaction 的结果解释。
5. 将六个现有 `ExecuteChangeSetAsync` 调用方机械迁移到 `ExecuteTransactionAsync`，保持分组、成功结果和拒绝/结果未知异常语义不变，不长期保留一套同义公共 Changeset 模型。
6. 分层稳定后，再新增普通 Batch 公共契约、Request 白名单与调用示例。

## 9. 类型经济性审查

### 9.1 当前真实转换链

复杂 PP 调用的出站路径是：

```text
CrmPlannedOperation（PP 内部规划）
  → ChangeSetOperation（公共 CRM 操作）
  → TransportChangeSetOperation（内部 CRM 传输操作）
  → WebApiOperation（HTTP method / URL / body / headers）
  → MIME
```

普通 Changeset 调用没有第一层，但仍然对同一 Create / Update / Delete / Associate / Disassociate 语义建立了两套派生类型，最后再转换成 wire-ready `WebApiOperation`。

响应路径是：

```text
MIME
  → ChangeSetParsedPart
  → BatchOperationResult
  → ChangeSetTransportOperationResult
  → ChangeSetOperationResult
```

这条链中存在真实边界，也存在只复制字段或收窄字段的中转模型。

### 9.2 判断一个类型是否值得存在

一个类型至少应满足以下一项，否则优先删除或收为局部实现细节：

- 表达新的业务或协议不变量；
- 改变基数，例如一个公共关系操作展开为多个 wire 请求；
- 隔离真正独立的变化原因，例如 SDK 请求与 HTTP/MIME；
- 防止调用方构造非法状态；
- 作为稳定边界被多个调用方独立消费。

仅仅因为进入了下一层、需要改变可见性或复制相同字段，不足以证明新类型有价值。

### 9.3 建议保留的模型

- 公共 Batch / Transaction 容器：表达独立与原子的业务选择；
- 一个带 `OperationId` 的公共操作包装：承载 SDK `OrganizationRequest` 和项目关联 ID；
- internal `TransportBatchItem → IndependentRequestItem | ChangeSetItem`：表达真实 MIME 拓扑；
- `WebApiOperation`：唯一 wire-ready 操作模型；
- 一个中性的 transport observation/result：表达实际收到的状态、头、正文、关联与缺失响应；
- 公共 `BatchResult` 和有序 `CrmOperationResult`：分别表达业务可消费的部分成功与原子成功结果。

### 9.4 建议删除或合并的模型

- 五类 `TransportChangeSetOperation`：与公共 CRUD 语义重复，随后仍要转换为 `WebApiOperation`；建议由专用 mapper 直接把公共 SDK 请求转换为一个或多个 `WebApiOperation`。
- `TransportLookupReference`：当前生产代码没有构造点，Lookup 已在组织服务层提前转成 `@odata.bind`，属于未完成迁移留下的死抽象。
- `ChangeSetTransportResult` / `ChangeSetTransportOperationResult`：只是从 `BatchResult` 再投影 `OperationId + Headers`；严格 Changeset 解释可以直接消费中性 Batch 结果。
- `ChangeSetParsedPart` 与 `BatchOperationResult` 的重复字段：Codec 可保留私有 MIME part 语法对象，但关联完成后只保留一个 canonical transport response。
- public `ICrmWebApiClient` 上的 internal 默认接口成员：可见性和调用分派已经造成真实缺陷。Web API client 是项目内部适配器，应形成一致的 internal 边界，不通过 public interface + internal member + 默认抛错实现隐藏协议类型。

### 9.5 公共 Changeset 类型的兼容性分叉

最简公共操作模型可以是：

```csharp
public sealed record CrmOperation(
    OrganizationRequest Request,
    string? OperationId = null);
```

- 普通独立 Batch item 持有一个 `CrmOperation`；
- `Transaction` 持有有序 `CrmOperation` 集合；
- Create / Update / Delete 等便利方法只负责构造 SDK request；
- mapper 通过封闭白名单将一个公共操作转换为一个或多个 `WebApiOperation`；
- Changeset 上下文禁止查询，普通 Batch 使用更宽但仍封闭的白名单。

这会消除五类 public `ChangeSetOperation` 派生类型，因为 SDK request 已经表达 CRUD 类型。代价是 Changeset 的允许操作从编译期封闭类型转为发送前白名单校验。

当前已确认不把现有 public Changeset 操作层次作为必须保持的源码兼容契约：使用单一“`OrganizationRequest + OperationId`”包装，同时移除内部 `TransportChangeSetOperation` 重复层。既有 endpoint 的业务行为仍是不变量。

### 9.6 推荐的最简链路

```text
公共 CrmOperation(OrganizationRequest + OperationId)
  → 白名单、校验、必要的一对多展开
  → WebApiOperation
  → TransportBatchItem
  → MIME

MIME
  → 私有解析结构
  → 中性 TransportBatchResult
  ├─ 普通 Batch 解释 → public BatchResult
  └─ Transaction 严格解释 → CrmOperationResult / TransactionException
```

PP Planner 可以保留自己的 `CrmPlannedOperation`，但它只属于复杂 PP 业务内部，最终应直接映射到公共 `CrmOperation`，不成为普通 Batch / Changeset 的使用门槛。

## 10. 公共结果模型与首期白名单草案

### 10.1 最小公共结果模型

以下类型只用于暴露当前讨论的形状，尚未冻结。public 结果不复制 transport 的 headers、body 和 reason phrase，只表达业务调用方需要的执行状态、标准 SDK 响应和安全失败信息；失败结果是否保留可机器判断的状态码仍需在公共契约确认时决定。

```csharp
public enum BatchItemStatus
{
    Succeeded,
    Rejected,
    NotExecuted
}

public sealed record CrmOperationResult(
    string OperationId,
    OrganizationResponse Response);

public sealed record BatchOperationResult(
    string OperationId,
    BatchItemStatus Status,
    OrganizationResponse? Response,
    string? ErrorMessage);

public sealed class BatchOperationsResult
{
    public IReadOnlyList<BatchOperationResult> Items { get; }
    public IReadOnlyList<BatchOperationResult> Succeeded { get; }
    public IReadOnlyList<BatchOperationResult> Rejected { get; }
    public IReadOnlyList<BatchOperationResult> NotExecuted { get; }
    public bool AllSucceeded { get; }

    // 构造时由内部实现完成一次分类，业务调用方不需要重复解析状态。
    internal BatchOperationsResult(/* ... */);
}

public sealed class BatchItemResult
{
    public string ItemId { get; }
    public BatchItemStatus Status { get; }
    public IReadOnlyList<CrmOperationResult> Operations { get; }
    public string? ErrorMessage { get; }
    public string? FailedOperationId { get; }

    // 由内部工厂创建，避免产生互相矛盾的字段组合。
    internal BatchItemResult(/* ... */);
}

public sealed record BatchResult(
    IReadOnlyList<BatchItemResult> Items);
```

实际编码时应通过 internal 构造或工厂保证合法组合：

- 独立请求成功：`Operations` 恰好一项，错误字段为空；
- Transaction 成功：`Operations` 包含全部公共逻辑操作；
- `Rejected`：`Operations` 为空，`ErrorMessage` 存在，`FailedOperationId` 尽可能关联失败操作；
- `NotExecuted`：`Operations` 为空，错误字段为空；
- 无法证明未执行时抛 Batch 级结果未知异常，不增加含义模糊的第四种 item 状态。

Create 的记录 ID 由标准 `CreateResponse` 提供，不在 `CrmOperationResult` 再保存一份可能不一致的 `RecordId`。若调用便利需要，可提供从 `CreateResponse` 计算的只读属性。

首期公共结果不暴露上游 HTTP 状态码；它不是业务状态，内部只在 Transaction 异常和网关日志映射中保留。若以后出现按具体上游状态码分支的真实消费者，再单独评估稳定契约。

单独 `ExecuteTransactionAsync(Transaction)` 返回有序 `IReadOnlyList<CrmOperationResult>`；明确回滚和结果未知使用不同的 `TransactionException` 分类。Batch 内 Transaction 的明确回滚只形成一个 `Rejected` item，不抛单独 Transaction 异常。

### 10.2 通用结果与便利结果的边界

人类指出：如果普通 `BatchUpdate` 调用方也要先遍历 Batch item、再遍历 item 内操作，双重循环说明混合 Batch 的通用结构泄漏到了常用便利入口。

这个观察已经确认“便利入口不应迫使调用方理解混合 Batch 的两层拓扑”，边界是：

- 通用 `ExecuteBatchAsync(Batch)` 必须保留两层，因为一个顶层 item 可能是包含多条操作的 Transaction；
- `BatchCreateAsync`、`BatchUpdateAsync` 等便利入口只创建独立 item，应提供一项对应一个输入 Entity 的扁平结果；需要原子性时调用对应的 Transaction 便利入口。

便利入口只投影通用结果，不建立第二套执行逻辑：

```text
BatchUpdateAsync(entities)
  → 构造多个独立 CrmOperation
  → ExecuteBatchAsync(batch)
  → 将每个单操作 BatchItemResult 投影为扁平结果
```

因此“薄适配”允许少量输入构造和结果投影；它禁止的是复制校验、发送、解析和失败判断。扁平结果是公共业务视图，不取代保留 item / Transaction 分组的通用结果，也不暴露 transport headers 或 body。

已确认采用带常用分类视图的 `BatchOperationsResult`，消费方式是：

```csharp
var result = await BatchUpdateAsync(entities);

if (result.AllSucceeded)
{
    // 全部完成
}

var rejected = result.Rejected;
var notExecuted = result.NotExecuted;
```

只有业务需要逐条处理多个失败记录时才遍历 `Rejected`；此时循环表达的是真实业务动作，而不是迫使调用方理解通用 Batch 的嵌套结构。便利 CRUD 采用扩展方法作为薄适配，默认 `Continue`，并提供同名重载显式选择 `Continue` 或 `Stop`；通用执行仍只有 `ExecuteBatchAsync` 一个内核。

### 10.3 首期 Request 白名单

首期已确认只覆盖现有组织服务已经具备明确映射、且不会隐藏非原子部分成功的请求：

| SDK Request | 普通 Batch 独立 item | Transaction | 说明 |
| --- | --- | --- | --- |
| `CreateRequest` | 支持 | 支持 | 一项对应一个 POST |
| `UpdateRequest` | 支持 | 支持 | 一项对应一个 PATCH |
| `DeleteRequest` | 支持 | 支持 | 一项对应一个 DELETE |
| `RetrieveRequest` | 支持 | 不支持 | GET 不允许进入 changeset |
| `AssociateRequest` | 首期仅单个 RelatedEntity | 支持 | 普通 Batch 不能隐藏多请求部分成功；Transaction 内可原子展开 |
| `DisassociateRequest` | 首期仅单个 RelatedEntity | 支持 | 同上 |
| `RetrieveMultipleRequest` | 暂缓 | 不支持 | 分页可能触发 Batch 外后续请求，需先定义一页还是全集语义 |
| Action / 其他 Request | 暂缓 | 暂缓 | 当前 Out.WebApi 没有统一白名单映射与响应契约 |

白名单是发送前校验，不表示任意 `OrganizationRequest` 都能透传到 Dataverse。后续新增 Request 类型时，主要增加“SDK Request → `WebApiOperation`”映射、结果解码和上下文合法性校验。

代码核对补充：

- 当前同步 `IOrganizationService.RetrieveMultiple` 只发送一次请求，解析时丢弃 `@odata.nextLink`，因此只返回一页；这是现有同步接口的独立风险，不由本次 Batch 重构引入。
- 当前异步 `ICrmOrganizationService.RetrieveMultipleAsync` 会沿 `@odata.nextLink` 继续请求并合并全部页面。PP18～PP21 的仓储按业务查询条件分块，每一块仍依赖该异步接口完成协议分页；“条件分块”和“结果翻页”是两层机制。
- 一个 `$batch` 中的 `RetrieveMultipleRequest` 天然只产生一页响应。若收到 `nextLink` 后继续请求，后续请求已经离开原 Batch；若只返回一页，又会与现有异步组织服务的“返回全集”语义不同。因此首期暂缓，不能直接复用现有全分页实现。
- Dataverse Action 是可通过 Web API `POST` 或 SDK `OrganizationRequest` 调用的平台消息；仓库中所谓 Plugin Action，是注册在该消息执行管线上的插件处理器，并非同一种客户端类型。当前 Out.WebApi 尚无 bound/unbound URL、参数、返回值和事务许可的通用映射。
- 部分现有 Action 会调用 ERP 等外部系统，这类外部副作用不会随 Dataverse changeset 回滚。首期普通 Batch 与 Transaction 均暂缓任意 Action；后续出现真实消费者时，按具体 Action 显式增加映射，并单独判断是否允许进入 Transaction。

该首期白名单已由人类确认：本次不支持 `RetrieveMultipleRequest` 与 Action，不把分页语义和任意 Action 映射扩入 Batch 重构范围。

## 11. 验证方法

未经授权不运行编译、构建或测试。进入代码实施后至少需要人工验证以下响应形态：

- 全部独立请求成功；
- 独立请求部分失败且继续；
- 独立请求首错停止，后续明确未执行；
- 单独 Transaction 成功；
- 单独 Transaction 明确回滚；
- 混合 Batch 中 Transaction 失败后继续；
- 网络中断、主动取消、不可解析响应和无法关联响应；
- 一个公共关系操作展开多个 wire 请求时的数量与结果关联。

## 12. 实施状态

已按以下确认方向完成首轮代码实施并进入静态独立审查：

> 以中性 Batch 传输内核作为唯一协议执行机制；普通 Batch 和单独 Transaction 在组织语义层分别解释结果；不为未来可能性提前建设通用策略框架。类型链只保留公共组织语义、唯一 wire 操作模型和中性传输结果，避免每层复制一套 CRUD 类型。

中性内核、分离解释以及单一公共操作包装方向已经确认。命名采用按受众分层的方式：业务公共入口使用 `Transaction`；内部 Batch item 使用 `ChangeSetItem`，直接对应 OData/Dataverse changeset 协议结构。`Changeset` 是 wire 概念而不是另一层 C# DTO，不再额外建立与 `ChangeSetItem` 形状相同的协议类型。`Atomic` 作为语义说明保留在文档中，不重复进入类型名称。

公共结果消费方式、首期 Request 白名单以及便利 CRUD 的默认 `Continue` + 显式策略重载均已确认。当前实现已建立公共 `Batch / Transaction / CrmOperation`、中性 `TransportBatchResult`、保留顶层拓扑的 MIME codec，并迁移六个既有原子调用方。

首轮独立审查及首次人工编译反馈发现并已修复七项问题：Create ID/Retrieve 响应映射遗漏、空正文 `application/http` 的 CRLF 被误删、`NotExecuted` 使用过宽的历史失败证据、多顶层 item 对直接 `application/http` 的不安全关联、只读长查询取消语义回归、Retrieve 成功正文解码异常未收敛，以及标识校验 helper 在迁移中遗漏。写 Batch/Transaction 在“开始发送后取消”时保守归为结果未知。

验证进展：人类已完成生产项目编译并确认成功，测试工程已完成旧 Changeset 契约迁移；外部验证已覆盖实际运行场景。现有测试作为回归护栏，不再为追求形式覆盖扩大本次范围。补充修复：MIME 子响应剥除 boundary 前多余 CRLF；`InvalidOperationException` 的 `ApiResponse.Code` 与 HTTP 400 对齐。

## 13. 复盘与收口

- 结果：公共业务语义收敛为 `Batch / Transaction / CrmOperation`，传输层保留 `IndependentRequestItem / ChangeSetItem / WebApiOperation`，MIME 层不再承担业务成败解释。
- 人类贡献：明确普通 Batch 的“尽量成功”默认语义、指出首错停止的业务残局风险、推动删除重复操作类型、要求便利 CRUD 返回扁平结果，并决定暂缓 RetrieveMultiple 与 Action。
- 模型修正：不能把 Changeset 协议结构直接当公共业务模型；缺失响应只有在连续前缀以明确拒绝结束时才能判断为 `NotExecuted`；写请求开始发送后的取消必须按结果未知处理。
- 协作改进：独立静态审查发现了多项协议边界问题，但遗漏的标识校验 helper 最终由人工编译暴露。后续同类重构应在首次完整切片后更早安排人工编译，减少纯静态审查盲区。
- 留待真实需求：`RetrieveMultipleRequest` 的分页语义、Action 映射与事务许可、业务幂等/补偿/重试策略均不在本次范围。
