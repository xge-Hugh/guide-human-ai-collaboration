# 项目知识分类与演进

> 地位：**当前项目治理方法**。本文件说明如何把观察、候选主张、研究、规范、失效模型、实现与证据组织成可维护的项目知识。它不直接增加人机协作规范。

## 1. 三个基本问题

维护新内容时，区分三个相互关联但不等价的问题：

1. **它是什么？** —— 语义问题，例如规范、概念模型、评估、工作流、指导、失效模型、观察、hypothesis、study result 或 implementation。
2. **它现在处于什么地位？** —— 认识论/生命周期问题，例如 candidate、current、superseded、historical、parked，或某项 validation 仍待完成。
3. **它主要在哪个维护 / inquiry context 中可被理解？** —— 例如 current specification、cognitive-coordination research、assurance research、executable carrier。

语义类型、当前地位与主要维护上下文不是同一维度。第三项通常由目录和 program README 隐含表达，不要求每个文件重复写 metadata。

一个 candidate norm 与 current norm 可以具有相同语义类型；一个 current research model 也不会因此取得 norm authority。`feedback` 与 `insights` 更接近低成本输入/lineage 位置，而不是知识的最终语义类型。

## 2. 最小维护模型

项目当前只要求四类结构：

### 2.1 知识对象

知识对象是值得独立保存和引用的主张、模型、观察、失效机制、工作流、指导、实验结果或其他项目知识。

分类默认作用于**最小的独立有意义内容单元**，而不是机械作用于整份文件。一份文档可以同时包含多个不同类型或不同成熟度的对象。

### 2.2 当前地位

常用地位：

- `candidate`：值得保留，但尚未成为当前项目立场；
- `current`：当前维护并供读者使用的项目知识；
- `superseded`：曾经成立或被采用，但已被更准确内容取代；
- `historical`：主要为追溯保存；
- `parked`：暂不继续推进，但不删除来源。

`current` 描述知识的**当前有效地位**；不要与工作是否正在进行混淆。Issue 可以是 `open/active`，同时它讨论的某项规范已经是 `current`，而行为验证仍是 `pending`。

若验证状态本身会改变结论，可单独说明 `pending / supported / mixed / failed / unknown`，但不要求所有知识对象都拥有验证字段。价值承诺、经验机制和具体实现需要的证据类型并不相同。

### 2.3 关系

目录说明对象主要放在哪里；重要关系需在不能由位置可靠推断时显式保留。初始关系词汇保持很小：

- `derived from`：由观察、研究或既有内容抽象/产生；
- `supports`：提供支持性证据或理由；
- `threatens`：描述某项规范或目的如何失效；
- `clarifies`：提供理解另一对象所需的概念区分；
- `implements`：某个载体或机制实现另一对象；
- `tests`：探测某个要求或失效是否出现；
- `specializes`：在特定领域或情境中把一般内容具体化；
- `narrows / supersedes`：缩窄或取代旧对象的当前含义。

只有当关系丢失会造成权威误判、追溯断裂、错误推广或重复推导时才记录。不要维护完整知识图谱。

### 2.4 演进记录

只记录会改变语义、权威、适用范围或证据解释的重要变化，例如：

- `candidate → current`；
- 当前主张被缩窄、重分类或取代；
- 一项观察被抽象成失效模型；
- 一个混合历史章节被拆成多个当前对象；
- 新证据改变现有结论的适用范围。

普通措辞修订、链接修复和格式调整不需要单独建立生命周期事件。

## 3. 输入如何进入项目

不要把项目演进理解成固定的 `feedback → insight → norm` 晋升梯。

一个输入可能产生多个出口：

```text
观察 / 想法
  ├─→ 概念模型
  ├─→ 规范
  ├─→ 自适应策略
  ├─→ 评估模型
  ├─→ 工作流或领域专项
  ├─→ 指导/配方
  ├─→ 失效模型
  ├─→ research question / hypothesis / model / study
  ├─→ 行为 eval
  └─→ 搁置 / 否定
```

同一观察也可以同时支持多个下游对象。

推荐处理顺序：

1. **先保存观察与来源。** 记录发生了什么、上下文、后果、未知和可追溯入口，不急于把解释写成事实。
2. **识别实际主张。** 区分观察、因果解释、价值判断、实现建议与待验证假设。
3. **按语义分类。** 使用问题而非关键词判断其属于概念、规范、评估、工作流、指导、失效模型、保障或其他类别。
4. **单独判断地位与范围。** 语义上像规范，不等于已经被项目采用；软件场景有效，也不自动成为跨领域要求。
5. **选择物理归档。** 只有在含义、地位和权威边界已经足够清楚后，才让目录成为它的主要位置。
6. **保留必要关系。** 对重要来源、被威胁规范、测试、实现或取代关系使用普通 Markdown 链接即可。

