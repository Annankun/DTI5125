# 开发状态（4/5 晚更新）

> 跟踪当前开发进度、已知 bug、下一步计划。
> 每次改完代码更新这个文件。

---

## 一、Notebook 结构（36 cells）

| Cell | Section | 内容 |
|------|---------|------|
| 0 | 标题 | 项目标题 + TOC |
| 1 | 1. Problem | markdown |
| 2-3 | 依赖+导入 | pip install（注释掉）+ imports |
| 4-9 | 2. Data Prep | KB 加载 + seed + augmentation + split |
| 10-12 | 3. Feature Eng | TF-IDF + Sentence Transformer |
| 13-15 | 4. Clustering | silhouette search + final clustering |
| 16-19 | 5. Recommender | cosine(emb/tfidf) + LR/SVM/NB + P@K 对比 |
| 20-21 | 6. Clarification | markdown + rules config |
| 22-23 | 7. Evaluation | markdown + single→multi-turn 图 |
| 24-25 | 8. Error Analysis | markdown + per-group/confusion pairs/explainability |
| 26 | 9. Chatbot Demo | markdown |
| 27-28 | 9.1-9.2 | NER + RAG (get_coverage_info) |
| 29-30 | 9.3 Intent | markdown + intent routing (embedding similarity) |
| 31 | 9.3.1 | Intent routing validation (30 test cases) |
| 32 | 9.4 Response | KB 查询 + 6 CQ handler + chatbot_respond() |
| 33 | 9.5 Gradio UI | callbacks + CSS + gr.Blocks + launch |

---

## 二、已完成

### 框架（4/4-4/5）
- [x] Knowledge Base 129 entries + benefit_group
- [x] Seed V1+V2 (1613 条) + augmentation (6237 条)
- [x] TF-IDF + Sentence Transformer FE
- [x] K-Means clustering + silhouette
- [x] 4 种推荐方法 + P@K 对比
- [x] Clarification rules (9 组)
- [x] NER EntityRuler patterns
- [x] Intent routing (embedding similarity, 6 CQ)
- [x] 6 个 CQ handler + chatbot_respond()
- [x] Gradio UI (Blocks, 双屏, Gemini 风格)
- [x] Coverage mapping (coverage_by_group.json)

### Bug 修复（4/5 晚）
- [x] **P1** RAG 截断 — 去掉 get_coverage_info() 里的 [:150] [:120] (Cell 28)
- [x] **P3** Follow-up 引导 — CQ2-CQ6 每个 handler 末尾加引导语 (Cell 31)
- [x] **P9** Clarifying 误重置 — clarifying 状态下不再跑 intent detection (Cell 31)
- [x] **B2** 删除 legacy cell (原 Cell 32)
- [x] Cell 32 从 `%run chatbot_ui.py` 替换为实际 UI 代码

---

## 三、自动化测试发现的问题（4/5 晚第二轮）

### T1. `$50 per visit/visit` 格式重复
- **位置**：Cell 30 get_coverage_info
- **原因**：per_visit_limit 值本身带 "per visit"，代码又拼了 "/visit"
- **严重性**：小

### T2. Follow-up 文案 "Is this the right category?"
- **位置**：Cell 34 所有 follow-up
- **问题**：用户不是专家，判断不了 category 对不对
- **改为**："Any questions about this category? Or describe your item in more detail."
- **严重性**：中

### T3. Coverage conditions 还是太长
- **位置**：Cell 30 get_coverage_info
- **现象**："Reimbursement for the services of practitioners included, when the practitioner..." 整段出现
- **原因**：first_sentence 截取不够——那段话的第一个 "." 在很后面
- **改为**：只取关键要求，如 "Requires: Licensed practitioner"
- **严重性**：中

