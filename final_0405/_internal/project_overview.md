# GreenShield ClaimBot — 项目总览

> 最后更新：2026-04-05 晚
> 给队友看这个文件了解全貌
> 开发进度和 bug 清单见 `dev_status.md`

---

## 1. 项目基本信息

- **课程**：DSA/GNG 5125，Group 27
- **项目名**：GreenShield ClaimBot: A Content-Based Recommender System for Insurance Claim Category Selection
- **技术栈**：Content-Based Recommender (F: U×I→S)。TF-IDF + Sentence Transformer embedding 做文本特征，cosine similarity + LR/SVM/NB 做推荐对比，spaCy EntityRuler 做实体提取，embedding similarity 做意图分类，rule-based clarification 做多轮追问，booklet 数据做 RAG grounding，Gradio 做 chatbot 界面

---

## 2. 整体理解

每次 Run All 做两件事：

**第一件：训练 + 准备（Cell 0-27）**——加载数据 → 生成文本特征（TF-IDF + embedding）→ 训练 5 种推荐模型并对比 → 选出最佳模型。同时把以下东西加载到内存：
- sentence-transformer 模型（后面意图分类和推荐都用它）
- 129 个类别的 embedding 向量（推荐时直接查表比对）
- 6 组意图模板的 centroid embedding（意图分类时比对）
- clarification rules（追问逻辑）

**第二件：启动 chatbot（Cell 28-35）**——加载 NER patterns、RAG coverage 数据、对话逻辑，然后启动 Gradio 界面。

**用户每次发消息，chatbot 实时做以下处理（不再训练，只是用已加载的模型算相似度）：**

```
用户输入 "I bought compression socks from the pharmacy"
  ↓
Step 1: 边界检查 — 是不是 hi/help/空？是 → 回引导语，结束
  ↓
Step 2: 意图分类 — 用 embedding similarity 判断用户想干什么（6 种类型之一）
         → 这里判断为 CQ1（推荐类别）
  ↓
Step 3: NER 实体提取 �� 识别出 "compression socks" 是 MEDICAL_ITEM
  ↓
Step 4: 调用推荐模型 — 用训练阶段跑好的 cosine embedding 模型，
         算用户输入和 129 个类别的相似度，返回 top-5
  ↓
Step 5: 判断是否需要追问 —
         top-1 和 top-2 分数差距大（>0.1）→ 直接推荐 top-1
         top 几个属于同一 confusable group → 进入追问流程
         → 这里 top 几个都是 Compression Stockings 类别，进入追问
  ↓
Step 6: 追问 — 按预定义规则逐步问：footless? → custom? → length? → pressure?
         用户每轮用数字选择
  ↓
Step 7: 输出最终推荐 + RAG coverage 信息（从 booklet 提取的报销条款）
  ↓
Step 8: Follow-up — "Any questions? Or describe your item in more detail."
         用户可以说 yes（确认）/ no（看其他选项）/ 新描述（回到 Step 2）
```

不是所有查询都走 Step 4-6。6 种意图的处理路径不同：

| 意图 | 例子 | 走推荐模型？ | 可能追问？ | 附 coverage？ |
|------|------|-------------|----------|-------------|
| CQ1 推荐类别 | "I bought compression socks" | ✅ | ✅（confusable group 时） | ✅ |
| CQ2 浏览 group | "What can I claim under dental?" | ❌ 直接从 KB 过滤 | ❌ | ❌ 列出类别 |
| CQ3 问区别 | "Custom vs non-custom brace?" | ✅ 找到 group | ❌ 展示对比 | ❌ |
| CQ4 按疾病查 | "I have diabetes" | ✅ | ❌ 列出相关类别 | ❌ |
| CQ5 问组件 | "CPAP mask vs supplies?" | ✅ 找到 group | ❌ 列出组件 | ❌ |
| CQ6 查覆盖 | "Is massage covered?" | ✅ | ❌ | ✅ 直接给 |

CQ1 是主线（大部分用户查询），其他 5 种是辅助查询。

追问（clarification）走的是**预定义规则系统**（Cell 23 的 clarification_rules），不走推荐模型。推荐模型只负责判断"这个查询属于哪个 confusable group"，之后的逐步追问完全由规则 decision tree 驱动。

