# GreenShield ClaimBot

A content-based recommender system that helps GreenShield+ insurance members identify the correct claim category for their medical expenses through a conversational chatbot interface.

**Course:** DSA/GNG 5125 — Group 27 Final Project

---

## Overview

GreenShield ClaimBot navigates 129+ insurance claim categories using natural language understanding. Users describe their medical expense in plain language and the chatbot recommends the most relevant claim category, asks clarifying questions when needed, and can look up coverage details.

**Key capabilities:**
- Recommend claim categories from a free-text description (e.g., "I bought knee braces")
- Browse all categories within a benefit group
- Compare similar/confusable categories
- Find categories for a medical condition
- Check coverage details (co-pay %, limits, conditions)
- Multi-turn clarification when the top recommendations are ambiguous

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Recommendation | Sentence-BERT (cosine similarity), TF-IDF, Logistic Regression, SVM, Naive Bayes |
| NLP / NER | spaCy (EntityRuler) |
| Embeddings | sentence-transformers |
| Clustering | scikit-learn K-Means |
| Chatbot UI | Gradio Blocks |
| Data processing | pandas, numpy |
| Data augmentation | nlpaug |

---

## Project Structure

```
DTI5125/
└── final_0405/
    ├── Group27_Final_ClaimBot.ipynb   # Main deliverable — run this
    ├── requirements.txt               # Python dependencies
    └── data/
        ├── knowledge_base.json        # 129 claim categories with descriptions & synonyms
        ├── seed_sentences_all.csv     # 1,613 training sentences
        ├── train_augmented.csv        # 6,237 augmented training examples
        ├── test_independent.csv       # Independent test set
        └── coverage_by_group.json     # Coverage details for RAG lookup
```

---

## Setup

**1. Install dependencies**

```bash
cd final_0405
pip install scikit-learn sentence-transformers spacy gradio pandas numpy nlpaug jsonlines
python -m spacy download en_core_web_sm
```

**2. Run the notebook**

Open `Group27_Final_ClaimBot.ipynb` in Jupyter and click **Run All Cells**.

- Cells 0–27: Train models and prepare data (~5 minutes)
- Cells 28–35: Launch the Gradio chatbot interface

**3. Open the chatbot**

Gradio will print a local URL (e.g., `http://127.0.0.1:7860`). Open it in your browser and start typing.

---

## How It Works

Each user message goes through a 7-step pipeline:

1. **Boundary check** — handle greetings, help requests, empty input
2. **Intent routing** — classify query type (recommend / browse / compare / condition / components / coverage) using embedding similarity against intent templates
3. **Named entity recognition** — extract medical items, body parts, conditions, and benefit groups via spaCy EntityRuler
4. **Query handling** — route to the appropriate handler for the detected intent
5. **Clarification** — if top results are ambiguous, ask follow-up questions using decision-tree rules
6. **Coverage lookup** — retrieve co-pay %, annual limits, and conditions from the coverage knowledge base
7. **Response generation** — format and return a structured reply with recommendations and context

**Recommendation model:** Cosine similarity over Sentence-BERT embeddings (best balance of accuracy and generalization — 84.1% P@1 on independent test set, 99%+ after clarification).

---

## Testing

```bash
cd final_0405
python _internal/test_dialogue.py   # 65 automated mock tests (~1 second)
```

Manual test cases (75 scenarios) are documented in `_internal/test_cases.md`.

---

## Results

| Metric | Score |
|--------|-------|
| Intent routing accuracy | 96.6% |
| Recommender P@1 (before clarification) | 84.1% |
| Recommender P@1 (after clarification) | ~99% |
| Automated dialogue tests | 65 / 65 pass |
