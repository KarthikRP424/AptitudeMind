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
![Status](https://img.shields.io/badge/Project-65%25%20Complete-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

---

## 🚀 What is AptitudeMind?

**AptitudeMind** is an Adaptive Agentic AI Mentor designed to transform traditional aptitude practice into a personalized learning experience.

Instead of simply generating random questions, AptitudeMind is designed to:

- 🧠 Understand the learner's request
- 📚 Select appropriate topics
- 🎯 Adapt question difficulty
- 🤖 Generate questions using a local LLM
- 🔍 Validate AI-generated questions
- 🧮 Verify mathematical consistency
- ♻️ Regenerate invalid questions
- ✅ Evaluate learner answers
- 💡 Explain mistakes
- 🧠 Remember learner performance
- 📊 Detect weak topics
- 🔄 Adapt future practice

---

# 🎯 Project Goal

> **Build an AI mentor that does not merely generate questions, but understands the learner, verifies its own output, remembers performance, and adapts future learning.**

The long-term vision is to evolve AptitudeMind into a complete AI-powered learning platform.

### Planned learning domains

| Domain | Examples |
|---|---|
| 🔢 Quantitative Aptitude | Percentage, Ratio, Algebra, Profit & Loss, Time & Work |
| 🧩 Logical Reasoning | Patterns, Coding-Decoding, Blood Relations, Series |
| 📝 Verbal Ability | Grammar, Vocabulary, Sentence Correction, Reading |

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