### 2.1 第一部分：数据 → 模型（Cell 0-27，跑一次出结果）

```
1. 数据准备（Cell 2-11）
   - knowledge_base.json：129 个 claim 类别的结构化信息（名称、描述、同义词、属性）
     → 这是推荐系统的 Item 内容
   - seed_sentences：为每个类别生成的训练句子（V1+V2 共 1613 条，augment 后 6237 条）
     → 这是训练数据，模拟用户怎么描述各种 claim
   - EDA：3 张图分析类别分布、confusable groups、query 长度

2. 特征工程（Cell 12-14）
   - TF-IDF 向量：词频统计，给 LR/SVM/NB 分类器做输入
   - Sentence Transformer embedding：语义向量，给 cosine similarity 推荐做输入
   - 目的：把文本变成数字向量，模型才能算相似度

3. 聚类分析（Cell 15-17）
   - K-Means 对 129 个类别的 embedding 聚类
   - 用途：发现哪些类别语义接近，验证我们手工定义的 confusable groups 是否合理
   - 不直接用于 chatbot 推荐，是分析层（为 Error Analysis 和 report 提供数据）

4. 推荐引擎对比（Cell 18-21）
   - 5 种方法：Cosine Sim (Embedding) / Cosine Sim (TF-IDF) / LR / SVM / NB
   - 用 Precision@K 对比选 champion
   - Chatbot 实际用 Cosine Embedding（不依赖训练数据，泛化更好）
   - SVM/LR/NB 的高分数可能因 train/test 同源虚高

5. 追问规则定义（Cell 22-23）
   - 9 组 confusable group 的追问规则
   - Compression Stockings 是树形（4 步分支：footless? → custom? → length? → pressure?）
   - 其他 8 组是线性（1-2 步）：Brace / CPAP / Glucose Monitoring / Walker / Social Worker / Insulin / Crutches / Stimulator

6. 评估 + 错误分析（Cell 24-27）
   - 性能提升对比：single-turn P@1 (84.1%) → top-5 (99.0%) → after clarification (~99%+)
   - 按 confusable/standalone 分组分析错误率
   - Confusion pairs + TF-IDF 可解释性
```

### 2.2 第二部分：Chatbot 对话（Cell 28-35，启动后实时运行）

```
用户输入
  ↓
边界检查：hi/help/空 → 引导语
  ↓
意图分类（embedding similarity，6 种查询类型）：
  CQ1 推荐类别    → 走推荐引擎（主线，最常见）
  CQ2 浏览 group  → 从 KB 过滤列出（不走引擎）
  CQ3 问区别      → 展示 confusable group 属性对比
  CQ4 按疾病查    → 走推荐引擎
  CQ5 问组件区别  → 展示产品线组件列表
  CQ6 查是否覆盖  → 走推荐引擎 + 附 coverage 信息
  ↓
NER 实体提取（spaCy EntityRuler）
  → 识别 body part / medical item / benefit group / condition 等，供各 handler 使用
  ↓
推荐 + 判断是否追问：
  - top-1 远高于 top-2 → 直接推荐 + coverage 信息
  - top 几个属于同一 confusable group → 进入追问流程（编号选择）
  - 不属于任何 group → 展示 top-3 供选择
  ↓
追问（clarification）：
  - 逐步追问区分属性，用户用数字选择
  - 最终给出唯一推荐 + RAG coverage 信息（来自 GreenShield booklet 原文）
  ↓
Follow-up：
  - 推荐后："Any questions? Or describe your item in more detail."
  - 列表后："Reply with a number to see details."
  - 用户说 yes → 确认 / no → 回到列表 / 新描述 → 重新推荐
```

对话的状态管理、回复格式、数字选择、yes/no 处理等详细规范见 `dialogue_framework.md`。

### 2.3 关键设计决策

| 决策 | 结果 | 原因 |
|------|------|------|
| 推荐方法 | Cosine Embedding（不是 SVM/LR 尽管它们分数更高） | 不依赖训练数据，泛化更好 |
| 意图分类 | Embedding similarity vs 6 组模板 centroid | 跟推荐引擎共享同一个 sentence-transformer |
| NER 职责 | 只做实体提取，不参与意图判断 | 意图用 embedding 更准 |
| benefit_group 来源 | booklet 官方章节（20 组），不用 clustering 结果 | booklet 是用户认知的分组方式 |
| Clustering 定位 | 分析层（验证 groups + error analysis），不用于生产 | silhouette 0.12 说明类别天然不紧密 |
| Collaborative Filtering | 不用 | 没有用户历史数据 |

