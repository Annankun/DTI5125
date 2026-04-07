# GreenShield ClaimBot (DTI5125 / Group 27)

一个面向 **GreenShield 学生保险报销场景** 的智能问答与推荐系统：
- 帮助用户根据自然语言描述，推荐最可能的 claim category。
- 在类别易混淆时发起多轮澄清问题（clarification）。
- 提供来自 booklet 的 coverage 说明（RAG grounding）。

## 项目目标

本项目用于课程 DTI5125 的小组期末实践，核心目标是：
1. 将用户的医疗报销描述映射到正确的报销类别。
2. 在复杂/模糊表达下保持高召回与可解释性。
3. 提供可交互 chatbot 界面用于演示。

## 核心能力

- **推荐引擎（Content-Based）**
  - TF-IDF / Sentence-Transformer 向量化
  - Cosine similarity + LR/SVM/NB 对比
  - 线上主推：Embedding + Cosine（泛化更稳）
- **多意图路由（6 类 CQ）**
  - CQ1 推荐类别
  - CQ2 按 benefit group 浏览
  - CQ3 类别差异对比
  - CQ4 按疾病查询
  - CQ5 组件/子类区别
  - CQ6 coverage 查询
- **NER 实体提取**
  - 基于 spaCy EntityRuler 的规则抽取（medical item / condition / benefit group 等）
- **澄清对话（Clarification）**
  - 针对 confusable groups 的规则树追问
  - 支持数字选项、yes/no、回退重选
- **Coverage grounding**
  - 从保险 booklet 提取的文本映射到类别，输出可读 coverage 信息
- **前端界面**
  - Gradio 聊天界面

## 项目结构

```text
.
├── README.md
└── final_0405/
    ├── Group27_Final_ClaimBot.ipynb      # 主 notebook（训练 + chatbot）
    ├── requirements.txt                  # 依赖
    ├── data/
    │   ├── knowledge_base.json           # 129 个类别的结构化知识库
    │   ├── coverage_by_group.json        # coverage 映射
    │   ├── seed_sentences_all.csv        # 训练语料（含增强）
    │   └── source/                       # 原始文本/手册/PDF
    └── _internal/
        ├── test_dialogue.py              # 对话逻辑测试脚本
        ├── test_cases.md                 # 手工测试用例
        ├── project_overview.md           # 项目全览与设计说明
        └── dialogue_framework.md         # 对话规则与状态管理
```

## 运行方式

### 1) 安装依赖

```bash
cd final_0405
pip install -r requirements.txt
```

### 2) 启动 Notebook

```bash
jupyter notebook Group27_Final_ClaimBot.ipynb
```

在 notebook 中执行 **Run All**，将完成：
- 数据加载与特征准备
- 推荐方法对比与模型准备
- chatbot 组件初始化
- Gradio 界面启动

### 3) 快速测试（可选）

```bash
cd final_0405
python _internal/test_dialogue.py
```

## 数据与方法概览

- **知识库规模**：129 个 claim categories
- **训练语料**：seed + augmentation（用于模型对比评估）
- **主要评估指标**：Precision@1 / @3 / @5
- **澄清策略**：规则决策树（按 confusable group）

## 已知说明

- Notebook 结果依赖本地环境与模型下载状态（首次运行可能较慢）。
- SVM/LR/NB 在同源切分下分数较高，但线上流程采用更稳健的 embedding-cosine 方案。
- `_internal/` 文件夹主要用于开发与测试记录，不影响核心运行。

## 团队与课程信息

- 课程：DTI5125
- 小组：Group 27
- 项目：GreenShield ClaimBot

---

如果你是本项目协作者，建议先阅读：
1. `final_0405/_internal/project_overview.md`
2. `final_0405/_internal/dialogue_framework.md`
3. `final_0405/_internal/test_cases.md`
