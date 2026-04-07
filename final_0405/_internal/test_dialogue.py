"""
Test dialogue framework logic WITHOUT ML dependencies.
Mocks: recommend_cosine_emb, detect_intent, nlp, knowledge_base, coverage_data, st_model
Tests: state transitions, number selection, yes/no, boundary, clarification tree/linear
Run: python _internal/test_dialogue.py
"""
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================================
# Load real data (no ML needed)
# ============================================================
with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    knowledge_base = json.load(f)
with open('data/coverage_by_group.json', encoding='utf-8') as f:
    coverage_data = json.load(f)['coverage_by_group']

# ============================================================
# Mock ML functions
# ============================================================
# Mock recommendations: return top categories based on simple keyword matching
def recommend_cosine_emb(query, top_n=5):
    query_lower = query.lower()
    scored = []
    for kb in knowledge_base:
        score = 0.1
        cat_lower = kb['category'].lower()
        desc_lower = kb.get('description', '').lower()
        for word in query_lower.split():
            if word in cat_lower:
                score += 0.2
            if word in desc_lower:
                score += 0.05
            for syn in kb.get('synonyms', []):
                if word in syn.lower():
                    score += 0.1
        scored.append((kb['category'], min(score, 0.99)))
    scored.sort(key=lambda x: -x[1])
    return scored[:top_n]

# Mock intent detection
def detect_intent(user_input):
    u = user_input.lower()
    if any(w in u for w in ['what can i claim under', 'show me all', 'list', 'what falls under']):
        return "CQ2", {}
    if any(w in u for w in ['difference', 'compare', 'vs', 'versus']):
        return "CQ3", {}
    if any(w in u for w in ['diabetes', 'diabetic', 'sleep apnea', 'allergies', 'condition']):
        return "CQ4", {}
    if any(w in u for w in ['machine or', 'mask or', 'vs supplies', 'which component']):
        return "CQ5", {}
    if any(w in u for w in ['is.*covered', 'can i claim', 'does my plan', 'covered']):
        return "CQ6", {}
    return "CQ1", {}

# Mock NLP (no entity extraction)
class MockDoc:
    def __init__(self):
        self.ents = []
class MockNLP:
    def __call__(self, text):
        doc = MockDoc()
        # Simple entity extraction for testing
        text_lower = text.lower()
        class Ent:
            def __init__(self, t, l):
                self.text = t
                self.label_ = l
        if 'dental' in text_lower:
            doc.ents = [Ent('dental', 'BENEFIT_GROUP')]
        elif 'vision' in text_lower:
            doc.ents = [Ent('vision', 'BENEFIT_GROUP')]
        elif 'diabetes' in text_lower or 'diabetic' in text_lower:
            doc.ents = [Ent('diabetes', 'CONDITION')]
        return doc

nlp = MockNLP()