---

## 3. 当前进度（4/5 晚更新）

详细 bug 清单和修复记录见 `dev_status.md`。

| 项目 | 状态 |
|------|------|
| Knowledge Base (129 entries + benefit_group) | ✅ |
| Seed V1+V2 (1613 条) + augmentation (6237 条) | ✅ |
| Notebook (36 cells) | ✅ |
| ML pipeline (4 种方法 + P@K) | ✅ |
| 6 CQ + Intent routing + Clarification | ✅ |
| Gradio UI (Blocks, 双屏) | ✅ |
| Coverage mapping (RAG) | ✅ |
| 对话框架重写（P2/P4/P5/P6 + 树形 clarification） | ✅ |
| EDA section (3 张图) | ✅ |
| Intent routing 验证 (96.6%) | ✅ |
| 对话输出格式优化 | 🔧 进行中（T1-T8） |
| Report / PPT / README | ❌ 未开始 |

### 推荐引擎结果（V1+V2 合并，1613 seed，6237 augmented）

| Method | P@1 | P@3 | P@5 |
|--------|-----|-----|-----|
| **SVM** | **98.9%** | **99.8%** | **99.8%** |
| NB | 97.4% | 99.6% | 99.8% |
| LR | 97.0% | 99.8% | 99.8% |
| Cosine (Emb) | 84.1% | 96.1% | 99.0% |
| Cosine (TFIDF) | 82.1% | 96.4% | 97.9% |

注意：SVM/NB/LR 数字可能因 train/test 同源而虚高。Cosine similarity 不依赖训练数据，更可靠。Chatbot 用 Cosine (Emb) 作为推荐引擎。

---

## 4. 分工（4/5 更新）

### 统筹（Yangchun）
- Report 初版框架 + 统稿
- README
- 代码首版框架（已完成）+ 最终整合
- 测试统筹
- PPT 整体结构

### 三人各自负责

| | 模块 A：数据与特征 | 模块 B：推荐与评估 | 模块 C：对话与展示 |
|---|---|---|---|
| **Notebook** | Cell 0-14 + data/ | Cell 15-27 | Cell 28-35 |
| **代码深化** | 独立 seed 测试集、药品名→NER、KB 审核 | Evaluation 指标补充、Error Analysis 深化、Clustering 图表 | Chatbot 交互 bug 修复（见 dev_status.md）、Clarification 审核、Coverage 文案 |
| **Report** | Data Prep + FE + NER | Clustering + Recommender + Evaluation + Error Analysis | Clarification + Demo + Visualization |
| **测试** | ~30 个 test case | ~15 个 test case | ~30 个 test case |
| **PPT** | 各讲各的 | 各讲各的 | 各讲各的 |

### 测试方法
1. Run All → 最后一个 cell 启动 chatbot
2. 按 `test_cases.md` 测试：New Chat → 输入 → 截图 → 填评价
3. 格式 bug 自己改（参考 `dialogue_framework.md`）
4. 准确度 bug 记录后发群，统筹判断改哪里
5. 改完跑 `python _internal/test_dialogue.py` 验证（1 秒，不需要 Run All）

### 参考文档
- `dev_status.md` — bug 清单 + 修复记录
- `dialogue_framework.md` — 对话交互规范
- `review_notes.md` — 多视角审查
- `test_cases.md` — 75 个测试用例
- `method_log.md` — 方法记录 + 表述策略
- `references.md` — 参考资料

---

## 5. 时间线（4/5 更新）

| 日期 | 任务 |
|------|------|
| 4/4 周六 | ✅ 框架定型 + 第一版代码 + V1+V2 数据 |
| 4/5 周日 | ✅ 对话框架重写 + EDA + 测试脚本 + 分工 |
| 4/6 周一 | 代码分发 + 三人各自深化代码 + 测试 |
| 4/7 周二 | 代码定稿 + Report 各写各章节 |
| 4/8 周三 | Report 统稿 + PPT |
| 4/9 周四 | 最终检查 + 提交 |

