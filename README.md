#  AI App Builder (Agentic AI System)

An advanced **Agent-Based AI Application Builder** that autonomously plans, designs, and generates applications using Large Language Models (LLMs).

This project demonstrates a **multi-agent orchestration system** built with LangGraph, enabling structured AI workflows for real-world software generation.

---

##  Key Highlights

*  Multi-Agent Architecture (Planner → Architect → Coder)
*  LLM-driven structured planning using typed outputs
*  Tool-augmented AI (file system operations)
*  Iterative code generation loop
*  State-based workflow management using LangGraph

---

##  System Architecture

This project follows an **Agentic AI Pipeline**:

```
User Prompt
    ↓
 Planner Agent
    ↓
 Architect Agent
    ↓
 Coder Agent (loop)
    ↓
Generated Project Files
```

---

##  Agents Explained

###  Planner Agent

* Converts user input into a structured **Plan**
* Uses LLM with structured output parsing

---

###  Architect Agent

* Transforms Plan → **TaskPlan**
* Breaks system into executable steps

---

###  Coder Agent

* Executes tasks step-by-step
* Uses tools:

  * read_file
  * write_file
  * list_file
  * get_current_directory
* Uses ReAct-style reasoning with LLM

---

##  Tech Stack

* Python
* LangGraph
* LangChain
* Groq LLM
* Google Gemini (Gemini 2.5 Flash)
* dotenv (environment variable management)

---

##  Dependencies

All dependencies are managed using:

```
pyproject.toml
```

Install using:

```
uv sync
```

---

##  Project Structure

```
AI_SE/
│
├── agent/
│   ├── generated_project/      # AI-generated output
│   ├── __init__.py
│   ├── graph.py
│   ├── prompts.py
│   ├── states.py
│   ├── tools.py
│
├── main.py
├── pyproject.toml
├── uv.lock
├── README.md
├── .gitignore
├── .env (excluded)
```

---

##  Workflow (How it works)

1. User provides a prompt
   Example:

   ```
   Build a colourful modern todo app in html css and js
   ```

2. Planner Agent creates structured plan

3. Architect Agent generates implementation steps

4. Coder Agent:

   * Reads files
   * Writes code
   * Iterates until complete

---

##  How to Run

### 1. Clone repository

```
git clone https://github.com/your-username/AI-App-Builder.git
cd AI-App-Builder
```

---

### 2. Create virtual environment

```
python -m venv .venv
```

Activate (Windows):

```
.venv\Scripts\activate
```

---

### 3. Install dependencies

```
uv sync
```

---

### 4. Add environment variables

Create `.env` file:

```
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
```

---

### 5. Run the project

```
python main.py
```

---

##  Example Usage

```python
agent.invoke({
  "user_prompt": "Build a colourful modern todo app in html css and js"
})
```

 Output:

* HTML
* CSS
* JavaScript files automatically generated

---

##  Important Notes

*  No frontend (backend AI system only)
*  `.env` is excluded for security
*  Requires valid API keys (Groq / Gemini)

---

##  Project Purpose

This project is designed to:

* Demonstrate Agentic AI systems
* Showcase LLM orchestration skills
* Build scalable AI-driven applications

---

##  Future Improvements

* Add frontend UI
* Deploy as web application
* Add memory and long-term context
* Improve multi-agent collaboration

---

##  Author

**Thakshana Lakruwan**
Data Science Undergraduate
Aspiring ML / AI Engineer

---

##  Why This Project Matters

This project demonstrates:

* Real-world LLM engineering skills
* Advanced agent workflows
* Practical AI system design

👉 Strong portfolio project for:

* ML Engineer roles
* AI Engineer roles
* Agentic AI / LLM Engineer roles