## 4. 常用判别方法

这些方法是维护工具，不是自动认证器。

### 4.1 跨领域测试

如果更换任务领域后，底层要求仍保持含义，它更可能属于通用层；若依赖代码、编译、接口、实验设计等具体对象，则更可能是工作流或领域专项。

### 4.2 实现可替换测试

如果换一种 Skill、UI、模板、状态系统或技术实现仍可满足目标条件，那么具体载体通常不是规范本身。

### 4.3 规范违反测试

问：若这个条件不成立，我们是否会认为协作本身违反了项目希望保护的人机关系或认识论边界？若只是少了一种方便做法，它更可能是指导或实现。

### 4.4 概念模型测试

问：它是在定义/区分用于表达其他规则的实体、状态或关系，还是在要求参与者必须做某事？前者通常属于语义模型。

### 4.5 失效模型测试

失效模型通常是条件性的：行为 X 在条件 Y 下通过机制 Z 威胁某项目的或规范。不要把一个观察到的负面例子直接反转成无条件禁止规则。

### 4.6 证据边界测试

始终区分：

- 已写出一个规则；
- 已实现规则的某个载体；
- 已定义一个 eval；
- 已执行该 eval；
- 已取得能支持某个具体主张的结果。

载体结构健康、测试定义存在或最终任务成功，都不能自动证明运行时保障可靠。

## 5. 物理目录、主要上下文与权威

项目知识本质上是 graph-like；目录只是一个**可替换的 materialized projection**。目录表达主要维护/检索上下文，并可能在该上下文中提供合理的默认 authority/status 线索，但不是完整语义图，也不能单独决定 truth、evidence strength、normative authority 或永久 conceptual ownership。

不同主要目录可以使用不同分类轴：spec 主要按 semantic/authority responsibility，research 主要按 inquiry cohesion，feedback 主要按 chronological intake，skills/tools 主要按 executable responsibility，archive 主要按 historical lifecycle。

当前约定：

- `docs/spec/`：当前维护的人机协作规格；
- `docs/guidance/`：可替换的交互、表示与模板方法；
- `docs/governance/`：项目自身的分类、演进与证据治理；
- `docs/research/`：主动 inquiry；按 coherent research program 维护 hypothesis、model、external evidence、project study、field observation、interpretation 等；不自动取得规范权威；
- `feedback/`：观察与实战摩擦的低成本入口；
- `insights/`：尚未形成独立 inquiry context 的小型 candidate、design intuition 与 lineage；
- `skills/`：实验性 executable carrier 与行为探针；
- `tools/` / `tests/`：研究/工程使用的可执行基础设施与其代码验证；
- `docs/archive/`：历史与已迁出材料。

历史目录结构和旧兼容路径不作为当前架构的一部分长期保留。若没有已识别的兼容消费者，迁移完成后应由 `docs/archive/`、必要的当前关系链接和 Git 历史承担追溯，而不是继续维护无权威的旧拓扑。

## 6. 何时增加新分类或新目录

不要为了对称或完整而增加目录。

只有当一个重复出现或足够重要的内容类别回答了**现有分类无法无失真表达的不同建筑问题**，才引入新语义类别。

Research program 也遵守同样规则：一个小 hypothesis 不需要独立目录；只有当某个 inquiry 出现 coherent question/model、多个相关对象、独立 evidence/studies、持续 revision 或 downstream consumers，才值得 materialize 成 program directory。

只有当已有足够当前内容、独立维护价值和清楚的 primary context 时，才进一步给对象或 program 单独物理目录。

新的发现若暂时无合适位置，先保留来源并解释为什么现有分类失真；必要时允许修改分类本身。

## 7. 方法本身也可被修订

本文件不是自证正确的元规则。若真实维护显示：

- 分类反复产生歧义；
- 关系记录成本超过收益；
- 不同协作者持续产生相互冲突的解释；
- 新领域出现无法合理表达的重要对象；
- 治理方法本身导致错误权威或流程负担；

则应把这些现象作为项目反馈，修订本方法。未来可变性来自可追溯、可重分类和可取代，而不是试图预先预测所有类别。
