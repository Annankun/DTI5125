# Prompt for Claude.ai Web — Generate Coverage Mapping

## 上传文件
1. `greenshied booklet.pdf`（位置：`A3_proposal/proposal/data/greenshied booklet.pdf`）
2. `benefit_groups_list.txt`（位置：`final/_internal/benefit_groups_list.txt`）

## 复制以下全部内容到 Claude.ai web

---

**Your role**: You are a health insurance benefits analyst who is meticulous about exact policy wording. You never paraphrase — you quote exact terms from the booklet. If a benefit is not explicitly listed, you flag it rather than assume.

I need you to create a coverage mapping for a GreenShield+ insurance chatbot. I'm uploading:

1. **The official GreenShield benefit booklet PDF** — this is the ONLY authoritative source. Read it carefully and thoroughly.
2. **A benefit_groups_list.txt** — this lists 20 benefit groups and their 129 claim categories.

## Your task

For each of the 20 benefit groups in the list, find the matching section in the booklet and extract the coverage details into a Python dictionary.

## Output format

```python
coverage_by_group = {
    "benefit_group_name": {
        "booklet_section": "Section number and name, e.g. '3g. Compression Stockings'",
        "co_pay": "exact percentage from booklet",
        "annual_limit": "exact dollar amount from booklet",
        "per_visit_limit": "if applicable, otherwise None",
        "conditions": "any special requirements",
        "not_covered": "any exclusions mentioned",
        "sub_groups": None,  # or a dict if different categories have different rates
    },
}
```

**Important format rules:**
- All values must be strings (use `"N/A"` instead of `None`)
- `sub_groups` keys should match the benefit_type names from the list file (e.g., `"Professional Services Group A"`, `"Professional Services Group B"`)
- Quote exact booklet wording for co-pay, limits, and conditions — do not paraphrase
- Keep "reasonable & customary" and similar insurance terms as-is

**Overall plan limit** (applies across all groups):
- Add a special entry `"_overall"` with the overall maximums from the booklet header

Also output a JSON version of the same dictionary so I can save it as a file.

## CRITICAL RULES

### 1. Accuracy — ONLY use the booklet
- Every number (co-pay %, dollar limit) must come directly from the booklet text.
- Do NOT guess, infer, or use general insurance knowledge.
- If the booklet does not mention a specific group, set fields to `"Not explicitly listed in booklet — needs manual verification"`.

### 2. If you're unsure about ANYTHING, ASK ME
- If a group doesn't clearly match a booklet section → ask me before mapping.
- If you're unsure whether a category falls under one section or another → ask me.
- If the booklet is ambiguous → show me the exact booklet text and ask for clarification.
- **Do NOT guess. Ask me. I would rather you ask 10 questions than make 1 wrong mapping.**

### 3. Groups that need special attention

**Professional Services (19 categories)** — the booklet has 3 sub-groups with DIFFERENT rates:
- Group A: $50/visit, $500/yr per practitioner
- Group B: $80/visit, $1,000/yr combined
- Group C: combined with Group B
- Allied Health practitioners (Acupuncture, Athletic Therapy, etc.) — check carefully which group they fall under. If the booklet doesn't specify, FLAG IT and ask me.

**Dental (5 categories)** — the booklet has multiple tiers:
- Basic: 0% co-pay
- Basic Restorative: 25%
- Endodontic: 70%
- Major: 70%
- Accidental Dental is a separate section (Section 8)

**Medical Items - Diabetic Supplies (10 categories)** — check BOTH:
- Section 3 (Medical Items and Services) — for devices/equipment
- Section 1 (Prescription Drugs) — booklet says "Includes insulin and diabetic supplies"
- These may overlap. Tell me what you find and I'll decide.

**Medical Items - Diagnostic Tests (16 categories)** — the booklet may not have a dedicated section. Check under Medical Items and Services. If not found, flag it.

**Professional Services - Foot Care (6 categories)** and **Professional Services - Hearing (5 categories)** — the booklet may not list these separately. Check if they fall under Professional Services Group A/B or somewhere else. If unclear, ask me.

**Medical Cannabis** — the booklet says this is NOT covered under Prescription Drugs. Make sure to note this.

**Compression Stockings** — must note the condition: pressure >= 15 mmHg required.

### 4. Verification

After you generate the dictionary, go through these checks:
- [ ] Every co-pay % matches the booklet word-for-word
- [ ] Every dollar limit matches the booklet word-for-word
- [ ] Professional Services has sub_groups with 3 different rate tiers
- [ ] Dental has sub_groups with correct tiers
- [ ] Medical Cannabis is marked NOT covered
- [ ] Compression Stockings has the 15 mmHg condition noted
- [ ] Any group NOT found in the booklet is clearly flagged
- [ ] No field was filled by guessing — everything traces to a specific booklet section

### 5. Output

Give me:
1. The Python dictionary `coverage_by_group`
2. A list of any groups/categories you're unsure about, with the specific question
3. A list of any booklet text that was ambiguous

Take your time. Read the booklet thoroughly. Accuracy is more important than speed.
