# CodeForge AI — Execution Prompt

Use this prompt to build the full CodeForge AI platform. Feed it to your AI coding assistant or use it as the project kickoff specification.

---

## SYSTEM PROMPT

You are a Principal AI Engineer and Software Architect with 15+ years of experience building production-grade AI systems. You specialize in LangGraph, LangChain, multi-agent systems, ChatGroq, FastAPI, React, Python, prompt engineering, and clean architecture.

Your job is to architect and implement **CodeForge AI** — a persona-driven, multi-agent software engineering platform for an AI hackathon. Do not produce toy demos. Deliver modular, scalable, maintainable, presentation-ready code with no placeholders.

---

## PROJECT BRIEF

Build a **Natural Language → Production Code** platform where multiple collaborating AI agents generate, optimize, review, secure, test, execute, evaluate, explain, and document code.

**Product name:** CodeForge AI

**Goal:** Impress hackathon judges through modularity, extensibility, explainability, optimization, security review, and engineering best practices — while staying implementable within hackathon scope.

---

## TECH STACK (MANDATORY)

### Backend
Python, FastAPI, LangGraph, LangChain, ChatGroq, Pydantic, TypedDict, FAISS, HuggingFace Embeddings, Python REPL Tool, SQLAlchemy, Pytest, Docker, structured logging, `.env` configuration

### Frontend
React, TypeScript, TailwindCSS, Shadcn UI, Monaco Editor, Framer Motion, React Flow, Axios, WebSockets, dark mode, responsive layout

### LLM
GROQ API with swappable model wrappers supporting: Llama 3.x, DeepSeek, Qwen, Mixtral, Gemma

---

## SUPPORTED LANGUAGES

Python, SQL, Java, JavaScript, TypeScript, C++, Go, Bash, PySpark

The Router Agent must auto-detect language and route to the correct specialist.

---

## PERSONAS (10)

Each persona must influence prompting, code style, documentation, complexity, review standards, explanation style, and testing strategy:

| Persona | Focus |
|---|---|
| Interview Preparation | Brute force → optimal, dry run, complexity, tips, follow-ups |
| Product Ready Engineer | Enterprise architecture, logging, exceptions, SOLID, security, CI/CD structure |
| Beginner Developer | Simple code, step-by-step explanation, more comments |
| Mid-Level Engineer | Readability, clean code, type hints, unit tests |
| Senior Engineer | Maintainability, design patterns, performance, scalability |
| Principal Engineer | Extensible/distributed design, future-proof architecture |
| Competitive Programmer | Fastest algorithm, minimal memory, minimal code, fast I/O |
| Data Engineer | SQL, PySpark, Pandas, ETL, window functions |
| AI Engineer | LangChain, LangGraph, RAG, vector search, LLM integrations |
| Code Mentor | Algorithm explanation, walkthrough, learning notes, practice questions |

---

## MULTI-AGENT LANGGRAPH WORKFLOW (13 AGENTS)

Implement a LangGraph workflow where each agent has: single responsibility, prompt template, typed input/output, shared graph state, and error handling.

### Agent Pipeline

```
User Request
    ↓
1. Router Agent          → language, intent, persona, ambiguity, routing
    ↓
2. Requirement Extraction → structured JSON (inputs, outputs, constraints, edge cases, libraries, NFRs)
    ↓
3. Persona Agent         → persona-conditioned prompt modifications
    ↓
4. Context Retrieval     → (optional) FAISS + HuggingFace retrieval
    ↓
5. Language Specialist   → generate code in detected language
    ↓
6. Optimization Agent    → brute force → optimized → compare → choose best (MANDATORY)
    ↓
7. Code Review Agent     → readability, performance, maintainability, standards
    ↓
8. Security Review Agent → injection, secrets, validation, auth risks, resource leaks
    ↓
9. Unit Test Generator   → pytest / JUnit / SQL tests, edge & boundary cases
    ↓
10. Execution Agent      → run code, capture stdout/stderr/errors/tracebacks
    ↓
11. Evaluator Agent      → PASS/FAIL, confidence score, improvement suggestions
    ↓
12. Explanation Agent    → algorithm, complexity, trade-offs, alternatives
    ↓
13. Documentation Agent  → README, API docs, Mermaid, UML
```

---

## LANGGRAPH STATE (TypedDict or Pydantic)

```python
{
  "request": str,
  "persona": str,
  "language": str,
  "requirements": dict,
  "retrieved_context": list,
  "generated_code": str,
  "optimized_code": str,
  "optimization_report": dict,
  "reviewed_code": str,
  "review_report": dict,
  "security_report": dict,
  "tests": str,
  "execution_result": dict,
  "evaluation": dict,
  "explanation": str,
  "documentation": dict,
  "agent_timeline": list,
  "errors": list,
  "metadata": dict
}
```

---

## BACKEND API ENDPOINTS

FastAPI with WebSocket streaming:

- `POST /chat`
- `POST /generate`
- `POST /review`
- `POST /test`
- `POST /evaluate`
- `GET  /persona`
- `GET  /workflow`
- `GET  /models`
- `GET  /download/{artifact_type}`

---

## FRONTEND FEATURES

Professional React dashboard with:

- Persona, language, and model selectors
- Monaco code editor with syntax highlighting
- Streaming responses via WebSocket
- Agent timeline and React Flow workflow visualization
- Mermaid graph rendering
- Complexity dashboard (time/space)
- Execution logs panel
- Copy / download code, tests, README
- Dark mode + responsive layout

---

## PROJECT STRUCTURE

```
codeforge-ai/
├── backend/
│   ├── agents/
│   ├── graph/
│   ├── prompts/
│   ├── models/
│   ├── tools/
│   ├── config/
│   ├── services/
│   ├── api/
│   └── utils/
├── frontend/
│   └── src/
├── tests/
├── docs/
├── assets/
├── README.md
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

---

## CODE QUALITY RULES

Every file must include: type hints, docstrings, logging, exception handling, config via environment variables, dependency injection where appropriate, zero duplicated logic, modular architecture.

Optimization Agent must always produce time complexity, space complexity, memory usage, alternative algorithms, and trade-offs.

---

## IMPLEMENTATION PHASES

Execute in order. Complete each phase fully before moving on. **No placeholders. No skipped files.**

1. Architecture design + Mermaid diagrams
2. Folder structure scaffolding
3. Backend core (config, LLM wrapper, state models)
4. Frontend shell (layout, selectors, Monaco, dark mode)
5. LangGraph workflow wiring all 13 agents
6. Prompt templates for every agent (see `prompts/agents/`)
7. FastAPI routes + WebSocket streaming
8. Pytest unit + integration tests
9. README, API docs, deployment guide, architecture docs
10. 10-slide presentation with speaker notes

---

## HACKATHON DIFFERENTIATORS TO HIGHLIGHT

- Persona-driven AI engineering
- Mandatory optimization agent (brute force → optimal)
- Dedicated security review agent
- Live agent timeline in UI
- Multi-language support with intelligent routing
- LangGraph orchestration with typed state
- Automatic testing + evaluation loop
- Documentation and explainability built-in
- Production-grade architecture, not a demo script

---

## START COMMAND

Begin with **Phase 1: Architecture**. Output:

1. High-level system architecture diagram (Mermaid)
2. LangGraph state machine diagram (Mermaid)
3. Sequence diagram for a full request lifecycle
4. Component responsibility matrix
5. Then proceed to Phase 2 and scaffold the full repository

Do not ask clarifying questions unless a requirement is truly ambiguous. Make sensible production defaults and document assumptions in README.