### T4. "yes" 重复展示已看过的 coverage
- **位置**：Cell 34 yes handler
- **现象**：Turn 1 已经显示了 coverage，Turn 2 说 "yes" 又完整显示一遍
- **改为**："yes" 应该确认结束，不是重复展示。回复 "Got it! Would you like to claim something else?"
- **严重性**：中

### T5. `[NOT EXPLICITLY IN BOOKLET — FLAG]` 暴露给用户
- **位置**：Cell 30 get_coverage_info
- **现象**：某些 group 没有 booklet 条目，FLAG 标记直接出现在 chat 里
- **改为**：检测 FLAG 字符串，替换成 "Check your plan booklet for details"
- **严重性**：高

### T6. drug/prescription 关键词不触发 Drug 类别优先
- **位置**：Cell 34 respond_cq1 或 chatbot_respond
- **现象**："cold drug prescribed" 推荐 Cold Therapy 而不是 Drug
- **原因**：cosine similarity 匹配 "cold" 到 Cold Therapy，忽略了 "drug"/"prescribed"
- **改为**：NER 加 DRUG_KEYWORD pattern，CQ1 handler 检查——如果有 drug/prescription/medicine 关键词且 top-1 不是 Drug 类别，强制考虑 Drug
- **严重性**：高

### T7. 药品品牌名（tylenol、advil 等）无法识别
- **位置**：NER patterns (Cell 29) + KB synonyms
- **现象**：用户输入药品名，embedding 不认识，推荐到无关类别
- **改为**：NER 加常见药品品牌名 pattern，或在 KB 的 Drug 条目 synonyms 里加入
- **需要**：常见药品名列表（见药品知识库方案）
- **严重性**：高

### T7b. 药品知识库方案（待定）
- **方案 B**：Health Canada DPD (Drug Product Database)
  - API: `https://health-products.canada.ca/api/drug/`
  - 按 brandname 搜索：`/drugproduct/?brandname=tylenol`
  - 包含：品牌名、通用名、DIN、OTC/处方
  - 问题：API 返回量太大，需要筛选
  - 替代方案：
    - 手动整理 50-100 个常见药名（方案 A）
    - IQVIA Top 200 Dispensed Drugs in Canada 列表
    - RxNorm (NIH/NLM) — 美国药品标准数据库，有 REST API，品牌名/通用名映射
    - OpenFDA Drug API — `api.fda.gov/drug/`，可按品牌名搜索
    - DrugBank Open Data — 学术用途免费，有品牌名+通用名+分类
    - WHO ATC Classification — 按治疗类别分类的药品列表
  - 选择标准：能快速提取品牌名列表，不需要完整数据库
  - Report 价值：可以写 "NER enriched with brand names from Health Canada DPD"
- **注意**：识别到药品后不能直接说"能报"，要告知条件（需处方、需 DIN、Cannabis 不覆盖）

### T8. "no" 后 top-3 出现 Medical Cannabis
- **位置**：Cell 34 no handler
- **现象**：用户说 "prescribed drug"，no 后 top-3 包含 Medical Cannabis
- **改为**：Medical Cannabis 标记为 NOT COVERED，从推荐结果中过滤掉，或排到最后
- **严重性**：中

---

## 四、未修 Bug（交互逻辑，原 P2/P4/P5/P6）

### P6. Compression Stockings 状态机断裂（最严重）
- **现象**：clarification 走到 length 步后卡住
- **原因**：
  - length 选 "knee" → 映射到 `"next_question_knee"`，但 handle_clarification() 只检查 `startswith("next_question")` 后直接跳到下一个 question
  - pressure 的 options key 是 `"15-19_knee"` `"20-29_thigh"` 这种复合 key，用户不可能输入匹配
  - length 选择没有传递给 pressure 步，导致无法区分 knee vs thigh 的压力选项
- **修复方向**：handle_clarification() 需要根据 clarify_context 已收集的属性动态过滤当前步的 options；或者把 rules 结构改成树形而非线性列表
- **影响**：Compression Stockings 的完整 clarification flow 不可用