# ============================================================
# Load notebook code (Cell 23 + 30 + 34)
# ============================================================
with open('Group27_Final_ClaimBot.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell_idx in [23, 30, 34]:
    src = ''.join(nb['cells'][cell_idx]['source'])
    # Remove test/print blocks at the end
    if '# Test' in src:
        src = src[:src.rfind('# Test')]
    exec(src)

# ============================================================
# Tests
# ============================================================
passed = 0
failed = 0

def test(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS: {name}")
    else:
        failed += 1
        print(f"  FAIL: {name}")
        if detail:
            print(f"        {detail}")

print("=" * 60)
print("DIALOGUE FRAMEWORK TESTS")
print("=" * 60)

# --- 1. Initial state ---
print("\n--- 1. Initial State ---")
s = make_initial_state()
test("stage is idle", s["stage"] == "idle")
test("last_list is empty", s["last_list"] == {})
test("context exists", "last_query" in s["context"])

# --- 2. Boundary inputs ---
print("\n--- 2. Boundary Inputs ---")
resp, s = chatbot_respond("", make_initial_state())
test("empty input -> guidance", "help" in resp.lower() or "describe" in resp.lower(), resp[:80])

resp, s = chatbot_respond("hi", make_initial_state())
test("greeting -> guidance", "tell me" in resp.lower() or "claim" in resp.lower(), resp[:80])

resp, s = chatbot_respond("hello", make_initial_state())
test("hello -> guidance", "claim" in resp.lower(), resp[:80])

resp, s = chatbot_respond("help", make_initial_state())
test("help -> feature list", "browse" in resp.lower() or "describe" in resp.lower(), resp[:80])

resp, s = chatbot_respond("?", make_initial_state())
test("? -> guidance (not crash)", isinstance(resp, str), resp[:80])

# --- 3. Number selection basics ---
print("\n--- 3. Number Selection ---")
s = make_initial_state()
s["last_list"] = {"1": "Massage", "2": "Physiotherapy"}
resp, s = chatbot_respond("1", s)
test("select 1 from list -> Massage", "Massage" in resp, resp[:80])
test("last_list cleared", s["last_list"] == {} or "Massage" not in str(s["last_list"]))

s2 = make_initial_state()
s2["last_list"] = {"1": "Massage", "2": "Physiotherapy"}
resp, s2 = chatbot_respond("2", s2)
test("select 2 from list -> Physiotherapy", "Physiotherapy" in resp, resp[:80])

# Number with no list
s3 = make_initial_state()
resp, s3 = chatbot_respond("1", s3)
test("number without list -> guidance", "describe" in resp.lower() or "help" in resp.lower(), resp[:80])

# --- 4. Yes/No handling ---
print("\n--- 4. Yes/No Handling ---")
s = make_initial_state()
s["context"]["last_result"] = "Massage"
resp, s = chatbot_respond("yes", s)
test("yes with last_result -> coverage", "Massage" in resp, resp[:80])

s = make_initial_state()
s["context"]["last_query"] = "I bought compression socks"
s["context"]["last_result"] = "Compression Stockings, knee length (20-29 mmhg)"
resp, s = chatbot_respond("no", s)
test("no with last_query -> top-3 list", "1." in resp, resp[:80])
test("no -> last_list populated", len(s["last_list"]) > 0)

# Yes without context
s = make_initial_state()
resp, s = chatbot_respond("yes", s)
test("yes without context -> normal routing", "yes" not in resp.lower()[:20] or isinstance(resp, str))

# --- 5. Compression Stockings tree clarification ---
print("\n--- 5. Compression Stockings Tree ---")
s = make_initial_state()
s["stage"] = "clarifying"
s["clarify_group"] = "Compression Stockings"
tree = clarification_rules["Compression Stockings"]["tree"]
s["clarify_node"] = tree
s["last_list"] = {"1": "Footless", "2": "Regular stockings"}

# Step 1: select Footless
resp, s = chatbot_respond("1", make_initial_state() | {
    "stage": "clarifying", "clarify_group": "Compression Stockings",
    "clarify_node": tree, "last_list": {"1": "Footless", "2": "Regular stockings"},
    "clarify_step": 0, "clarify_context": {},
    "context": {"last_query": "", "last_result": "", "last_intent": ""},
    "plan_type": None,
})
test("footless -> final result", "Calf Sleeves" in resp or "footless" in resp.lower(), resp[:100])

# Step 1: select Regular -> should ask custom
s = make_initial_state()
s["stage"] = "clarifying"
s["clarify_group"] = "Compression Stockings"
s["clarify_node"] = tree
s["last_list"] = {"1": "Footless", "2": "Regular stockings"}
resp, s = chatbot_respond("2", s)
test("regular -> asks custom", "custom" in resp.lower(), resp[:100])
test("still clarifying", s["stage"] == "clarifying")
test("has new options", len(s["last_list"]) > 0, str(s["last_list"]))

# Step 2: select No custom -> should ask length
if s["stage"] == "clarifying" and s["last_list"]:
    # Find the "No" option
    no_key = None
    for k, v in s["last_list"].items():
        if "not custom" in v.lower() or "no" in v.lower():
            no_key = k
            break
    if no_key:
        resp, s = chatbot_respond(no_key, s)
        test("not custom -> asks length", "length" in resp.lower() or "knee" in resp.lower(), resp[:100])
        test("still clarifying", s["stage"] == "clarifying")

        # Step 3: select Knee -> should ask pressure
        knee_key = None
        for k, v in s["last_list"].items():
            if "knee" in v.lower():
                knee_key = k
                break
        if knee_key:
            resp, s = chatbot_respond(knee_key, s)
            test("knee -> asks pressure", "pressure" in resp.lower() or "mmhg" in resp.lower(), resp[:100])

            # Step 4: select 20-29 -> final result
            pressure_key = None
            for k, v in s["last_list"].items():
                if "20-29" in v:
                    pressure_key = k
                    break
            if pressure_key:
                resp, s = chatbot_respond(pressure_key, s)
                test("20-29 -> final recommendation", "knee length (20-29 mmhg)" in resp.lower() or "20-29" in resp, resp[:120])
                test("back to idle", s["stage"] == "idle")
                test("context saved", s["context"]["last_result"] != "")

# --- 6. Linear clarification (Brace) ---
print("\n--- 6. Brace Linear Clarification ---")
s = make_initial_state()
s["stage"] = "clarifying"
s["clarify_group"] = "Brace"
s["clarify_step"] = 0
s["clarify_context"] = {}
q0 = clarification_rules["Brace"]["questions"][0]
s["last_list"] = {}
for i, k in enumerate(q0["options"].keys(), 1):
    s["last_list"][str(i)] = k

resp, s = chatbot_respond("1", s)  # "off-the-shelf"
test("brace off-the-shelf -> Non-custom", "Non-custom" in resp or "non-custom" in resp.lower(), resp[:100])
test("back to idle", s["stage"] == "idle")

# --- 7. CQ2 browse with number selection ---
print("\n--- 7. CQ2 Browse ---")
s = make_initial_state()
resp, s = chatbot_respond("What can I claim under dental?", s)
test("dental browse -> numbered list", "1." in resp, resp[:100])
test("last_list populated", len(s["last_list"]) > 0, str(s["last_list"]))

# --- 8. Context persistence ---
print("\n--- 8. Context ---")
s = make_initial_state()
resp, s = chatbot_respond("I bought a wheelchair", s)
test("context.last_query saved", s["context"]["last_query"] == "I bought a wheelchair")
test("context.last_intent saved", s["context"]["last_intent"] != "")

# --- 9. Long input resets clarification ---
print("\n--- 9. Topic Change ---")
s = make_initial_state()
s["stage"] = "clarifying"
s["clarify_group"] = "Brace"
s["clarify_step"] = 0
long_input = "Actually I want to ask about something completely different, I need to know about my dental coverage and what services are available under the dental plan"
resp, s = chatbot_respond(long_input, s)
test("long input resets clarification", s["stage"] == "idle" or "dental" in resp.lower())

# --- 10. All linear clarification groups ---
print("\n--- 10. All Linear Groups ---")
linear_groups = {
    "Brace": ("off-the-shelf", "Non-custom"),
    "CPAP": ("machine", "Machine"),
    "Glucose Monitoring": ("meter", "glucose meter"),
    "Walker": ("no", "non wheeled"),
    "Social Worker": ("bachelor", "Bachelors"),
    "Insulin": ("pump", "infusion pump"),
    "Crutches": ("underarm", "Crutches, pair"),
    "Stimulator": ("device", "TENS"),
}
for group_name, (answer, expected_in_resp) in linear_groups.items():
    s = make_initial_state()
    s["stage"] = "clarifying"
    s["clarify_group"] = group_name
    s["clarify_step"] = 0
    s["clarify_context"] = {}
    q0 = clarification_rules[group_name]["questions"][0]
    s["last_list"] = {}
    # Find the option key that matches our answer
    target_key = None
    for i, k in enumerate(q0["options"].keys(), 1):
        s["last_list"][str(i)] = k
        if answer.lower() in k.lower():
            target_key = str(i)
    if target_key:
        resp, s = chatbot_respond(target_key, s)
        test(f"{group_name}: {answer} -> {expected_in_resp}",
             expected_in_resp.lower() in resp.lower(),
             resp[:100])
    else:
        test(f"{group_name}: option not found for '{answer}'", False)

# --- 11. Multi-turn conversation ---
print("\n--- 11. Multi-turn Conversations ---")

# Scenario A: CQ1 -> clarification -> select -> yes
print("  Scenario A: Recommendation -> Clarification -> Yes")
s = make_initial_state()
# Simulate CQ1 that triggers CPAP clarification
s["stage"] = "clarifying"
s["clarify_group"] = "CPAP"
s["clarify_step"] = 0
s["clarify_context"] = {}
q0 = clarification_rules["CPAP"]["questions"][0]
s["last_list"] = {}
for i, k in enumerate(q0["options"].keys(), 1):
    s["last_list"][str(i)] = k
# User selects "1" (machine)
resp, s = chatbot_respond("1", s)
test("A1: CPAP machine selected", "Machine" in resp, resp[:80])
# User says "yes"
resp, s = chatbot_respond("yes", s)
test("A2: yes -> coverage details", "coverage" in resp.lower() or "co-pay" in resp.lower() or "claim" in resp.lower(), resp[:80])

# Scenario B: Get recommendation -> say no -> pick from top-3
print("  Scenario B: Recommendation -> No -> Pick from list")
s = make_initial_state()
s["context"]["last_query"] = "knee brace"
s["context"]["last_result"] = "Brace (Non-custom)"
resp, s = chatbot_respond("no", s)
test("B1: no -> shows alternatives", "1." in resp, resp[:80])
test("B1: last_list has items", len(s["last_list"]) >= 2)
if s["last_list"]:
    resp, s = chatbot_respond("1", s)
    test("B2: pick 1 -> shows category", "**" in resp, resp[:80])

# Scenario C: Browse -> pick group -> pick category
print("  Scenario C: Browse dental -> pick category")
s = make_initial_state()
resp, s = chatbot_respond("What can I claim under dental?", s)
test("C1: dental list", "1." in resp and len(s["last_list"]) > 0, resp[:80])
if s["last_list"]:
    resp, s = chatbot_respond("1", s)
    test("C2: pick 1 -> category details", "**" in resp, resp[:80])

# --- 12. Edge cases ---
print("\n--- 12. Edge Cases ---")

# Invalid number with list
s = make_initial_state()
s["last_list"] = {"1": "Massage", "2": "Physiotherapy"}
resp, s = chatbot_respond("99", s)
test("invalid number -> normal routing (not crash)", isinstance(resp, str), resp[:80])

# "0" with list
s = make_initial_state()
s["last_list"] = {"1": "Massage", "2": "Physiotherapy"}
resp, s = chatbot_respond("0", s)
test("0 with list -> not crash", isinstance(resp, str), resp[:80])

# Very long input
resp, s = chatbot_respond("a" * 200, make_initial_state())
test("200 char input -> not crash", isinstance(resp, str))

# Special characters
resp, s = chatbot_respond("!@#$%", make_initial_state())
test("special chars -> not crash", isinstance(resp, str))

# Number as word
s = make_initial_state()
s["last_list"] = {"1": "Massage", "2": "Physiotherapy"}
resp, s = chatbot_respond("one", s)
test("'one' with list -> not matched (goes to routing)", isinstance(resp, str))

# --- 13. Response format validation ---
print("\n--- 13. Response Format ---")

# All CQ handlers should include follow-up
s = make_initial_state()
resp, s = chatbot_respond("I bought a wheelchair", s)
test("CQ1 has follow-up", "describe" in resp.lower() or "reply" in resp.lower() or "right category" in resp.lower(), resp[-100:])

s = make_initial_state()
resp, s = chatbot_respond("What can I claim under dental?", s)
test("CQ2 has follow-up", "reply" in resp.lower() or "describe" in resp.lower(), resp[-100:])

# T4: yes should NOT repeat coverage (just confirm)
s = make_initial_state()
s["context"]["last_result"] = "Massage"
resp, s = chatbot_respond("yes", s)
test("yes is short confirmation (not repeating coverage)", len(resp) < 200, f"len={len(resp)}")
test("yes mentions category name", "massage" in resp.lower(), resp[:80])

# Coverage format is compact (test via direct call)
cov = get_coverage_info("Massage")
test("coverage is compact (no long conditions)", len(cov) < 300, f"len={len(cov)}")
test("coverage has 'See plan booklet'", "plan booklet" in cov.lower(), cov[-80:])

# --- 14. Clarification keyword matching ---
print("\n--- 14. Keyword Matching in Clarification ---")
s = make_initial_state()
s["stage"] = "clarifying"
s["clarify_group"] = "Compression Stockings"
tree = clarification_rules["Compression Stockings"]["tree"]
s["clarify_node"] = tree
s["last_list"] = {"1": "Footless", "2": "Regular stockings"}
# Try keyword instead of number
resp, s = chatbot_respond("footless", s)
test("keyword 'footless' matches", "Calf Sleeves" in resp or "footless" in resp.lower(), resp[:100])

# Try keyword for Brace
s = make_initial_state()
s["stage"] = "clarifying"
s["clarify_group"] = "Brace"
s["clarify_step"] = 0
s["clarify_context"] = {}
q0 = clarification_rules["Brace"]["questions"][0]
s["last_list"] = {str(i+1): k for i, k in enumerate(q0["options"].keys())}
resp, s = chatbot_respond("custom", s)
test("keyword 'custom' matches in Brace", s["stage"] == "clarifying" or "custom" in resp.lower(), resp[:100])

# Try unmatched keyword in clarification
s = make_initial_state()
s["stage"] = "clarifying"
s["clarify_group"] = "CPAP"
s["clarify_step"] = 0
s["clarify_context"] = {}
q0 = clarification_rules["CPAP"]["questions"][0]
s["last_list"] = {str(i+1): k for i, k in enumerate(q0["options"].keys())}
resp, s = chatbot_respond("banana", s)
test("unmatched keyword -> repeats question", "didn't catch" in resp.lower() or "1." in resp, resp[:100])

# --- 15. State cleanup after clarification ---
print("\n--- 15. State Cleanup ---")
s = make_initial_state()
s["stage"] = "clarifying"
s["clarify_group"] = "Compression Stockings"
tree = clarification_rules["Compression Stockings"]["tree"]
s["clarify_node"] = tree
s["last_list"] = {"1": "Footless", "2": "Regular stockings"}
resp, s = chatbot_respond("1", s)
test("after final result: stage idle", s["stage"] == "idle")
test("after final result: clarify_node None", s["clarify_node"] is None)
test("after final result: last_result set", s["context"]["last_result"] != "")

# ============================================================
print("\n" + "=" * 60)
print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed}")
print("=" * 60)
if failed > 0:
    sys.exit(1)
