# 人机协作保障机制参考研究

> 地位：**研究与取舍笔记，不是规范正文。**  
> 规范主张：[overview.md](overview.md) · [norm/](norm/README.md)  
> 实验设计与试点结论：[human-ai-collaboration-v1-implementation.md](human-ai-collaboration-v1-implementation.md)  
> 保障需求草稿：[archive/assurance-and-pilot-notes-from-workflow-v0.15.md](archive/assurance-and-pilot-notes-from-workflow-v0.15.md)
>
> 状态：探索结论（已支撑过一次试点；仍可作为以后选型的筛子）  
> 日期：2026-08-09；导航修订 2026-08-10

**一句话**：社区方案已证明若干**机制形态**可复用；人的独立判断与轻量性仍须自研。不整套引入任何框架。

## 阅读地图

1. 先读 §1 结论与 §2 筛选标准  
2. 需要比对来源时再读 §3 机制卡（M1–M7）  
3. 关心「现有框架缺什么」读 §4  
4. 试点后补强的审查/复盘/先例依据读 §7  
5. 具体实验栈与结果读 [v1 实施笔记](human-ai-collaboration-v1-implementation.md)，不要把本文当成安装说明

## 1. 结论

现有社区方案已经证明，以下基础形态无需从零发明：

- 用短常驻规则路由到按需 Skill；
- 用阶段产物保存意图、设计和实施上下文；
- 用人可读文件保存当前状态，使长任务能跨会话恢复；
- 把探索、计划、实施和验证拆成可组合能力；
- 在关键转换点提供「现在在哪、下一步是什么」的导航。

现有方案很少把人的独立判断、自我效能、认知负载和自然表达作为一级目标。如何把这些目标嵌入真实研发任务，同时不明显拖慢交付，仍需要本规范自行设计和验证。

因此不整套引入任何候选框架。保障形式实验采用「抽取机制、缩小范围、逐项试验」。

## 2. 筛选标准

候选机制优先满足：

- 能以常见 Agent 入口（例如 `AGENTS.md`）、Skill 和普通 Markdown **试运行**（不要求一开始就跨产品完美）；
- 普通任务具有快速通道，不要求完整仪式；
- 人能看到目标、假设、取舍和证据，而不只是批准最终计划；
- 状态可读、可纠正、可退出，不依赖隐藏数据库；
- 新增的阅读、命令、文档和维护成本与风险相称；
- 能说明失败和跳过条件，不以自动化程度或项目热度代替效果证据。

## 3. 候选机制卡

### M1：常驻规则路由到按需 Skill