### P2. Clarification 选项格式差
- **现象**：显示 `Options: off-the-shelf / custom`，没编号没引导
- **修复**：所有输出 options 的地方改成 `1. xxx\n2. xxx` + "Reply with 1 or 2."
- **影响**：所有 clarification 交互

### P4. 不认识数字选择
- **现象**：用户回复 "1" "2"，chatbot 不理解
- **修复**：state 加 `last_list` 字段，chatbot_respond 开头检查数字输入 → 映射到列表项
- **影响**：CQ4 列表、CQ1 top-3 列表、clarification 编号选项
- **依赖**：P2 先改好格式才有编号可选

### P5. 无上下文记忆
- **现象**：同一窗口多轮，不记得之前内容
- **修复（简单版）**：state 加 `context`，记住上一轮推荐/查询结果，支持 "yes"/"that one"/数字回指
- **注意**：完整上下文理解需要 LLM，只做规则版

---

## 四、Notebook 内容待补

| # | 事项 | 状态 |
|---|------|------|
| B1 | EDA section（3 张图：benefit group 分布、confusable groups、query length） | ✅ Cell 7 |
| B3 | Intent routing 验证（30 test cases，96.6%） | ✅ Cell 33 |
| B4 | plan_type 过滤（CQ6 按 GSA/Studentcare 显示不同 coverage） | 低优先，暂不做 |

---

## 五、提交物

| 事项 | 状态 | DDL |
|------|------|-----|
| Report | ❌ 未开始 | 4/9 |
| PPT | ❌ 未开始 | 4/9 |
| README（给 TA 的运行说明） | ❌ 未开始 | 4/9 |

---

## 六、修复计划（迭代式）

### 已完成
- P1 RAG 截断 ✅
- P3 Follow-up 引导 ✅（但文案需要再改，见 T2）
- P9 Clarifying 跳过 intent detection ✅
- P6 Compression Stockings 树形状态机 ✅
- P2 编号格式 ✅
- P4 数字选择 ✅
- P5 上下文记忆（简单版 yes/no） ✅
- B1 EDA ✅
- B3 Intent routing 验证 ✅

### 第一轮迭代（当前）：T1-T5 输出格式
| # | 问题 | 改哪 |
|---|------|------|
| T5 | FLAG 暴露给用户 | Cell 30 |
| T2 | Follow-up 文案 | Cell 34 |
| T4 | yes 重复展示 coverage | Cell 34 |
| T1 | per visit/visit 重复 | Cell 30 |
| T3 | Conditions 太长 | Cell 30 |

### 第二轮迭代（已完成）：T6-T8
- [x] T6 drug/prescription 关键词规则（已加，pharmacy 已移除）
- [ ] T7 药品品牌名识别（待队友整理列表）
- [x] T8 Medical Cannabis 过滤

### 第三轮迭代：T9-T10（已修）
- [x] T9 "no" 回到上一层列表（用 prev_list 保存）
- [x] T10 有 last_list 时 "yes" 引导选数字

### 待队友做
- [ ] T7 药品品牌名识别（整理列表 + 加到 NER）
- [ ] dialogue_framework.md 8.1 clarification 结束重新跑模型
- [ ] dialogue_framework.md 8.2 profile 跨轮累积
- [ ] dialogue_framework.md 8.3 轮次限制

---

## 七、UI 前端同步流程

主 notebook Run All 要 5 分钟。改 CSS/布局用独立 `chatbot_ui_dev.ipynb`（mock 数据，只依赖 gradio）。

**同步步骤：**
1. 在 dev notebook 改好 UI
2. 从 dev notebook 复制 `session_state = {"state": make_initial_state()}` 到 `demo.launch(share=False)` 全部代码
3. 粘贴到主 notebook Cell 32，保留开头：
   ```python
   # 9.5 Gradio Chatbot Interface
   import gradio as gr
   ```
4. 不要复制 mock 函数
