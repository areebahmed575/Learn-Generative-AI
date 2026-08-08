# 📋 Module 2 Recap: Datasets & Evaluation

## The big picture

Module 1 was about **watching** your app run (tracing). Module 2 is about **testing**
whether your app is any *good* — and proving that changes make it better, not worse.

**The school exam analogy runs through everything:**
- **Dataset** = the exam paper + answer key
- **App** = the student taking the exam
- **Evaluator** = the teacher marking answers
- **Experiment** = conducting the exam and recording grades

---

## The 5 concepts

### 1️⃣ Dataset — the answer key
A collection of **test questions paired with ideal answers**. Each pair is an "example."

```python
client.create_examples(inputs=[{"question": ...}], outputs=[{"output": ...}], dataset_id=...)
```

→ *Your fixed set of test cases to measure against.*

### 2️⃣ Evaluator — grades ONE answer
A function that compares the app's answer (`outputs`) to the correct answer
(`reference_outputs`) and returns `{"score", "key"}`. **Two kinds:**

| Type | How it grades | Example |
|---|---|---|
| **Code-based** | Simple Python rules | `outputs == reference` , length check |
| **LLM-as-Judge** | Ask an LLM to score meaning | "How similar 1–10?" |

→ *Why LLM-as-Judge?* Because `==` only checks if text is *letter-for-letter identical* —
useless for free text where the same meaning is worded differently. An LLM understands **meaning**.

### 3️⃣ Experiment — run the app over the WHOLE dataset + grade it

```python
evaluate(target_function, data=dataset, evaluators=[...], experiment_prefix="gpt-4o")
```

- `target_function` = tiny **adapter** turning the dataset's `{"question": ...}` dict into your app's string input.
- Loops over every example → gets app's answer → grades it → records scores.
- **The payoff:** run once for gpt-4o, again for gpt-3.5, compare side-by-side → *objective proof* of which is better.

### 4️⃣ Pairwise experiment — compare TWO versions head-to-head
For when there's **no correct answer** (e.g. summaries — many are valid).

```python
evaluate(("Experiment A", "Experiment B"), evaluators=[ranked_preference])
```

- Evaluator's `outputs` is a **list of two** answers; an LLM judge picks the winner (A / B / tie).
- First arg is a **tuple of two experiment names**, not a function.

→ *"Which is better?" is easier & more reliable than "rate this 7.3/10."*

### 5️⃣ Summary evaluator — ONE score for the whole experiment
For metrics that need **all answers at once** (e.g. F1-score, overall accuracy %).

```python
evaluate(app, data=dataset, summary_evaluators=[f1_score...])  # note: summary_evaluators
```

- Receives a **list of all** outputs + references → returns **one** overall number.
- Wired in with `summary_evaluators=[...]`, not `evaluators=[...]`.

---

## Normal vs. Summary vs. Pairwise — the key difference

```
Normal evaluator:   answer₁→score,  answer₂→score,  answer₃→score    (one each)
Summary evaluator:  [all answers] → ONE overall score               (whole set)
Pairwise:           A vs B per question → who wins                   (two apps compared)
```

---

## The 🔑 recurring building blocks

- **`langsmith_extra` / metadata** → attach searchable labels to runs (from Module 1, reused everywhere).
- **LLM-as-Judge** → the trick behind grading free text; appears in evaluators, pairwise, and beyond.
- **`response_format` (Pydantic)** → forces the judge LLM to return a **clean number** instead of rambling.
- **`experiment_prefix`** → names your experiment so you can find & compare it in the UI.

---

## Real-world use: this is your CI/CD safety net

Run these evaluations **before shipping to production** — like unit tests, but for answer *quality*.

- `evaluate()` → rich dashboards & version comparison.
- **LangSmith's pytest integration** (`@pytest.mark.langsmith` + `assert`) → actually **fails the CI pipeline** and blocks a bad deploy.
- ⚠️ Keep the CI dataset **small** (LLM calls cost money & are slow), gate on a **threshold** (not perfection), since answers are non-deterministic.

---

## One-line takeaways

| Concept | In one line |
|---|---|
| **Dataset** | Your answer key — questions + ideal answers |
| **Evaluator** | Grades one answer (code rules or LLM-as-Judge) |
| **Experiment** | Runs the app over the dataset, scores it, lets you compare versions |
| **Pairwise** | Compares two versions head-to-head — no answer key needed |
| **Summary evaluator** | One overall metric (F1, accuracy) across the whole experiment |

---

**In a sentence:** *Module 2 gives you a repeatable, objective way to measure your LLM
app's quality — build a dataset (answer key), grade answers with evaluators (including
LLM-as-Judge), run experiments to compare versions, use pairwise when there's no right
answer, and summary evaluators for whole-dataset metrics — so you can prove improvements
and catch regressions before production.*
