# 多视角 Review 备忘

> 开发时的审查视角和注意点。每个设计决策用相关视角过一遍。
> 2026-04-04 创建，4/5 更新

## Review 视角定义（6 个，每步选相关的用）

| # | 视角 | 关注什么 | 典型问题 | 什么时候用 |
|---|------|---------|---------|---------|
| 1 | **教授/Rubric** | 评分项覆盖、学术性、推荐系统语言 | "这算 recommender 还是 classifier？" | 每个决策 |
| 2 | **数据科学家** | 方法论、评估公平性、数据质量 | "train/test 同源？silhouette 0.12 能用？" | ML 相关决策 |
| 3 | **工程实现** | 代码结构、可运行性、边界情况、依赖 | "Run All 会卡吗？函数签名改了下游要不要改？" | 写代码、提交前 |
| 4 | **Reference 对比** | 别人怎么做、我们有没有依据 | "CLINC150 用 SVM 做 intent，我们为什么不用？" | 方法选择 |
| 5 | **用户/演示** | UX、demo 效果、队友能不能看懂 | "返回 66 条有意义吗？2 分钟能演示完吗？" | UI、交互、发代码给队友 |
| 6 | **Report 叙事** | 怎么讲故事、决策过程怎么写、工作量 vs 收益 | "这个设计决策能一句话说清依据吗？值不值得花 2 小时？" | 每个决策 |

**不是每步都用 6 个**。举例：
- 改 CSS → 5
- 选 intent routing 方法 → 1/2/4/6
- 写 coverage mapping → 2/3/4
- 整理提交物 → 3/5/6

---

## 教授视角

### ⚠️ Recommender 的"推荐"感不够强（最重要之一）
**问题**：框架更像"分类系统+chatbot"，如果 report 通篇说 classification，教授会觉得没做 recommender。
**改进**：
- **项目标题改成**："GreenShield ClaimBot: A Content-Based Recommender System for Insurance Claim Category Selection"（原标题偏 classification）
- Report 和 notebook 中全程用推荐系统语言——F: U×I→S, item ranking, top-N recommendation, relevance score
- 开一节叫 "Recommender Engine Design"，用 formal definition 开头
- 术语替换：classify → recommend, predicted category → recommended item, accuracy → 旁边加 Precision@K
- 代码变量名也要体现：`recommend()` 不是 `classify()`，`top_n_recommendations` 不是 `predictions`
- **这是贯穿整个项目的意识，不是写完再改的事**

### ⚠️ Innovation 说不清
**问题**："真实场景+pipelined hybrid"太泛。
**改进**：用数字讲故事——"We demonstrate that combining content-based retrieval with rule-based clarification achieves 85%+ accuracy on 129 highly overlapping categories where single-turn classification only reaches 60%." 创新点 = single-turn vs multi-turn 的提升��度。

---

## TA 视角

### ⚠️ 依赖管理
**问题**：sentence-transformers 第一次运行下载模型 ~90MB，TA 网络慢会卡。
**改进**：README 写清预下载命令 `python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"` 或提交时附带缓存。

### ⚠️ Chatbot demo 怎么跑
**问题**：TA 打开 notebook 不会自动看到 chatbot。
**改进**：README 写——"Run All cells. The last cell launches the chatbot in-browser via Gradio."
- 现在全在 notebook 里（gr.Blocks），不需要单独 app.py
- 最后一个 cell `demo.launch()` 自动弹出浏览器窗口

---

## 数据科学家视角

### ⚠️ 训练集和测试集太相似（最重要）
**问题**：seed 是 LLM 生成，augmentation 是同义词替换。训练集和测试集可能风格相同，导致 evaluation 指标虚高。
**改进**：
- 训练集 = Yangchun + Claude/LLM 生成 + 同义词替换扩充
- 测试集 = 两位队友各自独立生成（不同来源、不同风格）
- 三人的 seed 差异化方式：
  - 不同 LLM / 不同 prompt 风格
  - 从 Reddit、论坛抽取真实用户提问
  - 换 prompt 角度（"不懂术语的学生怎��问" vs "详细描述的用户"）
  - 不同语言能力（简单口语 vs 详细专业描述）
  - 回忆真实 claim 经历
- Report 里说明分离策略和三人各自的方法

### ⚠️ 129 类的 class imbalance
**问题**：confusable groups 每类 8-10 seed，独特类别 3-5 seed，本身不均衡。
**改进**：
- 用 macro-F1（不受 imbalance 影响）作为主指标，已在 proposal 里写了
- report 里说明差异化投入是有意为之，并讨论对结果的影响
- 可以做一个对比实验：均匀 seed vs 差异化 seed 的效果

### ⚠️ cosine similarity 和 classifier score 尺度不同
**问题**：cosine sim 是 0-1，predict_proba 也是 0-1 但分布不同，不能简单加权融合。
**决定**：不做 ensemble，4 种方法分别跑、分别评估、对比选 champion，放进最终 chatbot。
- 4 种方法：cosine sim (embedding) + LR + SVM + NB
- 对比表格展示 Precision@K
- 选 champion 后分析"为什么赢"（数据科学家视角）
- Error analysis：每种方法错在哪类 category、为什么
- **数据局限性**：训练数据有限（每类 20-30 条 augmented），champion 未必在真实数��上最优。Report 加 limitations 段落诚实讨论，到时候看实际准确率再调整

---

## 项目架构师视角