---

## 6. 关键决策（已确认）

| 决策 | 结果 | 原因 |
|------|------|------|
| 推荐系统类型 | Content-Based | 教授课堂推荐 + 有 item 内容 + 无用户历史 |
| Chatbot 界面 | Gradio | 简单直接，不用 N8N |
| NER | spaCy EntityRuler（规则式） | 领域封闭，规则够用 |
| 数据增强 | 简单 augmentation（删词/换序/加填充） | WordNet 不适用，back-translation 不需要 |
| Ensemble | 不做 | 分别对比选 champion |
| N8N / FastAPI | 不用 | 教授说 alternative，Gradio 替代 |
| Surprise 库 | 不用 | 非 collaborative filtering |

---

## 7. Rubric 覆盖检查

| Rubric 项 | 分值 | 覆盖 |
|-----------|------|------|
| Problem Formulation | 2.5% | ✅ |
| Data Preparation | 2.5% | ✅ |
| Clustering | 3% | ✅ K-Means + silhouette + 对比手工 groups |
| Feature Engineering | 3% | ✅ TF-IDF vs embedding 对比 |
| Recommender (≥3 算法) | 3% | ✅ cosine sim + LR + SVM + NB = 4 种 |
| Evaluation | 4% | ✅ P@K + classification metrics + clustering + end-to-end |
| Error Analysis | 3% | ✅ confusion pairs + per-group + 可解释性 |
| Visualization + Demo | 3% | ✅ Gradio chatbot + 性能提升图 |
| Innovativeness | 1% | ✅ 真实场景 + single→multi-turn 提升 |
| Presentation + Report | 5% | 待完成 |

---

## 8. 文件结构

```
final/
├── Group27_Final_ClaimBot.ipynb        ← 主 notebook（36 cells，Run All 跑全部 + 启动 chatbot）
├── data/
│   ├── knowledge_base.json             ← 129 category KB（名称/描述/同义词/属性/benefit_group）
│   ├── seed_sentences_all.csv          ← V1+V2 seed (1613 条)
│   ├── train_augmented.csv             ← augmented 训练数据 (6237 条)
│   ├── coverage_by_group.json          ← RAG coverage 数据（从 booklet 提取）
│   └── source/                         ← 原始数据文件
├── _internal/
│   ├── [入口]
│   │   project_overview.md             ← 本文件：项目全貌、技术流程、分工
│   ├── [开发]
│   │   dev_status.md                   ← bug 清单 T1-T10 + 修复记录 + 计划
│   │   dialogue_framework.md           ← 对话规范 + 待实现设计（8.1-8.3）
│   │   review_notes.md                 ← 多视角审查要点
│   ├── [数据]
│   │   benefit_groups_list.txt         ← 20 组 benefit group 完整列表
│   │   coverage_mapping.py             ← coverage 生成脚本（优化 RAG 时用）
│   │   coverage_mapping.json           ← coverage 完整版数据
│   │   prompt_for_claude_web-*.md      ← AI 提取 coverage 的 prompt
│   │   method_log.md                   ← 方法记录 + LLM 参与度 + 表述策略
│   ├── [测试]
│   │   test_cases.md                   ← 75 个手动测试用例
│   │   test_dialogue.py                ← mock 自动测试（65 tests，1 秒）
│   │   test_deep.py                    ← 多轮对话场景测试
│   │   test_screenshots/               ← 测试截图
│   ├── [参考]
│   │   references.md                   ← 参考项目/教程/数据集
│   ├── [UI 开发]
│   │   chatbot_ui_dev.ipynb            ← UI 前端单独开发用（mock 数据，改完同步到主 nb）
│   └── _personal/                      ← 个人临时脚本（不用看）
```

---

## 9. 方法与 LLM 参与度

> 写 report 时决定怎么表述。详见 `method_log.md`。

### 可以公开说用了 LLM 的（数据构建层）
| 模块 | Report 表述 |
|------|------------|
| Seed sentences | "Generated using LLM with multiple prompting strategies, then manually reviewed" |
| KB description/synonyms | "Constructed using LLM-assisted generation with manual curation" |
| Coverage mapping | "Extracted from official booklet using LLM, with manual verification" |

