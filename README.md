# 🧠 AptitudeMind

<h3 align="center">
  Adaptive Agentic AI Mentor
</h3>

<p align="center">
  <b>Learn smarter. Practice better. Improve continuously.</b>
</p>

<p align="center">
  A local-first Agentic AI platform that generates, validates, evaluates,
  remembers, and adapts aptitude practice based on learner performance.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black)
![Llama](https://img.shields.io/badge/LLM-Llama%203.2-orange)
![Agentic AI](https://img.shields.io/badge/AI-Agentic-purple)
![Status](https://img.shields.io/badge/Project-In%20Development-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

---

## 🚀 What is AptitudeMind?

**AptitudeMind** is an Adaptive Agentic AI Mentor designed to transform traditional aptitude practice into a personalized learning experience.

Instead of simply generating random questions, AptitudeMind is designed to:

* 🧠 Understand the learner's request
* 📚 Select appropriate topics
* 🎯 Adapt question difficulty
* 🤖 Generate questions using a local LLM
* 🔍 Validate AI-generated questions
* 🧮 Verify mathematical consistency
* ♻️ Regenerate invalid questions
* ✅ Evaluate learner answers
* 💡 Explain mistakes
* 🧠 Remember learner performance
* 📊 Detect weak topics
* 🔄 Adapt future practice

---

# 🎯 Project Goal

> **Build an AI mentor that does not merely generate questions, but understands the learner, verifies its own output, remembers performance, and adapts future learning.**

The long-term vision is to evolve AptitudeMind into a complete AI-powered learning platform.

### Planned learning domains

| Domain                   | Examples                                               |
| ------------------------ | ------------------------------------------------------ |
| 🔢 Quantitative Aptitude | Percentage, Ratio, Algebra, Profit & Loss, Time & Work |
| 🧩 Logical Reasoning     | Patterns, Coding-Decoding, Blood Relations, Series     |
| 📝 Verbal Ability        | Grammar, Vocabulary, Sentence Correction, Reading      |

---

# 🌟 Why AptitudeMind?

Traditional aptitude platforms often follow:

```text
Student
   ↓
Question
   ↓
Answer
   ↓
Score
```

AptitudeMind is designed around a continuous learning loop:

```text
              ┌─────────────────────┐
              │      Student        │
              └──────────┬──────────┘
                         ↓
              ┌─────────────────────┐
              │  AptitudeMind Agent │
              └──────────┬──────────┘
                         ↓
              ┌─────────────────────┐
              │ Topic + Difficulty  │
              └──────────┬──────────┘
                         ↓
              ┌─────────────────────┐
              │ Retrieve / Generate │
              └──────────┬──────────┘
                         ↓
              ┌─────────────────────┐
              │     Validator       │
              └──────────┬──────────┘
                         ↓
                  ┌──────┴──────┐
                  │             │
                Invalid        Valid
                  │             │
                  ↓             ↓
             Regenerate       Student
                                ↓
                         Answer Evaluation
                                ↓
                         Progress Memory
                                ↓
                         Weak Topic Analysis
                                ↓
                       Adaptive Next Question
                                │
                                └───────────────↺
```

---

# 🏗️ Current Architecture

AptitudeMind currently follows a modular architecture where different components are responsible for different stages of the learning workflow.

```text
                         ┌─────────────────┐
                         │     Student     │
                         └────────┬────────┘
                                  ↓
                         ┌─────────────────┐
                         │      Agent      │
                         └────────┬────────┘
                                  ↓
                         ┌─────────────────┐
                         │ Search / Intent │
                         └────────┬────────┘
                                  ↓
                    ┌─────────────┴─────────────┐
                    ↓                           ↓
              Question Bank                Generator
                    │                           │
                    └─────────────┬─────────────┘
                                  ↓
                         ┌─────────────────┐
                         │ Question Adapter│
                         └────────┬────────┘
                                  ↓
                         ┌─────────────────┐
                         │    Validator    │
                         └────────┬────────┘
                                  ↓
                         ┌─────────────────┐
                         │   Evaluator     │
                         └────────┬────────┘
                                  ↓
                         ┌─────────────────┐
                         │  Answer Engine  │
                         └────────┬────────┘
                                  ↓
                         ┌─────────────────┐
                         │ Progress Memory │
                         └─────────────────┘
```

### Core principle

> **The LLM generates. Deterministic Python verifies.**

AptitudeMind does not blindly trust the LLM for mathematical correctness.

---

# 🧩 Core Components

| Component             | Responsibility                                          |
| --------------------- | ------------------------------------------------------- |
| `agent.py`            | Agent decision and execution workflow                   |
| `search.py`           | Search query parsing and intent detection               |
| `search_engine.py`    | Question retrieval from the question bank               |
| `question_bank.py`    | Stores and retrieves aptitude questions                 |
| `question_adapter.py` | Converts question-bank records into standardized format |
| `generator.py`        | Generates questions using local LLM                     |
| `validator.py`        | Validates question structure and consistency            |
| `evaluator.py`        | Evaluates student answers                               |
| `answer_engine.py`    | Deterministic mathematical verification                 |
| `difficulty.py`       | Adaptive difficulty selection                           |
| `topics.py`           | Topic management                                        |
| `companies.py`        | Company-specific question filtering                     |

---

# 🔎 Intelligent Search & Intent Detection

AptitudeMind can parse natural search requests and identify:

* 🏢 Company
* 📚 Topic
* 🎯 Difficulty
* 🧩 Question Type

For example:

```text
TCS percentage medium
```

can be interpreted as:

```text
Company     → TCS
Topic       → Percentage
Difficulty  → Medium
```

A more specific request:

```text
profit percentage
```

is interpreted as:

```text
Topic         → Profit and Loss
Question Type → PROFIT_PERCENTAGE
```

This prevents broad topic matching from accidentally returning a different question type.

---

# 🔄 Adaptive Difficulty

When the student does not explicitly specify difficulty, AptitudeMind can select difficulty based on the existing difficulty system.

Example:

```text
Student Request
      ↓
Topic Detection
      ↓
Student Performance
      ↓
Adaptive Difficulty
      ↓
Question Retrieval
```

AptitudeMind also preserves explicit question-type intent during adaptive retrieval.

For example:

```text
User:
profit percentage
```

If adaptive difficulty selects `Hard`, but there is no `PROFIT_PERCENTAGE` question at that difficulty, the Agent preserves the requested question type instead of returning an unrelated `LOSS` question.

---

# 🧩 Question Adapter

The **Question Adapter** standardizes older question-bank records into the format expected by the modern AptitudeMind pipeline.

Currently supported Profit & Loss adaptations include:

* `PROFIT_PERCENTAGE`
* `PROFIT`
* `LOSS`

Percentage questions are also supported.

Example:

```text
Question Bank
      ↓
Question Adapter
      ↓
Standardized Question
      ↓
Validator
```

The adapter has its own test suite, and the current adapter tests for the supported Percentage and Profit & Loss cases have passed.

---

# 🛡️ Question Validation

AptitudeMind validates questions before allowing them into the evaluation pipeline.

The validation layer is designed to prevent problems such as:

* Missing fields
* Invalid question structure
* Invalid options
* Unsupported question formats
* Inconsistent generated questions

The principle is:

```text
Generated / Retrieved Question
             ↓
          Validator
             ↓
       ┌─────┴─────┐
       ↓           ↓
    Invalid       Valid
       ↓           ↓
   Reject /      Continue
  Regenerate
```

---

# 🧮 Deterministic Answer Engine

The Answer Engine performs mathematical verification using deterministic Python logic.

Current supported areas include:

* Percentage
* Profit
* Profit Percentage
* Loss
* Average
* Simple Interest
* Time, Speed & Distance
* Algebra

The Answer Engine calculates the expected answer independently rather than relying on the LLM's reasoning.

Example:

```text
Cost Price = ₹500
Selling Price = ₹600

Profit = ₹600 - ₹500
       = ₹100

Profit Percentage
= (100 / 500) × 100
= 20%
```

---

# 🤖 Agent → Adapter → Validator → Evaluator → Answer Engine

A major implemented workflow is:

```text
Student Request
      ↓
Agent
      ↓
Search / Retrieval
      ↓
Question Adapter
      ↓
Validator
      ↓
Student Answer
      ↓
Evaluator
      ↓
Answer Engine
      ↓
Verified Result
```

This workflow has been tested with real question-bank questions.

---

# ✅ Verified End-to-End Example

A verified Profit Percentage flow:

```text
User Request:
profit percentage
```

The Agent detects:

```text
Topic:
Profit and Loss

Question Type:
PROFIT_PERCENTAGE
```

It retrieves:

```text
An article is bought for ₹500 and sold for ₹600.
What is the profit percentage?
```

Options:

```text
1. 10
2. 15
3. 20
4. 25
```

Student selects:

```text
3
```

The Answer Engine calculates:

```text
Profit = ₹600 - ₹500
       = ₹100

Profit Percentage
= (₹100 / ₹500) × 100
= 20%
```

Result:

```text
CORRECT ✅
```

---

# 🧪 Testing

AptitudeMind uses individual component tests as well as end-to-end workflow testing.

Current verified testing includes:

* ✅ Question Adapter tests
* ✅ Percentage verification
* ✅ Profit verification
* ✅ Profit Percentage verification
* ✅ Loss verification
* ✅ Answer Engine tests
* ✅ Search intent detection
* ✅ Question-type filtering
* ✅ Agent retrieval workflow
* ✅ Adapter → Validator workflow
* ✅ Evaluator → Answer Engine workflow
* ✅ End-to-end Profit Percentage workflow

The project follows:

```text
Build
  ↓
Test
  ↓
Debug
  ↓
Verify
  ↓
Commit
```

rather than adding multiple untested features at once.

---

# 🧠 Current Development Status

AptitudeMind is actively under development.

### Implemented / Working Areas

* ✅ Local LLM integration with Ollama
* ✅ Llama 3.2 integration
* ✅ Question Bank
* ✅ Topic system
* ✅ Company-based question retrieval
* ✅ Search system
* ✅ Question-type intent detection
* ✅ Adaptive difficulty foundation
* ✅ Agent decision layer
* ✅ Agent execution layer
* ✅ Question Adapter
* ✅ Question Validator
* ✅ Deterministic Answer Engine
* ✅ Evaluator
* ✅ Percentage workflow
* ✅ Profit workflow
* ✅ Profit Percentage workflow
* ✅ Loss workflow
* ✅ Progress / memory foundation
* ✅ Agent → Adapter → Validator → Evaluator → Answer Engine pipeline

### 🚧 In Development

* 🚧 More deterministic aptitude question types
* 🚧 Stronger AI question generation
* 🚧 Self-correction and regeneration
* 🚧 Advanced adaptive intelligence
* 🚧 RAG knowledge base
* 🚧 Complete Agent loop
* 🚧 FastAPI backend
* 🚧 Web interface
* 🚧 Analytics dashboard
* 🚧 Larger testing framework
* 🚧 Deployment
* 🚧 Final documentation and demo

---

# 🗺️ Development Roadmap

```text
Phase 1
Local LLM + Tools
        ↓
Phase 2
Question Bank + Search
        ↓
Phase 3
Adaptive Difficulty
        ↓
Phase 4
Agent Decision Layer
        ↓
Phase 5
Question Adapter + Validator
        ↓
Phase 6
Deterministic Answer Engine
        ↓
Phase 7
Evaluator + Student Progress
        ↓
Phase 8
Advanced Question Generation
        ↓
Phase 9
Adaptive Intelligence
        ↓
Phase 10
RAG Knowledge Base
        ↓
Phase 11
Complete Agent Workflow
        ↓
Phase 12
FastAPI Backend
        ↓
Phase 13
Web Application
        ↓
Phase 14
Analytics + Gamification
        ↓
Phase 15
Testing + Deployment
```

---

# 🛠️ Technology Stack

### Programming

* Python 3.12

### AI / LLM

* Ollama
* Llama 3.2

### Current Architecture

* Agentic AI workflow
* Deterministic verification
* Structured question processing
* Adaptive difficulty
* Persistent learner progress

### Planned Technologies

* FastAPI
* RAG
* Vector database
* Embeddings
* Web frontend
* Analytics
* Deployment infrastructure

---

# 💡 Design Philosophy

AptitudeMind follows several engineering principles.

### 1. LLM should not be blindly trusted

```text
LLM
 ↓
Generate
 ↓
Validate
 ↓
Verify
 ↓
Use
```

### 2. Separate responsibilities

Each component has a specific responsibility instead of putting the entire system inside one large AI prompt.

### 3. Deterministic verification

Mathematical answers should be independently verified whenever possible.

### 4. Build incrementally

Every major feature should be:

```text
Implemented
    ↓
Tested
    ↓
Integrated
    ↓
Verified
```

### 5. Preserve learner intent

If a learner asks for a specific question type, adaptive systems should not silently replace it with an unrelated question type.

---

# 📂 Project Structure

```text
AptitudeMind/
│
├── agent.py
├── answer_engine.py
├── companies.py
├── difficulty.py
├── evaluator.py
├── generator.py
├── question_adapter.py
├── question_bank.py
├── search.py
├── search_engine.py
├── topics.py
├── validator.py
│
├── tests/
│
├── README.md
└── requirements.txt
```

---

# 🚀 Running AptitudeMind

### 1. Clone the repository

```bash
git clone https://github.com/KarthikRP424/AptitudeMind.git
cd AptitudeMind
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate environment

```bash
source .venv/bin/activate
```

### 4. Make sure Ollama is installed and running

```bash
ollama list
```

The project currently uses:

```text
llama3.2:3b
```

### 5. Run the Agent

```bash
python agent.py
```

Example:

```text
🔎 Enter your request: profit percentage
```

---

# 🔬 Engineering Milestones

AptitudeMind is being developed through verified milestones rather than treating the entire system as one large implementation.

Recent milestones include:

```text
Question Bank
      ↓
Search
      ↓
Question Adapter
      ↓
Percentage Integration
      ↓
Profit Integration
      ↓
Profit Percentage Integration
      ↓
Loss Integration
      ↓
Validator
      ↓
Evaluator
      ↓
Answer Engine
      ↓
Agent End-to-End Workflow
      ↓
Question-Type Intent Preservation
```

---

# 📌 Current Focus

The current development focus is **stabilizing the Agent workflow** before expanding into larger features.

The next engineering focus areas are:

1. Profit Agent testing
2. Loss Agent testing
3. Wrong-answer handling
4. Invalid-answer handling
5. Unsupported-question handling
6. No-question retrieval path
7. Generated-question path
8. Regeneration
9. Full regression testing
10. Expansion to additional aptitude types

---

# 🌱 Long-Term Vision

The final goal is not simply to create an AI question generator.

The goal is to build:

> **A personal AI aptitude mentor that understands the learner, generates or retrieves suitable practice, verifies its own work, remembers performance, identifies weaknesses, and continuously adapts the learning experience.**

```text
Learn
  ↓
Practice
  ↓
Evaluate
  ↓
Remember
  ↓
Understand Weakness
  ↓
Adapt
  ↓
Practice Again
  ↺
```

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Karthik R P**

ECE Student | AI & Agentic AI Enthusiast | Aspiring AI Engineer

GitHub:

https://github.com/KarthikRP424

---

<p align="center">
  <b>🚀 AptitudeMind is under active development.</b>
</p>

<p align="center">
  Built step by step with learning, testing, debugging, and iteration.
</p>