- **来源**：[OpenAI Agents JS 的 AGENTS.md](https://github.com/openai/openai-agents-js/blob/main/AGENTS.md)
- **解决问题**：底线持续生效，复杂流程只在匹配任务时加载。
- **可直接借鉴**：在常驻入口中声明 Skill 的触发条件和授权边界；Skill 承担详细过程。
- **需要改造**：常驻部分必须远小于完整项目手册，避免规则不断累积。
- **主要风险**：触发条件过宽造成所有任务加载 Skill；触发条件过窄导致漏用。
- **实验用途**：只为中高复杂度、跨阶段或明确学习型任务启动协作 Skill。

### M2：Skill 渐进披露

- **来源**：[OpenAI Skills 文档](https://learn.chatgpt.com/docs/build-skills)
- **解决问题**：完整规范常驻会挤占任务上下文。
- **可直接借鉴**：元数据负责发现，`SKILL.md` 负责核心过程，`references/` 按阶段读取，脚本无需全文进入上下文。
- **需要改造**：实验期只保留一个协作 Skill，不提前拆出大量角色和子 Skill。
- **主要风险**：重复内容散落在入口、Skill 和参考文档中，形成多个权威来源。
- **实验用途**：`SKILL.md` 只保存路由和最低充分规则；完整规范作为按需参考（现为 [docs/norm/](norm/README.md)）。

### M3：轻量协议与可回退探索

- **来源**：[OpenSpec](https://github.com/Fission-AI/OpenSpec)
- **解决问题**：需求只存在聊天中，AI 容易补全成不同解释。
- **可直接借鉴**：先探索再提案；人在编码前能检查意图；允许回到任一产物修正，而非只能顺序前进。
- **需要改造**：不是每个任务都生成 proposal、spec、design 和 tasks；简单任务可合并或不持久化。
- **主要风险**：所谓轻量协议仍可能演变成重复文档。
- **试点用法（历史）**：Batch 任务只保留任务文档、实施文档和一个短任务胶囊。

### M4：对话式设计与 Skill 组合

- **来源**：[Superpowers](https://github.com/obra/superpowers) 及其 [brainstorming Skill](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md)
- **解决问题**：AI 未理解意图便直接实施；不同阶段缺少明确责任。
- **可直接借鉴**：自然协作对话、一次推进一个主要问题、方案与权衡、实施前形成可审查设计、完成前验证。
- **需要改造**：问题应先给线索并按认知状态调整，不默认选择题；确认按风险触发，不逐段机械审批。
- **明确舍弃**：所有任务强制完整设计、固定提出多个方案、强制 TDD、自动创建 Worktree 和每阶段提交文档。
- **主要风险**：把正确但适用有条件的实践写成无例外门禁。

### M5：文件化状态与上下文恢复

- **来源**：[GSD](https://github.com/gsd-build/get-shit-done) 及其 [架构说明](https://github.com/gsd-build/get-shit-done/blob/main/docs/ARCHITECTURE.md)
- **解决问题**：长任务、清空会话和上下文压缩后丢失当前位置与关键决定。
- **可直接借鉴**：人可读状态文件；稳定目标、当前状态和阶段上下文分开；新会话只加载需要的部分。
- **需要改造**：将 `PROJECT/REQUIREMENTS/ROADMAP/STATE/CONTEXT` 等多文件压缩为当前任务已有文档加一个任务胶囊。
- **明确舍弃**：大量命令 DSL、默认多 Agent 自动执行，以及绕过权限以追求无摩擦自动化。
- **主要风险**：状态文件过多、相互漂移，维护成本超过恢复收益。

### M6：阶段产物与共同导航

- **来源**：[GitHub Spec Kit](https://github.github.com/spec-kit/) 与 [BMAD 工作流地图](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/docs/reference/workflow-map.md)
- **解决问题**：长任务中不知道当前阶段、输入来自哪里、下一步应做什么。
- **可直接借鉴**：阶段产物作为下一阶段输入；交互式帮助回答「现在在哪、接下来做什么」。
- **需要改造**：阶段是导航而不是流水线门禁；允许合并、回退和跳过；共同航标只强调**一个**下一步，呈现形式仍可迭代。
- **明确舍弃**：把企业中的 PM、架构师、Scrum Master、开发和测试角色全部复制给单人协作，以及为每个角色生产一套文档。
- **主要风险**：角色、阶段和产物数量本身成为虚假的成熟度指标；航标展示不当会变成新的阅读噪声。

### M7：从真实失效逐步增加规则

- **来源**：[Anbeeld AGENTS.md](https://github.com/Anbeeld/AGENTS.md)
- **解决问题**：规则只凭直觉编写，无法判断是否必要。
- **可直接借鉴**：观察失效、比较公开实践、试验修正，再增加或收紧规则；使用同步脚本而非人工复制。
- **需要改造**：不把所有经验继续追加到一个全局文件，成熟机制应路由到 Skill、参考资料或脚本。
- **主要风险**：规则只增不减，最终形成上下文税。

## 4. 需要自行设计和验证的部分

以下主题可以借鉴认知科学和教育研究，但目前没有发现可直接采用的完整研发工作流实现：

- 在 AI 给出完整答案前，怎样以低摩擦方式激活人的预测和已有图式；
- 怎样根据人的可观察表现调节解释深度、问题难度和学习插槽；
- 怎样同时结算任务结果、人的独立能力和人机协作能力，校准自我效能；
- 怎样控制单轮文本长度与知识密度，并在不理解时逐级诊断而非追加长文；
- 怎样接纳故事、经验和跨抽象层表达，同时提取可操作结构；
- 怎样让脚手架随能力增长逐渐撤除，而不是形成新的 AI 依赖；
- 怎样在时间压力下保护业务底线，并允许把学习债务延后偿还；
- 怎样识别双方优先级漂移并低摩擦恢复共同议程。

这些内容构成保障形式实验区别于现有「提高 Agent 交付率」框架的核心假设；规范正文中的原则与机制见 [docs/norm/](norm/README.md)。

## 5. 对实验设计的约束

研究结论对保障形式实验产生以下约束（曾落实为 v1 设计，见实施笔记）：

1. 常驻入口只作启动器和底线，不复制完整规范。
2. 只创建一个协作 Skill，由任务风险和持续性决定加载深度。
3. 优先复用现有任务文档；动态状态只增加一个短任务胶囊。
4. 默认保留自然对话，不要求人记忆命令、角色名或阶段编号。
5. 首先试验共同航标、目标与不变量提取、低负担阶段回顾、人的判断与贡献留痕。
6. 脚本和 Hook 只在观察到可重复失效后加入，不预建完整编排器。
7. 每个新增机制必须说明触发、跳过、失败和删除条件。

## 6. 探索退出条件

当前候选已经覆盖实验所需的规则路由、渐进披露、任务协议、状态恢复、阶段导航和验证模式。继续扩大项目清单的边际收益已经降低。

后续只有在设计遇到具体未知，或新试运行暴露新的失败类型时，才定向回到社区检索。项目 Star 数、功能数量和方法论完整度不作为采用理由。

## 7. 试点后的定向研究

下列条目来自 Batch 试点后的补强，已反馈进规范正文与 Skill references；此处保留证据链。

### 7.1 跨阶段成熟模式检查

试点证明「先参考成熟模式、再决定自行设计什么」不应只用于保障系统选型，而应成为跨阶段的按需行为：任务理解参考领域定义与真实事故，实施讨论参考仓库先例和官方架构，代码实施参考现有惯例与官方 API，审查参考风险导向验证，复盘参考 AAR、debrief 与无责事后分析。

它不是每阶段强制搜索。只在承重、陌生、高风险或已有明显成熟模式的问题上触发，并输出「直接借鉴、约束适配、自行设计/明确舍弃」三类取舍。研究表明，比较具有共同结构的案例比孤立阅读案例更有利于抽取可迁移原则，但先例也可能造成错误锚定，因此仍由当前业务不变量和证据裁剪。[Gentner、Loewenstein 与 Thompson 的类比编码研究](https://groups.psych.northwestern.edu/gentner/papers/GentnerLoewensteinThompson03.pdf)；[National Academies 的学习迁移综述](https://www.nationalacademies.org/read/9853/chapter/15)。

规范对应：[五阶段](norm/02-five-phases.md) 与原则中的先例条款；Skill：`references` 中的阶段检查。

### 7.2 复盘应是共同 debrief，而非 AI 总结

- 46 个样本的 Meta 分析显示，正确实施的 debrief 与约 20%～25% 的绩效改善相关；结构、目标对齐和促进方式会影响效果，不能把「写了一份复盘」当作机制已发生。[Tannenbaum 与 Cerasoli，2013](https://pubmed.ncbi.nlm.nih.gov/23516804/)
- 更大规模的后续 Meta 分析同样支持 AAR/debrief 的总体效果，并指出团队对齐、客观回顾材料和促进方式之间存在交互。[Keiser 与 Arthur，2021](https://pubmed.ncbi.nlm.nih.gov/32852990/)
- AHRQ 的 TeamSTEPPS 将有效 debrief 描述为及时、简短、基于具体事件的团队讨论，既回顾发生了什么，也分析原因、强化做得好的地方并形成下一次改变；它甚至可以短至约三分钟。[AHRQ TeamSTEPPS](https://www.ahrq.gov/teamstepps-program/curriculum/team/tools/debrief.html)
- 在该研究的连续导航训练情境中，同时分析成功与失败比只分析失败更能改善后续表现；这为复盘同时检查有效与失效路径提供了依据，但不直接证明所有任务都具有相同效果。[Ellis 与 Davidi，2005](https://doi.org/10.1037/0021-9010.90.5.857)
- “Debriefing with Good Judgment”主张促进者公开自己的观察和判断，同时探询参与者当时的假设，而不是假装没有判断或单向给结论。这适合转化为 AI 的「观察—担心—询问」表达。[Rudolph 等，2006](https://pubmed.ncbi.nlm.nih.gov/19088574/)
- Google SRE 的无责复盘强调事实、影响、促成因素以及具有责任人和完成信号的行动项；也明确指出复盘有成本，应按事件重要性触发并从小做起。[Google SRE Postmortem Culture](https://sre.google/workbook/postmortem-culture/)

据此并结合本项目的实战失效，作出以下工程化适配（不是论文直接验证的通用定律）：不采用固定长问卷或 AI 自动结算，而以基于真实经历的共同模型修正为核心；事实只在恢复或对齐需要时简述；AI 公开自己的观察与可质疑解释，人通过真实场景、后果比较、反例和迁移参与检验；前序预约作为延迟分析承诺逐项处置；最后才收敛极少数真正执行的重点行动。一个开放问题用于避免开场问卷，不是追问上限；若复盘属于约定范围，人未参与或明确跳过前不得单方面关单。

规范对应：[复盘阶段](norm/02-five-phases.md)；Skill：`review-and-retrospective.md`。

### 7.3 审查应匹配风险与证据，而非堆测试

Batch 试点中「数百个单元测试通过，真实请求仍失败」并不说明自动化测试无用，而说明证据覆盖的层级与真实失效边界不同：隔离单元测试不能证明路由、绑定、序列化、依赖注入、配置、网络和外部系统契约整体可用。Microsoft 官方同样区分单元、集成、功能和服务级验证，并建议限制昂贵集成测试的数量，只覆盖它真正负责的关键场景。[Microsoft ASP.NET Core 测试指南](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/multi-container-microservice-net-applications/test-aspnet-core-services-web-apps)

相关研究和成熟实践进一步约束：

- 控制测试套件规模后，代码覆盖率与故障检出效果只有低到中度相关，覆盖率适合发现未覆盖区域，不适合作为质量目标。[Inozemtseva 与 Holmes，ICSE 2014](https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf)
- 风险导向测试以风险的持续评估指导测试选择，并要求按当前目标裁剪方法，而不是套固定比例。[Felderer 与 Schieferdecker 的风险导向测试分类](https://arxiv.org/abs/1912.11519)
- 现代代码审查的收益不止找缺陷，还包括理解变更、知识传递和形成替代方案；这支持为人提供可理解的审查切片，而不是把几百行代码直接交给人。[Bacchelli 与 Bird，ICSE 2013](https://research.tudelft.nl/en/publications/expectations-outcomes-and-challenges-of-modern-code-review/)
- Google 的官方审查指南同时检查设计、功能、复杂度和测试，并明确反对为未来可能性过度泛化。[Google Engineering Practices](https://google.github.io/eng-practices/review/reviewer/looking-for.html)

由此采用「变化 → 失效模式 → 业务后果 → 证据缺口」模型，再选成本最低但相关性、保真度和判别力足够的证据。编译、静态审查、针对性单测、集成/功能测试、真实请求重放、人工验收和运行观测分别回答不同问题。N+1 等性能怀疑先测量代表数据和业务影响；没有证据或收益时不做优化。真实缺陷也不强制补单测，而是先定位逃逸原因，再决定自动回归、人工验证、发布 smoke 或监控中哪种最耐久。

规范对应：[风险、验证与回退](norm/03-cognitive-mechanisms.md#612-风险验证与回退)；Skill：`review-and-retrospective.md`。