### ⚠️ 先跑 clustering 再写 decision tree
**问题**：如果提前手写 12 组 decision tree，跑完 clustering 发现 groups 不一样，要重写。
**改进**：
- 执行顺��：knowledge base → clustering → 确定最终 groups → 再写 decision tree
- 代码里 decision tree 做成 config 驱动（JSON/dict），改 groups 只改配置不改逻辑
- Report/notebook 里明确说明这个顺序和理由："We first ran clustering to discover natural category groups, then designed clarification rules based on the clustering results, rather than hand-crafting groups upfront."

### 代码结构决定
**决定：全放 notebook，不做 app.py**
- Gradio 在 notebook 里 `demo.launch()` 直接跑 chatbot
- TA Run All 一路看到 chatbot
- 演示时 `share=True` 生成公开链接，浏览器全屏打开
- 可选：部署到 Hugging Face Spaces（免费永久链接），到时候看时间
- Report 里放 chatbot 截图/录屏作为备份

### 4/5 新增设计决定
**Gradio 架构**：从 `gr.ChatInterface` 改为 `gr.Blocks`
- 双屏：Welcome Screen（标题+输入框+examples）↔ Chat Screen
- Welcome 发送第一条消息后切换到 Chat
- New Chat 按钮回到 Welcome
- 状态管理用模块级 dict（不用 gr.State，避免 additional_inputs 兼容问题）

**Intent routing**：embedding similarity 而非 keyword if/elif
- 跟推荐引擎共享同一个 sentence-transformer
- NER 只负责实体提取，不参与 intent 判断
- 架构上对应 CRSLab 的 policy module

**benefit_group**：从 booklet 官方章节归类（20 组），不用 clustering 结果
- Clustering 保留在分析层（发现 pattern + 验证分组 + error analysis）

---

---

## Error Analysis 注意点（Rubric 3%）

Error Analysis 不只是说"错了"，要说**为什么错、错的特征是什么**：

| 层面 | 分析什么 |
|------|---------|
| 算法对比 | 4 种方法各自错在哪类，cosine sim 搞不定的 classifier 能搞定吗？ |
| Category 级别 | 哪些 category 最容易推荐错？confusable groups 错最多 |
| Confusion pairs | 具体哪两个 category 最容易混淆？看 TF-IDF 权重词重叠度 |
| Clustering vs 推荐 | clustering 聚出来的 group 跟推荐错误的 pattern 一致吗？ |
| 单轮 vs 多轮 | 加 clarification 后修正了哪些错误？还有哪些修不了？ |

可解释性融入 error analysis：每次推荐展示 TF-IDF 权重最高的词（"因为你提到了 knee 和 compression"），分析时也用这些词解释混��原因。不需要 SHAP。

---

## RAG 注意点

### 教授视角
- Requirements 明确写了 "RAG"，教授 feedback 强调 "Grounding, Trustworthiness"
- RAG 在我们项目里 = 推荐结果附带 booklet 报销条款，让用户 trust 推荐
- Report 里要用 "grounded recommendation" 这个术语

### 数据科学家视角
- Coverage 信息来源必须是 booklet 原文，不能自编
- 有些 group 在 booklet 里没有单独条款（如 Diagnostic Tests），要标明

### UX 视角
- CQ1 推荐结果附 coverage：用户看到类别 + co-pay + limit 才能确认
- CQ6 覆盖查询：回答核心就是 coverage 信息
- Coverage 信息不能太长，提取关键数字（co-pay, limit, conditions）

### Reference 视角
- CRSLab 的两通道输出（结构化推荐 + NL 解释）
- 我们的 RAG = 结构化 coverage 数据 + NL 回答模板

---

## 总结：开发时必须注意的 Top 5（4/5 更新）

| # | 事项 | 何时注意 |
|---|------|---------|
| 1 | 测试集要跟训练集风格/来源不同 | 生成 seed 和划分数据时 |
| 2 | Report 用推荐系统语言，不是 classification 语言 | 写 report 和 notebook markdown 时 |
| 3 | RAG 必须用 booklet 原文数据，不能自编 | 写 coverage mapping 和 get_coverage_info 时 |
| 4 | 每个设计决策用多视角审查（见顶部表格） | 每一步 |
| 5 | cosine sim vs classifier 分别展示对比，不做 ensemble | 写 evaluation 时 |

---

## 初跑结果（V1 only, 723 seed）

| Method | P@1 | P@3 | P@5 |
|--------|-----|-----|-----|
| Cosine (Emb) | 90.3% | 98.6% | 99.3% |
| SVM | 71.7% | 91.0% | 92.4% |

## V1+V2 合并结果（1613 seed, 6237 augmented）

| Method | P@1 | P@3 | P@5 |
|--------|-----|-----|-----|
| **SVM** | **98.9%** | **99.8%** | **99.8%** |
| NB | 97.4% | 99.6% | 99.8% |
| LR | 97.0% | 99.8% | 99.8% |
| Cosine (Emb) | 84.1% | 96.1% | 99.0% |
| Cosine (TFIDF) | 82.1% | 96.4% | 97.9% |

- Cosine P@1 从 90.3% 降到 84.1%——多样风格数据让评估更严格，更真实
- Confusable group P@1: 77.5%, Standalone: 92.0%
- Top confusion: compression stockings 压力等级、insulin 设备类型
- 性能提升图：single-turn 84.1% → top-5 99.0% → after clarification ~99%+
- Classifier 数字仍可能偏高（train/test 同源），Cosine 更可靠
- 等队友独立测试集验证后更新
