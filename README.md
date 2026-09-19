# 🧠 Adaptive Cognitive Test

An AI-powered adaptive cognitive assessment system that dynamically selects the next question based on the user's recent performance, difficulty level, cognitive category, and current test state.

---

## 📌 Project Overview

The system presents a short cognitive assessment consisting of 10 questions selected from a larger question bank.

Unlike a fixed-sequence quiz, the next question is selected dynamically based on the user's performance.

The system considers:

- Recent answer accuracy
- Current adaptive confidence
- Question difficulty
- Cognitive category performance
- Previously asked questions
- Remaining questions in the question bank

The application also provides a short explanation describing why the next question was selected.

---

## 🎯 Objectives

The project demonstrates:

- Adaptive question selection
- Stateful decision-making
- Difficulty adaptation
- Category adaptation
- Deterministic scoring
- LLM-assisted explanations
- LangGraph workflow orchestration
- API failure handling
- Final cognitive performance profiling

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    │       app.py        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Test State       │
                    │     state.py        │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
     ┌──────────────────┐             ┌──────────────────┐
     │  Scoring Engine  │             │ Question Selector│
     │   scoring.py     │             │   selector.py    │
     └────────┬─────────┘             └────────┬─────────┘
              │                                │
              │                                ▼
              │                       ┌──────────────────┐
              │                       │    LangGraph     │
              │                       │     graph.py     │
              │                       └────────┬─────────┘
              │                                │
              │                                ▼
              │                       ┌──────────────────┐
              │                       │   Gemini Agent   │
              │                       │   llm_agent.py   │
              │                       └──────────────────┘
              │
              ▼
     ┌──────────────────┐
     │ Cognitive Profile│
     │  profile_agent.py│
     └──────────────────┘
```

---

## 📂 Project Structure

```text
cognitive_adaptive_test/
│
├── agents/
│   ├── graph.py
│   ├── llm_agent.py
│   └── profile_agent.py
│
├── core/
│   ├── question_bank.py
│   ├── scoring.py
│   ├── selector.py
│   └── state.py
│
├── data/
│   └── questions.json
│
├── utils/
│   └── graph_runner.py
│
├── app.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🔄 Adaptive Question Selection

The system uses two main adaptive mechanisms.

### 1. Difficulty Adaptation

Recent performance is calculated from the user's most recent three answers.

```text
Recent accuracy >= 75%
        ↓
      HARD

Recent accuracy between 40% and 75%
        ↓
     MEDIUM

Recent accuracy <= 40%
        ↓
      EASY
```

This allows the assessment difficulty to respond to the user's recent performance.

### 2. Category Adaptation

The system tracks attempts and correct answers separately for:

- Logical Reasoning
- Numerical Reasoning
- Pattern Recognition
- Verbal Reasoning

At the beginning of the test, categories with fewer attempts are prioritized to maintain balanced coverage.

Once all categories have been assessed, the selector calculates category accuracy and can focus on the category with the lowest observed accuracy.

Example:

```text
Logical Reasoning      100%
Numerical Reasoning     50%
Pattern Recognition    100%
Verbal Reasoning       100%
        ↓
Numerical Reasoning
```

This allows the system to identify categories that require additional assessment.

---

## 🧠 Selection Logic

The selector follows this order:

```text
1. Determine target difficulty
           ↓
2. Determine target category
           ↓
3. Find unused question matching
   both difficulty and category
           ↓
4. If unavailable, find an unused
   question at the target difficulty
           ↓
5. If target difficulty is exhausted,
   choose the closest available difficulty
           ↓
6. Avoid previously asked questions
```

This prevents repeated questions while maintaining adaptive behavior.

---

## 📊 Persistent Test State

The test maintains state throughout the session.

The state contains:

- Current question
- Current difficulty
- Score
- Questions answered
- Asked question IDs
- User answers
- Category scores
- Category attempts
- Recent performance
- Adaptive confidence
- Selection explanation
- Completion status

This allows each question-selection decision to use the history of the current test.

---

## 🤖 LLM Integration

Google Gemini is used to generate a short natural-language explanation for the question-selection decision.

The LLM receives information such as:

- Selected difficulty
- Selected category
- Recent accuracy
- Category accuracy
- Category selection reason

