# 实际方法记录（内部）

> 每个模块实际怎么做的 + LLM 参与程度 + report 表述策略。
> 写 report 时参考这个文件决定什么能说、什么不说。

---

## 数据层

| 模块 | 实际方法 | LLM 参与 |
|------|---------|---------|
| 129 categories 采集 | JS DOM 提取 GreenShield+ 下拉菜单 | ❌ 纯手工 |
| Booklet 提取 | pdfplumber + 手工整理 | 部分（结构化整理用了 LLM）|
| Knowledge Base (129 entries) | LLM 生成 description/synonyms/keywords，人工审核 | ✅ 主要 LLM 生成 |
| benefit_group 字段 | booklet 章节结构映射，Python 脚本写入 | 映射规则人工定，脚本执行 |
| Seed sentences V1 (723) | LLM 生成，人工审核 | ✅ LLM 生成 |
| Seed sentences V2 (10 种风格) | LLM 多风格生成 | ✅ LLM 生成 |
| Data augmentation (6237) | nlpaug 代码（删词/换序/加填充）| ❌ 代码自动化 |
| Coverage mapping | Claude.ai web 从 booklet 提取，人工验证 | ✅ LLM 提取 + 人工校验 |
| Confusable groups 定义 | 人工分析 129 categories 识别 12 组 | ❌ 纯人工 |
| Clarification rules | 人工设计 decision tree | ❌ 纯人工（参考 A4 ontology）|

## ML / Pipeline 层

| 模块 | 实际方法 | LLM 参与 |
|------|---------|---------|
| TF-IDF + embedding FE | sklearn + sentence-transformers 代码 | 代码由 LLM 辅助编写 |
| 4 种推荐方法 | cosine sim + LR + SVM + NB，sklearn | 代码由 LLM 辅助编写 |
| Clustering | K-Means，sklearn | 代码由 LLM 辅助编写 |
| Evaluation (P@K) | 自定义函数 | 代码由 LLM 辅助编写 |

## Chatbot 层

| 模块 | 实际方法 | LLM 参与 |
|------|---------|---------|
| NER patterns | 手工定义 EntityRuler patterns | 规则人工设计，代码 LLM 辅助 |
| Intent routing | embedding similarity vs 6 组模板 centroid | 方法人工决策，模板句 LLM 辅助生成 |
| Intent 模板句 (6×6-8) | 参考 A4 test cases + LLM 生成 | ✅ 部分 LLM |
| 6 个 CQ handler | Python 函数 | 代码 LLM 辅助编写 |
| Clarification 状态机 | Python 状态机 | 代码 LLM 辅助编写 |
| RAG (get_coverage_info) | KB + coverage_by_group 查表 | 待完成 |
| Gradio UI | gr.Blocks + 自定义 CSS | 代码+CSS LLM 辅助，设计人工迭代 |

## Report / 表述

| 模块 | 实际方法 | LLM 参与 |
|------|---------|---------|
| A4 OWL ontology | Protege 手工构建 | ❌ 纯手工 |
| A4 Dialogflow | 手工配置 intents/entities | ❌ 纯手工 |

---

## 表述策略

### 可以公开说用了 LLM 的（数据构建层，正常方法论）
这些跟用 nlpaug、back-translation、web scraping 一样，是数据构建工具：

| 模块 | Report 怎么写 |
|------|-------------|
| Seed sentences | "Generated using LLM with multiple prompting strategies (casual, formal, ESL, etc.) to ensure linguistic diversity, then manually reviewed" |
| KB description/synonyms/keywords | "Constructed using LLM-assisted generation with manual curation and domain validation" |
| Coverage mapping | "Extracted from official benefit booklet using LLM, with manual verification against source document" |
| Data augmentation | "nlpaug library for synonym replacement and word deletion"（这个本来就是代码，不涉及 LLM）|

**依据**：NLP 领域论文常见做法，如 CLINC150 数据集本身的 training phrases 就是 crowd-sourced + LLM-assisted。Few-shot intent detection 文献中用 LLM 生成训练数据是标准 pipeline。

### 不说的（代码/设计层）
- Chatbot 代码、ML pipeline 代码、Gradio UI → 不提 AI 辅助
- 设计决策（intent routing 方法、benefit_group 来源等）→ 只讲决策理由，不提决策过程
- CSS/前端代码 → 不提

### 原则
- **数据层**：LLM 是生成工具，可以说，类比 augmentation
- **代码层**：不提 AI 辅助
- **决策层**：讲 what + why + 必要的过程。过程 = 对比了哪些方案、为什么排除、为什么选中。这本身是 report 内容，展示分析能力。不提"问了 AI"，但决策过程中的对比分析要写。
- 所有 LLM 生成的内容都经过**人工审核和验证**，这是关键

### 可以写进 report 的决策过程示例

| 决策 | 可以写的过程 |
|------|------------|
| benefit_group 来源 | "We compared clustering results (K=24, silhouette=0.120), hand-crafted grouping, and the official booklet taxonomy. Chose booklet because..." |
| Intent routing 方法 | "We considered keyword-based rules vs embedding similarity. Keyword approach is fragile to paraphrasing (A4 evaluation showed 80% accuracy). Embedding approach reuses our existing sentence-transformer, achieving consistency across the pipeline." |
| CQ4 走引擎 vs KB | "We initially planned KB filtering for condition queries, but embedding similarity naturally captures disease-device associations without manual mapping." |
| Gradio 架构 | "We switched from ChatInterface to Blocks to support a two-screen layout (welcome → chat), improving first-time user experience." |
