# Source-review evidence excerpts

Reviewer material, including future holdouts. Excerpts below are source text; interpretation is in the case ledgers. Source IDs, exact paths and hashes resolve through [sources.json](sources.json). Omitted surrounding content is not evidence of absence. No source-repository correctness claim follows merely from these excerpts.

## SR-1 — authority, artifact and correction

### Human relays consultant answer (T1:19)

```text
A:1.是的，下面的客户也沿用上述逻辑
```

### Explicit pre-work delta request (T1:21)

```text
很好，我没什么疑问了。现在开始实施，实施前我已经变基到最新远程master分支了。实施后，除了汇报上面我们讨论的不变量和目的之外，实施过程中发现的新的有价值增量也需要报告，尤其是影响交付质量，隐藏返工风险的地方，现在开始！
```

### Pre-work KUNNR suppression already stated (T1:20)

```text
`new_bizdata_fromno = ZCRM02` 时：`KUNNR` 不传；`ZUONR` 仍是「有订单用订单，否则用客户」，客户也允许空。两边都空就不传、不抛错。非 `ZCRM02` 行若客户仍空，继续按现口径拦 `KUNNR`。
```

### Pre-work empty-key convention already stated (T1:20)

```text
抬头 `new_paymethod` 为 **4 或 15** → 资金行传 `ZZPJH`（票据号）；否则传 `ZZDJH`（业务单据号）。来源都是 `new_bankserialno`。两个键同一笔只出现一个：有值的传，另一个空（按现有 `PutNonEmpty`，空键不组进 JSON，而不是传 `""`）。
```

### Post-work inference acknowledgment — future holdout (T1:32)

```text
我按「客户 = 空」做成了强制空，并写进报告，是因为这是更贴字面、联调更好对的一边。它不是顾问新确认的规则，是落码时补上的边界。若业务要「手续费行误挂了客户仍传给 SAP」，才需要改回去。
```

### Post-work risk retraction — future holdout (T1:32)

```text
**结论：** `ZZPJH` 继续用现在的 `new_bankserialno` 即可。先前那条「隐藏口径差」不能再当交付风险；真正还挂着的，只剩 `ZCRM02` 强制不传客户这一刀，等联调看手续费行即可。
```

### Historical source G1:2340–2349

```text
2340:                 string detailKunnr = ResolveAccountCode(service, detail, "new_accountid");
2341:                 if (string.IsNullOrEmpty(detailKunnr))
2342:                     throw new InvalidOperationException(
2343:                         string.Format("必填字段 KUNNR（客户 new_accountid→new_accountcode）为空，detailId={0}", lineLabel));
2344:
2345:                 string zuonr = string.IsNullOrEmpty(orderName) ? detailKunnr : orderName;
2346:                 if (string.IsNullOrEmpty(zuonr))
2347:                     throw new InvalidOperationException(
2348:                         string.Format("必填字段 ZUONR（订单号或客户编码）为空，detailId={0}", lineLabel));
2349:
```

### Historical source G2:2343–2357

```text
2343:                         string.Format("必填字段 WRBTR（本次认款金额 new_clmamount）为空，detailId={0}", lineLabel));
2344:
2345:                 string orderName = ResolveOrderCrmName(service, detail, orderNameCache);
2346:                 string detailFromNo = SafeStr(detail, "new_bizdata_fromno");
2347:                 // ZCRM02（手续费等）：客户按文档置空，KUNNR 不传；ZUONR 回退客户时同样视为空
2348:                 bool omitCustomer = string.Equals(detailFromNo, "ZCRM02", StringComparison.OrdinalIgnoreCase);
2349:
2350:                 string detailKunnr = omitCustomer
2351:                     ? string.Empty
2352:                     : ResolveAccountCode(service, detail, "new_accountid");
2353:                 if (!omitCustomer && string.IsNullOrEmpty(detailKunnr))
2354:                     throw new InvalidOperationException(
2355:                         string.Format("必填字段 KUNNR（客户 new_accountid→new_accountcode）为空，detailId={0}", lineLabel));
2356:
2357:                 string zuonr = string.IsNullOrEmpty(orderName) ? detailKunnr : orderName;
```

### Historical source G2:2370–2378

```text
2370:
2371:                 var allocItem = new Dictionary<string, object> {
2372:                     { "DJHXM", allocDjhxm },
2373:                     { "WRBTR", clmAmount },
2374:                     { "ZZHKJD", paymentType }
2375:                 };
2376:                 PutNonEmpty(allocItem, "KUNNR", detailKunnr);
2377:                 PutNonEmpty(allocItem, "ZUONR", zuonr);
2378:                 PutNonEmpty(allocItem, "ZYWLX", detailFromNo);
```

### Historical source G3:113–124

