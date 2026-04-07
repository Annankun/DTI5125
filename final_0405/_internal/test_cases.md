# Chatbot 测试用例（75 个）

> 手动测试 chatbot 回答质量用。每个用例 New Chat → 输入 → 截图 → 评价。
> 截图存到 `_internal/test_screenshots/` 文件夹
> 文件命名：`01.png`, `01-1.png`, `01-2.png` ...（同一用例的变体测试）
> 每个测试：New Chat → 输入 → 截图结果 → 填写评价
> 评价标记：✅ 正确 / ⚠️ 部分对 / ❌ 错误 / 💡 建议

---

## Welcome 页面 Example 按钮

| # | 按钮文字 | 期望 | 截图 | 评价 |
|---|---------|------|------|------|
| e1 | Compression socks — what category? | → Compression Stockings clarification | e1.png | 这么多选项也没让我选，给我序号让我选 或者问题你是哪种？ |
| e2 | What's under vision? | → 列出 vision 类别 | e2.png | 之前说过，没有followup引导你要报销什么或者我我能做什么for你的报销？ |
| e3 | Diabetes — what's covered? | → Diabetes 相关类别列表 | e3.png |显示数字，但是我输入数字不管用，变成模糊词了。要接着刚刚的对话，知道我说1,，,3,4是什么  |
| e4 | Custom vs non-custom brace? | → Brace 区别对比 | e4.png |同e2，无引导。而且回复了又回去了，不能读聊天的上下问吗？每次对话应该都建立上下文，同一个窗口在多少句内都是有记忆的，personalized的 |
| e5 | CPAP mask vs supplies? | → CPAP 组件区别 | e5.png |同上，不能识别数字在上下文的含义 |
| e6 | Is massage therapy covered? | → Yes + coverage info | e6.png | rag显示不全 |

---

## CQ1 推荐（描述购买/服务）

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 01 | I bought prescription glasses | glasses / new glasses / need glasses | → Prescription Glasses | 01.png | 关于推荐内容的介绍要讲清楚是介绍，rag部分提示不清。 |
| 02 | I had a physiotherapy session | physio / physio session / saw physio | → Physiotherapy | 02.png |显示不全，有点点点结尾。 |
| 03 | I need to claim my knee brace | knee brace / brace knee / got a brace | → Brace (可能触发 clarification) | 03.png | followup问题不清楚？要标识好。option也不清楚，能不能直接用1,2指代。 rag部分显示不全 |
| 04 | I bought a walker for my grandmother | walker / need walker / bought walker | → Walker (可能问 wheeled/non-wheeled) | 04.png | |
| 05 | I got a dental cleaning last week | clean dental / teeth cleaning / dental clean | → Dental Services | 05.png | |
| 06 | I need to claim crutches | crutches / bought crutches / need crutch | → Crutches (可能问 underarm/forearm) | 06.png | |
| 07 | I bought a blood pressure monitor | blood pressure / bp monitor / pressure machine | → Blood pressure monitor | 07.png | |
| 08 | I had an MRI scan | mri / need mri / got mri done | → MRI | 08.png | |
| 09 | I saw a psychologist yesterday | psychologist / saw psychologist / psychology session | → Psychologist | 09.png | |
| 10 | I purchased a CPAP machine | cpap / cpap machine / sleep machine | → CPAP Machine (可能问 machine/mask/supplies) | 10.png | |

## CQ2 浏览

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 11 | What can I claim under dental? | dental options / what dental / show dental | → 列出 dental 类别 | 11.png | |
| 12 | What hearing services are available? | hearing services available? / what hearing / hearing options | → 列出 hearing 类别 | 12.png | |

## CQ3 区别

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 13 | What's the difference between custom and non-custom orthotics? | custom vs regular orthotics / orthotics difference | → 列出 foot care 区别 | 13.png | |

## CQ4 疾病

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 14 | I have sleep apnea, what's covered? | sleep apnea / apnea covered? / sleep apnea claim | → CPAP 相关类别 | 14.png | |

## CQ6 覆盖

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 15 | Is acupuncture covered? | acupuncture covered? / can claim acupuncture? | → Yes + coverage info | 15.png | |
| 16 | Can I claim a cervical pillow? | cervical pillow / neck pillow claim | → 可能 not explicitly covered | 16.png | |

## 边界 — prescribed drug 问题

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 17 | prescribed drug | prescription / my prescription / drug claim | → Drug (不应该出 Medical Cannabis) | 17.png | |

## 边界 — 无关/模糊输入

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 18 | hello | hi / hey / yo | → 友好回复 + 引导 | 18.png | |
| 19 | compression socks 20mmhg knee length | socks 20mmhg knee / compression knee 20 | → 具体 compression stocking 类别 | 19.png | |
| 20 | I need help | help / help me / what can you do | → 引导用户描述 | 20.png | |

## 简短/口语

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 21 | glasses | glass / my glasses / eye glasses | → Prescription Glasses | 21.png | |
| 22 | massage | got massage / massage claim | → Massage | 22.png | |
| 23 | dental | teeth / my teeth / dental stuff | → Dental Services 或 CQ2 浏览 | 23.png | |
| 24 | insulin | insulin claim / need insulin / my insulin | → Insulin 相关 (可能问哪种) | 24.png | |
| 25 | braces | brace / my brace / leg brace | → Brace (可能 clarification) | 25.png | |
| 26 | wheelchair | need wheelchair / wheelchair claim | → Transport Wheelchair | 26.png | |
| 27 | hearing aid | hearing aids / ear aid / hearing device | → Hearing Aids | 27.png | |
| 28 | eye exam | eye test / vision test / eye check | → Eye Exam | 28.png | |

