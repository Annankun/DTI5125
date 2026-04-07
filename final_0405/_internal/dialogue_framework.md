# 对话框架规范（4/5 定稿）

> Chatbot 交互的完整定义。改代码和写 report 都参考这个文件。

---

## 一、对话状态

| 状态 | 含义 | state 字段 |
|------|------|-----------|
| `idle` | 等待用户输入 | `stage: "idle"` |
| `clarifying` | 追问中，等用户回答选项 | `stage: "clarifying"`, `clarify_group`, `clarify_step`, `clarify_context` |

- **不单独设 `showing_list` 状态。** 所有编号列表（clarification 选项、CQ4 列表、CQ1 top-3）统一用 `last_list` 存映射。
- `chatbot_respond` 开头统一检查：如果 `last_list` 存在且用户输入是数字 → 映射到对应项 → 清空 `last_list`。
- `last_list` 是独立于 `stage` 的字段，clarifying 和 idle 状态下都可以有。

```python
state = {
    "stage": "idle",           # "idle" | "clarifying"
    "clarify_group": None,
    "clarify_step": 0,
    "clarify_context": {},
    "plan_type": None,
    "last_list": {},           # {"1": "category_name", "2": "category_name", ...}
    "context": {               # 简单上下文记忆
        "last_query": "",
        "last_result": "",
        "last_intent": "",
    }
}
```

---

## 二、状态转移

```
idle → (用户输入) → boundary check → intent routing → CQ handler
  CQ1 高分直接推荐 → idle (存 context)
  CQ1 多个候选 → idle + last_list (top-3 编号)
  CQ1 confusable → clarifying + last_list (选项编号)
  CQ2-CQ6 → idle + last_list (如果有列表)

clarifying → (用户输入数字) → 查 last_list → 下一步/最终结果
clarifying → (用户输入长文本 >60 字符) → 重置为 idle → 重新 routing
clarifying → (用户输入短关键词) → handle_clarification 匹配

idle + last_list → (用户输入数字) → 查 last_list → 展示 coverage 详情
idle + last_list → (用户输入非数字) → 清空 last_list → 当作新查询

any → (用户输入 hi/help/空) → fallback 引导
any → (用户输入 "no"/"wrong") → 展示 top-3
any → (用户输入 "yes"/"that one") → 对 context.last_result 展示 coverage
```

---

## 三、回复格式模板

### 推荐结果（CQ1 高分直接推荐）
```
Based on your description, I recommend:

**Compression Stockings, knee length (20-29 mmhg)**
Relevance: 53.1%

Coverage: Co-pay 50% | Limit $500/yr
Note: Pressure >= 15 mmHg required. See plan booklet for full conditions.

Is this the right category? Or describe your item in more detail.
```

### 编号列表（CQ4 疾病、CQ1 多个候选）
```
For diabetes, here are the relevant categories:

1. Blood glucose meter (94%)
2. Glucose Monitoring Supplies/Sensors (91%)
3. Glucose Monitoring Transmitter (88%)
4. Insulin Pump (79%)

Reply with a number to see details, or describe your item.
```

### Clarification 追问
```
I found several similar categories. Let me help narrow it down.

Is your brace custom-made or off-the-shelf?
1. Off-the-shelf (store-bought)
2. Custom (prescribed by specialist)

Reply 1 or 2.
```

### Coverage 详情（CQ6 / 选数字后）
```
Yes, Massage is covered under your plan.

Coverage: Co-pay 0% | Limit $500/yr per practitioner | $50/visit
Requires: Licensed practitioner (RMT)
See plan booklet for full conditions.

Would you like to submit a claim? Describe your purchase.
```

### Follow-up 引导（每条回复末尾必须有）
| 场景 | 引导语 |
|------|--------|
| 直接推荐后 | "Any questions about this category? Or describe your item in more detail." |
| 编号列表后 | "Reply with a number to see details, or describe your item." |
| Clarification 选项后 | "Reply 1 or 2." / "Reply with a number." |
| Coverage 详情后 | "Would you like to claim something else? Describe your next item." |
| 浏览列表后 | "Which one would you like to claim? Or describe your item." |

### 特殊规则
- **不要问用户 "Is this right/correct?"**——用户不是专家，判断不了 category 对不对
- **drug/prescription/medicine 关键词**：如果用户输入包含这些词但 top-1 不是 Drug/Prescription 类别，需要额外检查（NER 或关键词规则）

---

## 四、数字选择机制

```python
# chatbot_respond 开头（在 boundary check 之后、intent routing 之前）
if state.get("last_list") and user_input.strip() in state["last_list"]:
    selected_category = state["last_list"][user_input.strip()]
    state["last_list"] = {}
    
    if state["stage"] == "clarifying":
        # 交给 handle_clarification 处理（可能是中间步骤）
        return handle_clarification(user_input, state)
    else:
        # 直接展示 coverage 详情
        coverage = get_coverage_info(selected_category)
        state["context"]["last_result"] = selected_category
        return format_coverage_response(selected_category, coverage), state
```

每次展示编号列表时，必须同时更新 `state["last_list"]`：
```python
state["last_list"] = {"1": "Blood glucose meter", "2": "Glucose Monitoring Supplies/Sensors", ...}
```

---

## 五、Clarification 状态机

### 简单 group（8 个）：保持线性
现有的 questions 列表结构不变。handle_clarification 按 step 推进。