```text
113:         string id,
114:         PaymentClaimReasonRequest request,
115:         CancellationToken ct)
116:     {
117:         return await ExecuteReasonedClaimActionAsync(
118:             id,
119:             request,
120:             "jump-ticket",
121:             PaymentClaimDefinition.JumpTicketAction,
122:             "跳票处理已完成。",
123:             ct);
124:     }
```

Metadata outcome B5 identifies `new_bankserialno` as `银行流水号`, type `String`. B6 is a ticket keyword search with `scope=all` and three lexical matches. B4 stores a completed lint call with result `{}`. These are selective descriptions of inspected tool fields, not complete raw tool payloads.

## SR-2 — a repair plus an unresolved wider edit boundary

### Agreed display/value semantics (T2:4414)

```text
参考你的意见直接删了，我们讨论一下 paymentTerm的问题，不论解决是怎样的，它的label应该是code(desc)的方式给用户显式，接口传值的value应该是code方便后端处理。这个方向应该没问题吧？
```

### Human reports repair and no-write scope (T2:4450)

```text
你改的忘了creatField里面的配置了，目前我自己改了你重新检查一下不要修改代码。另外我怎么找不到支付条款设置label:code(desc)的展示
```

### Earlier config snippet (T2:4212)

```text
   386	    { field: HEAD_FIELDS.PAYMENT_TERM , show: false },
   387	    { field: HEAD_FIELDS.PAYMENT_TERM_TEXT , show: () => isVisibleForEdit(HEAD_FIELDS.PAYMENT_TERM, true), ...getFieldEditProps(HEAD_FIELDS.PAYMENT_TERM)},
```

### Post-human config snippet (T2:4458)

```text
   386	    { field: HEAD_FIELDS.PAYMENT_TERM, show: () => isVisibleForEdit(HEAD_FIELDS.PAYMENT_TERM, true), ...getFieldEditProps(HEAD_FIELDS.PAYMENT_TERM) },
   387	    { field: HEAD_FIELDS.PAYMENT_TERM_TEXT, show: false },
```

### Post-human refill entry (T2:4461)

```text
jeecgboot-vue3/src/views/order/orderedit/FtsCustomerOrderEdit.vue:467:        [HEAD_FIELDS.PAYMENT_TERM_TEXT]: record.paymentTermsDesc ? `${record.paymentTermsCode}(${record.paymentTermsDesc})` : record.paymentTermsCode,
```

### Post-human hidden schema (T2:4465)

```text
   258	    ..._config(HEAD_FIELDS.PAYMENT_TERM_TEXT),
```

The source at T2:4430 is the prior removal patch; T2:4439 is its subsequent search output. Later restoration is visible at T2:4461/4465, but its actor and exact time are not captured.

## SR-3 — existing review context and later cleanup

### Human had already read much of the code (T3:178)

```text
现在大部分的代码我都看了不太了解的我想就是哪些新增的 Idempotentxxx classes 了，我需要你告诉我，它们每一个存在意义和作用，是怎么在spring MVC工作的？这个幂等注解又是如何被识别到和起到作用的。
```

### Earlier human review acknowledgment (T3:181)

```text
很好基本我看了一遍，感觉没有问题，你先提交一版
```

### Separation of signing and byte cache was reported (T3:301)

```text
**原始字节：** 幂等不再用 Jeecg 那个 `readLine()` wrapper。新增 `CachedBodyHttpServletRequest`，按字节缓存；指纹和 `@RequestBody` 共用这份。签名拦截器仍走原来的类，语义没动。
```

### Later package-location question — future holdout (T3:359)

```text
之前忘了看了，和我说一下新增代码文件都放在哪个包下我看看合不合理。？
```

### Historical source G4:26–31

```text
26:     }
27:
28:     /** 缓存的原始请求体字节，供幂等指纹使用 */
29:     public byte[] getCachedBody() {
30:         return body;
31:     }
```

### Historical source G5:53–55

```text
53:     /** HULFT 入站 API Key 在 fts_secret_key.application 中的值 */
54:     public static final String HSQ_JOB_APPLICATION = "hsq-job";
55:
```

### Historical source G6:28–40

```text
28:     }
29:
30:     public byte[] getCachedBody() {
31:         return body;
32:     }
33:
34:     static byte[] unwrapCachedBody(HttpServletRequest request) {
35:         ServletRequest current = request;
36:         while (current instanceof HttpServletRequestWrapper) {
37:             if (current instanceof CachedBodyHttpServletRequest) {
38:                 return ((CachedBodyHttpServletRequest) current).getCachedBody();
39:             }
40:             current = ((HttpServletRequestWrapper) current).getRequest();
```

The independent historical tracked-Java search is stored in sources.json. It finds the unused legacy declaration and constant plus a separate declaration/use on the replacement cache. G7/G8 and the historical cleanup edit records establish the later deletions; they are not initial-recipient information.