The model is instructed to explain only observable test-state information and not make claims about intelligence, personality, or other unsupported characteristics.

Example:

> Selected a hard Numerical Reasoning question because recent performance has been strong, and Numerical Reasoning has not been assessed much yet.

---

## 🛡️ API Failure Handling

The adaptive decision itself does not depend on the LLM.

The core question-selection logic is deterministic Python logic.

If the Gemini API:

- Is unavailable
- Returns an error
- Does not return usable text
- Has no API key configured

the system automatically uses a deterministic fallback explanation.

Therefore, an API failure does not prevent the cognitive test from continuing.

---

## 🔗 LangGraph

LangGraph is used to represent the adaptive workflow.

The workflow contains nodes for:

```text
Select Question
      ↓
Evaluate Answer
      ↓
Update State
      ↓
Check Completion
      ↓
Select Next Question
```

The current Streamlit execution uses LangGraph for the next-question selection workflow while deterministic Python functions handle scoring and state updates.

This keeps the core adaptive logic transparent and testable.

---

## 📈 Cognitive Profile

After completing the assessment, the system generates a final profile containing:

- Overall score
- Overall accuracy
- Category-wise performance
- Number of questions answered
- Observed strongest categories
- Categories with the lowest observed accuracy
- Question-by-question response summary

Category results are based only on the user's observed performance during the current test attempt.

---

## 🗃️ Question Bank

The system contains a question bank with:

- 20 questions
- Multiple difficulty levels
- Multiple cognitive categories
- Unique question IDs
- Four answer options per question

### Difficulty Levels

- Easy
- Medium
- Hard

### Cognitive Categories

- Logical Reasoning
- Numerical Reasoning
- Pattern Recognition
- Verbal Reasoning

---

## 💻 Technologies Used

- Python
- Streamlit
- LangGraph
- Google Gemini API
- python-dotenv
- JSON

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd cognitive_adaptive_test
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Do not commit the `.env` file to GitHub.

The `.gitignore` file excludes:

```text
.env
.venv/
__pycache__/
*.pyc
```

---

## ▶️ Running the Application

Run:

```bash
streamlit run app.py
```

The application will open in the browser.

---

## 🧪 Testing

The system was tested using different performance patterns.

### Strong-Performance Path

Correct answers increase recent accuracy.

Expected behavior:

```text
Medium → Hard
```

### Weak-Performance Path

Incorrect answers decrease recent accuracy.

Expected behavior:

```text
Medium → Easy
```

### Category Adaptation

The system was also tested with lower performance in individual categories.

Expected behavior:

```text
Balanced category coverage
        ↓
Identify lower-performing category
        ↓
Prioritize that category
```

---

## 🧩 Design Decisions

### Deterministic Core Logic

The core adaptive decision-making logic is implemented using Python rather than delegating the decision entirely to an LLM.

This makes question selection:

- Explainable
- Reproducible
- Easier to test
- Less vulnerable to hallucination

### LLM as an Explanation Layer

Gemini is used primarily to convert the internal selection state into a concise human-readable explanation.

The design separates:

```text
Decision-making
      ↓
Deterministic Python logic

Explanation
      ↓
Gemini
```

This prevents an LLM failure from stopping the assessment.

---

## 🤖 AI Assistance Disclosure

AI tools were used during development for:

- Code suggestions
- Debugging assistance
- Architecture discussion
- Streamlit implementation guidance
- LangGraph implementation guidance
- Gemini integration guidance
- Documentation drafting

The core adaptive logic was reviewed, tested, and modified during implementation.

The final implementation was tested manually through multiple assessment runs, including both strong- and weak-performance scenarios.

---

## 🎥 Demo

The demo demonstrates:

1. Starting the assessment
2. Answering questions
3. Difficulty adaptation
4. Category adaptation
5. Question-selection explanations
6. Answer feedback
7. Persistent progress tracking
8. Final cognitive profile

---

## 📌 Future Improvements

Possible future improvements include:

- Larger question banks
- More granular difficulty levels
- Additional cognitive categories
- More advanced performance models
- Persistent results storage
- User authentication
- Analytics dashboard
- More sophisticated adaptive policies

---

## 👩‍💻 Author

Sadaf fatemah Jumani