### Compression Stockings：树形
```python
"Compression Stockings": {
    "tree": {
        "question": "Is it footless (calf sleeves/tights) or regular stockings?",
        "options": {
            "Footless": {"result": "Compression Calf Sleeves/Tights (footless), any length"},
            "Regular": {
                "question": "Are they custom-made?",
                "options": {
                    "Yes": {"result": "Compression Stockings, custom, any length"},
                    "No": {
                        "question": "What length?",
                        "options": {
                            "Knee": {
                                "question": "What pressure level?",
                                "options": {
                                    "Up to 14 mmHg": {"result": "Compression Stockings, any length (up to 14 mmhg)"},
                                    "15-19 mmHg": {"result": "Compression Stockings, knee length (15-19 mmhg)"},
                                    "20-29 mmHg": {"result": "Compression Stockings, knee length (20-29 mmhg)"},
                                    "30+ mmHg": {"result": "Compression Stockings, knee length (30 mmhg & over)"}
                                }
                            },
                            "Thigh/Full": {
                                "question": "What pressure level?",
                                "options": {
                                    "Up to 14 mmHg": {"result": "Compression Stockings, any length (up to 14 mmhg)"},
                                    "15-19 mmHg": {"result": "Compression Stockings, thigh/full (15-19 mmhg)"},
                                    "20-29 mmHg": {"result": "Compression Stockings, thigh/full (20-29 mmhg)"},
                                    "30+ mmHg": {"result": "Compression Stockings, thigh/full (30 mmhg & over)"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
```

handle_clarification 逻辑：
- 如果 rules 有 `"tree"` 字段 → 走树形逻辑（用 `clarify_context` 记录当前节点路径）
- 否则 → 走现有线性逻辑

---

## 六、Coverage 精简格式

`get_coverage_info()` 输出改为精简版：

```
Coverage: Co-pay {X}% | Limit {Y}/yr
{一句 conditions 摘要}
See plan booklet for full conditions.
```

- co-pay + limit 一行
- conditions 只取第一句或关键要求（如 "Pressure >= 15 mmHg required"）
- 末尾统一加 "See plan booklet for full conditions."
- 如果有 per_visit_limit，加在 limit 后面

---

## 七、"no" / "yes" 处理

| 用户输入 | 条件 | 动作 |
|---------|------|------|
| "yes" / "that one" / "correct" | context.last_result 存在 | **不重复展示 coverage**（用户已经看过了）。回复 "Got it! Would you like to claim something else? Describe your next item." |
| "no" / "wrong" / "not this" | context.last_result 存在 | 展示 top-3（基于 context.last_query 重新推荐） |
| "yes" / "no" | context.last_result 为空 | 当作普通输入走 intent routing |

---

## 八、待实现的设计（交给模块 C）

### 8.1 Clarification 结束后重新跑模型
当前：clarification 结束直接用规则硬编码的 category 名。
改为：把原始输入 + 收集的属性拼成增强 query → 调 `recommend_cosine_emb()` → 用模型结果。规则结果做 fallback（模型对数字属性可能不准）。

```python
enhanced_query = original_input + " " + " ".join(collected_attributes.values())
model_result = recommend_cosine_emb(enhanced_query, top_n=1)[0][0]
rule_result = node["result"]
final = model_result if model_result == rule_result else rule_result
```

目的：推荐始终由模型决定，规则只负责提问。report 可写 "The model is the final decision-maker; clarification rules serve as an information-gathering mechanism."

### 8.2 Profile 跨轮累积（Personalization）
当前 context 只存上一轮。加 profile 字段累积整个对话的用户信息：

```python
"profile": {
    "conditions": [],        # NER 检测到的疾病
    "body_parts": [],        # 部位
    "plan_type": None,       # GSA / Studentcare
    "claimed_items": [],     # 已处理的类别
    "mentioned_groups": [],  # 提过的 benefit group
    "turn_count": 0,
}
```

每轮 NER 检测到实体 → 加到 profile（不覆盖）。推荐时 profile 里有 conditions → 给相关类别 boost。

### 8.3 轮次限制
设 20 轮上限。18 轮提醒，20 轮自动总结已处理的 items + 用户 conditions，提示开始新对话。

---

## 九、Coverage 显示规则

### FLAG 标记处理
coverage_by_group.json 里某些 group 有 `[NOT EXPLICITLY IN BOOKLET SCHEDULE -- FLAG]` 标记。**绝对不能暴露给用户。**

处理方式：如果 co_pay/limit/conditions 包含 `[NOT` 或 `FLAG`，替换为：
- co_pay: 显示 "Check your plan booklet"
- limit: 显示 "See plan booklet for details"
- conditions: 不显示

### per_visit 格式
避免 `$50 per visit/visit` 重复。如果 per_visit_limit 值本身包含 "per visit"，不再拼 "/visit"。

### Conditions 长度
只取关键要求，不超过一句话。如果 conditions 原文超过 80 字符，提取核心要求（如 "Requires licensed practitioner" / "Pressure >= 15 mmHg required"），不贴原文。

---

## 八、边界输入（已实现）

| 输入 | 回复 |
|------|------|
| 空 / 1 个字符 | "Hi! I can help you find the right GreenShield claim category..." |
| hi / hello / hey | "Hello! Tell me what you need to claim..." |
| help / what can you do | 功能列表（4 个 bullet） |