## 缩写/简称

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 29 | physio | physiotherapy / PT session | → Physiotherapy | 29.png | |
| 30 | chiro | chiropractor / chiropractic / back crack | → Chiropractic | 30.png | |
| 31 | cpap | cpap machine / sleep apnea machine | → CPAP (可能问 machine/mask/supplies) | 31.png | |
| 32 | xray | x-ray / x ray / got xray | → X-Ray | 32.png | |
| 33 | mri | MRI scan / brain scan | → MRI | 33.png | |

## 口语化描述

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 34 | my back hurts | back pain / back problem | → 引导：描述你买了什么或做了什么治疗 | 34.png | |
| 35 | broke my leg | leg broken / fractured leg | → 可能推荐 crutches/brace/cast | 35.png | |
| 36 | need new glasses | want glasses / glasses broken | → Prescription Glasses | 36.png | |
| 37 | socks for swelling | swollen legs socks / leg swelling | → Compression Stockings | 37.png | |
| 38 | knee thing from pharmacy | bought knee thing / pharmacy knee support | → Brace (Non-custom) | 38.png | |
| 39 | the machine for sleeping | sleep breathing machine / breathing machine night | → CPAP Machine | 39.png | |
| 40 | blood sugar test strips | sugar strips / glucose strips / diabetes strips | → Glucose Monitoring Supplies/Sensors | 40.png | |

## ESL/口语

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 41 | I buy medicine | buy drug / bought medicine | → Drug | 41.png | |
| 42 | how to claim teeth | teeth claim how / claim for teeth | → Dental Services | 42.png | |
| 43 | want check eye | check eye / eye check want | → Eye Exam | 43.png | |
| 44 | massage money back | massage refund / get money massage | → Massage + coverage info | 44.png | |

## 完全模糊

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 45 | help | help me | → 引导 | 45.png | |
| 46 | claim | make claim / submit claim | → 引导 | 46.png | |
| 47 | what do I do | what now / now what | → 引导 | 47.png | |
| 48 | hi | hey / hello there | → 友好回复 + 引导 | 48.png | |
| 49 | ? | ?? / ... | → 引导 | 49.png | |
| 50 | how does this work | how to use / what is this | → 说明 chatbot 功能 | 50.png | |

## 药品/产品名

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 51 | tylenol | tylenol claim / bought tylenol | → Drug | 51.png | |
| 52 | advil | advil receipt / claim advil | → Drug | 52.png | |
| 53 | ibuprofen | ibuprofen 400mg | → Drug | 53.png | |
| 54 | amoxicillin | antibiotics / antibiotic prescription | → Drug | 54.png | |
| 55 | birth control pills | the pill / contraceptive / birth control | → Drug (contraceptives) | 55.png | |
| 56 | epipen | epi pen / epinephrine | → Drug | 56.png | |
| 57 | ventolin inhaler | inhaler / puffer / asthma inhaler | → Drug 或 Aerochamber | 57.png | |
| 58 | melatonin | melatonin supplement | → 可能 not covered (non-prescription) | 58.png | |
| 59 | vitamin D | vitamin d pills / vitamins | → 可能 not covered | 59.png | |
| 60 | ozempic | semaglutide / weight loss injection | → Drug | 60.png | |

## 具体设备/品牌

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 61 | freestyle libre | libre sensor / cgm sensor | → Glucose Monitoring System | 61.png | |
| 62 | dexcom | dexcom g7 / dexcom sensor | → Glucose Monitoring System | 62.png | |
| 63 | resmed | resmed cpap / resmed machine | → CPAP | 63.png | |
| 64 | dr scholls insoles | shoe insoles / insoles pharmacy | → Standard foot orthotics | 64.png | |
| 65 | tens machine | tens unit / muscle stimulator / tens | → Stimulator, TENS | 65.png | |

## 具体治疗

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 66 | root canal | root canal done / had root canal | → Dental (Endodontic) | 66.png | |
| 67 | wisdom teeth | wisdom tooth out / wisdom extraction | → Dental (extraction) | 67.png | |
| 68 | filling | tooth filling / got filling / cavity filled | → Dental (restorative) | 68.png | |
| 69 | colonoscopy | had colonoscopy / colonoscopy done | → Colonoscopy | 69.png | |
| 70 | allergy test | allergy testing / tested for allergies / allergy check | → Blood/Scratch test for Allergies | 70.png | |

## 学生常见

| # | 输入 | 变体 | 期望 | 截图 | 评价 |
|---|------|------|------|------|------|
| 71 | gym injury | hurt at gym / sports injury / injured playing | → 引导：具体买了什么/看了什么医生 | 71.png | |
| 72 | anxiety medication | anxiety pills / anti anxiety / anxiety meds | → Drug | 72.png | |
| 73 | therapist | see therapist / need therapist / therapy | → 可能问哪种 therapist | 73.png | |
| 74 | counselling | counseling / saw counsellor / counselor session | → Clinical Counsellor | 74.png | |
| 75 | flu shot | flu vaccine / got flu shot / influenza vaccine | → Drug (vaccines) | 75.png | |
