# 项目参考资料

> 按模块分类的参考项目、教程、数据集。写 report 引用和方法选择依据用。
> 2026-04-04

---

## 一、直接相关的 GitHub 项目

| # | 项目 | 对我们的用处 |
|---|------|-------------|
| 1 | [Insurance Claim NLP](https://github.com/siddharthsky/insurance_claim_NL-p) | 最接近——保险 claim 文本分类 pipeline |
| 2 | [TF-IDF 209 类分类](https://github.com/sid-thiru/Text-Classification-with-TFIDF-and-sklearn) | 跟 129 类场景几乎一样的 sklearn pipeline |
| 3 | [Content-Based Recommender](https://github.com/nikitaa30/Content-based-Recommender-System) | TF-IDF + cosine similarity 推荐实现 |
| 4 | [Cosine Similarity + sentence-transformers](https://github.com/ev2900/Cosine_Similarity_Search_Example) | embedding + cosine sim 的简洁实现 |
| 5 | [ClarifyingQA](https://github.com/krasheninnikov/clarifyingqa) | 追问逻辑参考 |
| 6 | [TF-IDF Chatbot](https://github.com/miteshksingh/tfidf-chatbot) | TF-IDF 检索式 chatbot + fallback 阈值 |
| 7 | [Multi-Topic Chatbot](https://github.com/MarcLinderGit/multi_chatbot) | 多轮对话状态管理参考 |

## 二、CLINC150 相关

| # | 资源 | 用处 |
|---|------|------|
| 1 | [CLINC150 sklearn 分类](https://github.com/shriadke/Intent_Classification_using_CLINC150_Dataset) | 150 类 intent 分类，4 种 sklearn 算法对比 |
| 2 | [CLINC150 官方数据集](https://github.com/clinc/oos-eval) | 150 intent + OOS 样本，sanity check 用 |
| 3 | [Few-Shot Intent Detection](https://github.com/jianguoz/Few-Shot-Intent-Detection) | CLINC150 domain splits，in-domain OOS 概念 |

## 三、Kaggle Notebooks

| # | 资源 | 用处 |
|---|------|------|
| 1 | [Multi-Class Text Classification TFIDF](https://www.kaggle.com/code/selener/multi-class-text-classification-tfidf) | Consumer Complaints 多类分类，结构类似保险 claim |
| 2 | [Content-Based TF-IDF Recommendation](https://www.kaggle.com/code/ramzanzdemir/recommendation-systems-content-based-tf-idf) | content-based 推荐 notebook |

## 四、教程 & 文档

| # | 资源 | 用处 |
|---|------|------|
| 1 | [Multi-Class Text Classification (Susan Li)](https://medium.com/data-science/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f) | TF-IDF + LR/SVM/NB 对比的经典教程 |
| 2 | [spaCy EntityRuler 教程](https://ner.pythonhumanities.com/02_01_spaCy_Entity_Ruler.html) | 规则式 NER 实现参考 |
| 3 | [spaCy Rule-Based Matching 官方文档](https://spacy.io/usage/rule-based-matching) | Matcher/PhraseMatcher/EntityRuler |
| 4 | [Gradio ChatInterface 官方 demo](https://github.com/gradio-app/gradio/blob/main/demo/chatbot_multimodal/run.ipynb) | 多轮 chatbot UI |

## 五、第二轮搜索新发现

### 最有价值的新资源

| # | 项目 | 为什么有用 |
|---|------|-----------|
| 1 | [sklearn-hierarchical-classification](https://github.com/globality-corp/sklearn-hierarchical-classification) | sklearn 兼容的层级分类器，直接支持 coarse-to-fine pipeline |
| 2 | [Kaggle: Recommender Systems in Python 101](https://www.kaggle.com/code/gspmoreira/recommender-systems-in-python-101) | 完整的 TF-IDF + cosine sim content-based 推荐 notebook |
| 3 | [CRSLab](https://github.com/RUCAIBox/CRSLab) | Conversational Recommender System 工具包，架构参考 |
| 4 | [Gradio 多轮 chatbot 官方指南](https://www.gradio.app/guides/conversational-chatbot) | `gr.ChatInterface` 多轮对话 + state 管理 |
| 5 | [Gradio State in Blocks](https://www.gradio.app/guides/state-in-blocks) | `gr.State` 跨轮次持久化数据（user profile / 对话历史） |
| 6 | [Claim Description Classification (190K records)](https://github.com/Mahesh3394/Claim-Description-Classification) | 大规模 claim 分类 + class imbalance 处理 |
| 7 | [Content-Based Filtering TF-IDF](https://github.com/Valdecy/Recommender-Systems-Content_Based_Filtering) | TF-IDF + cosine sim content-based filtering 干净实现 |
| 8 | [medspaCy](https://medium.com/geekculture/introduction-to-the-medspacy-the-medical-named-entity-recognition-ner-package-e7c6f0f06496) | 医疗 NER 包，基于 spaCy，可参考 pattern |
| 9 | [ai-chatbot-framework](https://github.com/alfredfrancis/ai-chatbot-framework) | Python chatbot 框架，NLU + 多轮 context 管理 |
| 10 | [GreenShield+ Help Centre](https://greenshieldplus.zendesk.com/hc/en-ca/categories/25812899418260-Insurance-and-Benefits) | GreenShield 官方 FAQ 分类，可作为 seed 数据来源 |
| 11 | [Hands-On Recommendation Systems (书)](https://github.com/PacktPublishing/Hands-On-Recommendation-Systems-with-Python) | content-based / knowledge-based / hybrid 全覆盖 |

---

## 六、按项目模块的参考映射

| 模块 | 参考 |
|------|------|
| TF-IDF + LR/SVM/NB | CLINC150 sklearn, Susan Li 教程, Kaggle TFIDF |
| Content-Based 推荐 | Content-Based Recommender, Kaggle CB-TFIDF |
| Chatbot + 对话管理 | TF-IDF Chatbot, Multi-Topic Chatbot, Gradio demo |
| spaCy NER | EntityRuler 教程, spaCy 官方文档, medspaCy |
| OOS detection | CLINC150 官方, Few-Shot Intent Detection |
| Clarification | ClarifyingQA, aitrek/intent_classifier |
| Coarse-to-fine | sklearn-hierarchical-classification |
| 保险领域 | insurance_claim_NL-p, Claim Description Classification, GreenShield Help Centre |
| CRS 架构 | CRSLab, Hands-On RS 书 |
| Gradio 状态管理 | Gradio 多轮指南, Gradio State in Blocks |
