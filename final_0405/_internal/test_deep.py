"""Deep multi-turn tests + 10 new single-turn cases. Mock ML."""
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    knowledge_base = json.load(f)
with open('data/coverage_by_group.json', encoding='utf-8') as f:
    coverage_data = json.load(f)['coverage_by_group']

def recommend_cosine_emb(query, top_n=5):
    q = query.lower()
    qwords = set(q.split())
    scored = []
    for kb in knowledge_base:
        score = 0.05
        cat_lower = kb['category'].lower()
        desc_lower = kb.get('description', '').lower()
        kws = [k.lower() for k in kb.get('keywords', [])]
        syns = [s.lower() for s in kb.get('synonyms', [])]
        for w in qwords:
            if len(w) < 3: continue
            if w in cat_lower: score += 0.25
            if w in desc_lower: score += 0.08
            for s in syns:
                if w in s: score += 0.15
            for k in kws:
                if w in k: score += 0.12
        for s in syns:
            if s in q: score += 0.3
        for k in kws:
            if k in q: score += 0.2
        scored.append((kb['category'], min(score, 0.99)))
    scored.sort(key=lambda x: -x[1])
    return scored[:top_n]

def detect_intent(user_input):
    u = user_input.lower()
    if any(w in u for w in ['what can i claim under', 'show me all', 'what falls under']): return 'CQ2', {}
    if any(w in u for w in ['difference between', 'compare', ' vs ']): return 'CQ3', {}
    if any(w in u for w in ['i have diabetes', 'diabetic', 'sleep apnea']): return 'CQ4', {}
    if any(w in u for w in ['covered', 'can i claim']): return 'CQ6', {}
    return 'CQ1', {}

class MockDoc:
    def __init__(self): self.ents = []
class MockNLP:
    def __call__(self, text):
        doc = MockDoc()
        class Ent:
            def __init__(self, t, l): self.text = t; self.label_ = l
        tl = text.lower()
        if 'dental' in tl: doc.ents = [Ent('dental', 'BENEFIT_GROUP')]
        elif 'vision' in tl: doc.ents = [Ent('vision', 'BENEFIT_GROUP')]
        elif 'hearing' in tl: doc.ents = [Ent('hearing', 'BENEFIT_GROUP')]
        elif 'diabetes' in tl: doc.ents = [Ent('diabetes', 'CONDITION')]
        elif 'sleep apnea' in tl: doc.ents = [Ent('sleep apnea', 'CONDITION')]
        return doc
nlp = MockNLP()

with open('Group27_Final_ClaimBot.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)
for ci in [23, 30, 34]:
    src = ''.join(nb['cells'][ci]['source'])
    if '# Test' in src: src = src[:src.rfind('# Test')]
    exec(src)

# ================================================================
print('=' * 60)
print('10 NEW SINGLE-TURN CASES')
print('=' * 60)

new_cases = [
    ('N01', 'I need to claim my eye exam', 'Eye Exam'),
    ('N02', 'bought a blood pressure monitor', 'Blood Pressure'),
    ('N03', 'I saw a chiropractor', 'Chiropractic'),
    ('N04', 'sleep apnea machine', 'CPAP'),
    ('N05', 'I got custom orthotics from my podiatrist', 'Orthotic'),
    ('N06', 'prescription medication for anxiety', 'Drug'),
    ('N07', 'how to claim my contact lenses', 'Contact'),
    ('N08', 'I bought a glucose meter', 'glucose meter'),
    ('N09', 'need to claim ambulance ride', 'Ambulance'),
    ('N10', 'acupuncture session last week', 'Acupuncture'),
]

for tid, inp, expected in new_cases:
    s = make_initial_state()
    resp, s = chatbot_respond(inp, s)
    first_line = resp.split(chr(10))[0] if resp else ''
    found = expected.lower() in resp.lower()
    status = 'PASS' if found else 'FAIL'
    print(f'[{tid}] {status} | "{inp}"')
    if not found:
        print(f'       Expected: {expected}')
        print(f'       Got: {first_line[:100]}')
    print()

# ================================================================
print('=' * 60)
print('DEEP TEST 1: Compression Stockings full flow')
print('User wants: knee length, 20-29 mmhg, not custom, regular')
print('=' * 60)

s = make_initial_state()

resp, s = chatbot_respond('I bought compression stockings', s)
print(f'\nT1 USER: I bought compression stockings')
print(f'T1 BOT:\n{resp}')
print(f'   [stage={s["stage"]}, list={dict(list(s.get("last_list",{}).items())[:3])}]')

resp, s = chatbot_respond('2', s)
print(f'\nT2 USER: 2 (Regular)')
print(f'T2 BOT:\n{resp}')
print(f'   [stage={s["stage"]}, list={dict(list(s.get("last_list",{}).items())[:3])}]')

no_key = next((k for k,v in s.get('last_list',{}).items() if 'not' in v.lower()), '2')
resp, s = chatbot_respond(no_key, s)
print(f'\nT3 USER: {no_key} (Not custom)')
print(f'T3 BOT:\n{resp}')
print(f'   [stage={s["stage"]}, list={dict(list(s.get("last_list",{}).items())[:3])}]')

knee_key = next((k for k,v in s.get('last_list',{}).items() if 'knee' in v.lower()), '1')
resp, s = chatbot_respond(knee_key, s)
print(f'\nT4 USER: {knee_key} (Knee)')
print(f'T4 BOT:\n{resp}')
print(f'   [stage={s["stage"]}, list={dict(list(s.get("last_list",{}).items())[:4])}]')

p_key = next((k for k,v in s.get('last_list',{}).items() if '20-29' in v), '3')
resp, s = chatbot_respond(p_key, s)
print(f'\nT5 USER: {p_key} (20-29 mmhg)')
print(f'T5 BOT:\n{resp}')
print(f'   [stage={s["stage"]}]')

resp, s = chatbot_respond('yes', s)
print(f'\nT6 USER: yes')
print(f'T6 BOT:\n{resp}')

# ================================================================
print('\n' + '=' * 60)
print('DEEP TEST 2: Browse vision -> pick -> no -> re-describe')
print('=' * 60)

s = make_initial_state()

resp, s = chatbot_respond('What can I claim under vision?', s)
print(f'\nT1 USER: What can I claim under vision?')
print(f'T1 BOT:\n{resp}')

if s.get('last_list'):
    resp, s = chatbot_respond('1', s)
    print(f'\nT2 USER: 1 (pick first)')
    print(f'T2 BOT:\n{resp}')

    resp, s = chatbot_respond('no', s)
    print(f'\nT3 USER: no')
    print(f'T3 BOT:\n{resp}')

    resp, s = chatbot_respond('I need prescription glasses with bifocal lenses', s)
    print(f'\nT4 USER: I need prescription glasses with bifocal lenses')
    print(f'T4 BOT:\n{resp}')

# ================================================================
print('\n' + '=' * 60)
print('DEEP TEST 3: Prescription drug -> yes -> claim another item')
print('=' * 60)

s = make_initial_state()

resp, s = chatbot_respond('I need to claim my prescription medication', s)
print(f'\nT1 USER: I need to claim my prescription medication')
print(f'T1 BOT:\n{resp}')

resp, s = chatbot_respond('yes', s)
print(f'\nT2 USER: yes')
print(f'T2 BOT:\n{resp}')

resp, s = chatbot_respond('I also had a massage therapy session', s)
print(f'\nT3 USER: I also had a massage therapy session')
print(f'T3 BOT:\n{resp}')

resp, s = chatbot_respond('yes', s)
print(f'\nT4 USER: yes')
print(f'T4 BOT:\n{resp}')