### 不提 AI 辅助的（代码/设计层）
- Chatbot 代码、ML pipeline、Gradio UI、CSS
- 设��决策只讲 what + why，不提决策过程中的 AI 辅助

---

## 10. 数据生成与使用（需要改进）

### 当前状态
- **KB (knowledge_base.json)**：129 个类别，每个有 category/description/synonyms/keywords/benefit_group/confusable_group/disambiguation_attributes
- **Seed sentences (seed_sentences_all.csv)**：V1(723 条 normal) + V2(890 条 10 种风格)，共 1613 条
- **Augmented (train_augmented.csv)**：nlpaug 增强到 6237 条（删词/换序/加填充词）
- **Train/Test split**：80/20，stratified

### 生成方式（AI 生成 + 人工审核）
- **KB description/synonyms/keywords**：LLM 生成 + 人工审核
- **Seed V1**：LLM 正常风格生成
- **Seed V2**：LLM 10 种 persona 风格（confused_student / terse / esl_speaker / brand_specific 等）
- **Augmentation**：nlpaug 代码自动化（删词/换序/加填充词），不涉及 LLM
- **Coverage mapping (RAG 数据)**：AI 从 booklet PDF 提取覆盖条款 → ���工逐条校验对照原文（提取 prompt 见 `prompt_for_claude_web-Generate Coverage Mapping.md`）
- **测试用例**：AI 辅助生成 75 个 test case + 人工审核预期结果
- **总体原则**：AI 用于数据生成和提取，人工负责审核和校验

### 需要改进的地方
1. **训练集和测试集同源**——都是 LLM 生成的，风格类似，导致 SVM/LR/NB 数字虚高。**需要独立生成测试集**（不同来源、不同风格、不同 LLM/prompt）
2. **药品品牌名缺失**——KB 的 Drug 条目没有 tylenol/advil 等常见药名。**需要整理 50-100 个品牌名加到 NER patterns + KB synonyms**（可参考 Health Canada DPD 或 Top 200 Dispensed Drugs in Canada）
3. **Seed 数量不均**——confusable 类别 ~18 条/类，standalone ~9 条/类，augment 后差距更大
4. **缺少真实用户数据**——所有 seed 都是合成的，没有真实 claim 经历

### 各模块后续要做的

**数据与特征（Cell 0-14）**：独立生成测试集（不同来源/风格）、整理药品品牌名→NER、审核 KB synonyms

**推荐与评估（Cell 15-27）**：Evaluation 加 confusion matrix 可视化、Error Analysis 加 sentence length vs accuracy 分析、Clustering 加 t-SNE 可视化、准备 report 叙事（为什么选 cosine emb 不选 SVM、silhouette 0.12 的解释）

**对话与展示（Cell 28-35）**：跑 test_cases.md 测试、修交互 bug（见 dev_status.md）、Clarification rules 审核、Coverage 文案优化

- 方法参考 `method_log.md` 的表述策略

---

## 11. 测试方式（需要改进）

详细测试文档见：
- `test_cases.md` — 75 个手动测试用例
- `dev_status.md` — bug 清单 + 修复记录
- `dialogue_framework.md` — 对话规范（改 bug 时参考）
- `_internal/test_dialogue.py` — mock 自动化测试（65 tests，1 秒）
- `_internal/test_deep.py` — 多轮对话场景测试（mock）

### 当前状态
- Mock 自动测试 65/65 pass（对话逻辑层面）
- Intent routing 96.6%（30 个 test query）
- 手动测试只做了 ~15 个，剩余 ~60 个待完成
- 已发现 10 个问题（T1-T10），T1-T6/T8-T10 已修，T7（药品品牌名）待做

### 需要改进
1. 手动测试覆盖不足 — 三人分工跑完 75 个 case
2. 药品品牌名识别 — 整理常见药名加到 NER（见 T7）
3. Coverage 准确性未系统验证 — RAG 输出是否跟 booklet 一致

### 测试迭代方法
改 5 个 → 跑 mock（1 秒）→ 跑 2-5 个场景多轮对话逐轮分析 → 记录新问题 → Run All 验证 → 下一轮
