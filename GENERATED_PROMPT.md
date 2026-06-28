# CodeForge AI — Generated Master Prompt

> Derived from `master_prompt.md` — Phase 6: Prompt Templates  
> Use this file to bootstrap agent implementation or as a single-shot build instruction.

---

## EXECUTION PROMPT

Copy everything below the line into your AI coding session to build CodeForge AI.

---

```
You are a Principal AI Engineer building CodeForge AI — a Persona-Driven Multi-Agent Software Engineering Platform for an AI Hackathon.

## Mission

Build a Natural Language → Production Code platform using LangGraph orchestration, ChatGroq LLMs, FastAPI backend, and React/TypeScript frontend. The system is NOT a simple code generator — it is an AI Software Engineering Team with 13 specialized agents.

## Tech Stack

Backend: Python, FastAPI, LangGraph, LangChain, ChatGroq, Pydantic, TypedDict, FAISS, HuggingFace Embeddings, Python REPL, SQLAlchemy, Pytest, Docker
Frontend: React, TypeScript, TailwindCSS, Shadcn UI, Monaco Editor, Framer Motion, React Flow, Axios, WebSockets, Dark Mode
LLM: GROQ API with swappable model wrapper (Llama 3.x, DeepSeek, Qwen, Mixtral, Gemma)

## Languages

Python, SQL, Java, JavaScript, TypeScript, C++, Go, Bash, PySpark

## Personas (10)

Interview Preparation, Product Ready Engineer, Beginner Developer, Mid-Level Engineer, Senior Engineer, Principal Engineer, Competitive Programmer, Data Engineer, AI Engineer, Code Mentor

Each persona modifies: prompting, code style, documentation, complexity, review standards, explanation style, testing strategy.

## LangGraph Agents (13)

Implement each agent with: single responsibility, prompt template, typed input/output, error handling.

1. **Router Agent** — Detect language, intent, persona, ambiguity; route workflow → JSON output
2. **Requirement Extraction Agent** — Extract inputs, outputs, constraints, edge cases → structured JSON
3. **Persona Agent** — Load persona modifiers → persona_prompt_block for downstream agents
4. **Context Retrieval Agent** — FAISS + HuggingFace embeddings → relevant code snippets (optional)
5. **Language Specialist Agent** — Generate complete, runnable code in target language
6. **Optimization Agent** (MANDATORY) — Brute force → optimized → compare → select best → complexity analysis
7. **Code Review Agent** — Readability, performance, maintainability, standards → scored JSON review
8. **Security Review Agent** — SQL injection, secrets, unsafe code, input validation → security report JSON
9. **Unit Test Generator** — Pytest/JUnit/SQL tests with edge, negative, boundary cases
10. **Execution Agent** — Run code/tests via Python REPL; capture stdout/stderr/tracebacks
11. **Evaluator Agent** — PASS/FAIL, confidence score, improvement suggestions
12. **Explanation Agent** — Algorithm, complexity, trade-offs, alternatives (persona-adapted)
13. **Documentation Agent** — README, API docs, Mermaid diagrams, deployment guide

## Graph State (TypedDict/Pydantic)

```python
class CodeForgeState(TypedDict):
    request: str
    persona: str
    language: str
    router_output: dict
    requirements: dict
    persona_instructions: dict
    retrieved_context: dict
    generated_code: str
    optimized_code: str
    reviewed_code: str
    security_report: dict
    tests: str
    execution_result: dict
    evaluation: dict
    explanation: str
    documentation: dict
    agent_timeline: list
    errors: list
    current_agent: str
```

## LangGraph Workflow

```
START → router → requirement_extraction → persona → context_retrieval
  → language_specialist → optimization → code_review → security_review
  → unit_test_generator → execution → evaluator
  → [conditional: regenerate if FAIL] → explanation → documentation → END
```

Conditional edge after evaluator: if `should_regenerate` and loop_count < 2, route back to language_specialist or optimization.

## Prompt Templates

Use the prompt templates in `prompts/` directory:
- `prompts/system_prompt.md` — Base system prompt
- `prompts/router_agent.md` through `prompts/documentation_agent.md` — Per-agent templates
- `prompts/personas/persona_modifiers.md` — Persona injection blocks
- `prompts/llm_wrapper.md` — ChatGroq wrapper and model routing

## Backend API Endpoints

POST /chat (WebSocket streaming), POST /generate, POST /review, POST /test, POST /evaluate, GET /persona, GET /workflow, GET /models, GET /download/{artifact}

## Frontend Features

Dark mode, responsive layout, Monaco code editor, agent timeline, React Flow workflow visualization, Mermaid graphs, streaming responses, model/persona/language selectors, complexity dashboard, execution logs, copy/download buttons.

## Project Structure

```
codeforge-ai/
├── backend/
│   ├── agents/          # 13 agent implementations
│   ├── graph/           # LangGraph workflow + state
│   ├── prompts/         # Prompt template loaders
│   ├── models/          # Pydantic schemas
│   ├── tools/           # Python REPL, FAISS retriever
│   ├── config/          # Settings, model config
│   ├── services/        # LLM wrapper, orchestration
│   ├── api/             # FastAPI routes
│   └── utils/           # Logging, helpers
├── frontend/
│   └── src/
│       ├── components/  # UI components
│       ├── pages/       # Dashboard, workspace
│       ├── hooks/       # WebSocket, API hooks
│       └── lib/         # Axios, utils
├── tests/
├── docs/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Code Quality Requirements

- Type hints and docstrings on all Python code
- Logging and exception handling throughout
- Configuration via environment variables
- No duplicated logic — modular architecture
- No placeholders — complete implementations only
- Dependency injection for LLM provider and tools

## Build Phases

Phase 1: Architecture + state schema
Phase 2: Folder structure
Phase 3: Backend (FastAPI + services)
Phase 4: Frontend (React dashboard)
Phase 5: LangGraph workflow wiring all 13 agents
Phase 6: Prompt templates (DONE — see prompts/)
Phase 7: API endpoints + WebSocket streaming
Phase 8: Pytest unit + integration tests
Phase 9: README, architecture docs, Mermaid diagrams
Phase 10: 10-slide presentation with speaker notes

## Hackathon Differentiators

Emphasize: persona-driven AI, mandatory optimization agent, security review agent, live agent timeline, multi-language support, best complexity analysis, LangGraph orchestration, production architecture, auto testing/evaluation/documentation.

Start with Phase 1. Implement completely. Do not skip files. Do not use placeholders.
```

---

## Prompt File Index

| File | Agent / Purpose |
|------|-----------------|
| `prompts/system_prompt.md` | Base system prompt for all agents |
| `prompts/router_agent.md` | Agent 1 — Routing & classification |
| `prompts/requirement_extraction_agent.md` | Agent 2 — Structured requirements |
| `prompts/persona_agent.md` | Agent 3 — Persona instruction generation |
| `prompts/context_retrieval_agent.md` | Agent 4 — RAG context enrichment |
| `prompts/language_specialist_agent.md` | Agent 5 — Code generation |
| `prompts/optimization_agent.md` | Agent 6 — Algorithm optimization (mandatory) |
| `prompts/code_review_agent.md` | Agent 7 — PR-style code review |
| `prompts/security_review_agent.md` | Agent 8 — Security audit |
| `prompts/unit_test_generator_agent.md` | Agent 9 — Test suite generation |
| `prompts/execution_agent.md` | Agent 10 — Sandbox execution |
| `prompts/evaluator_agent.md` | Agent 11 — Quality gate PASS/FAIL |
| `prompts/explanation_agent.md` | Agent 12 — Algorithm explanation |
| `prompts/documentation_agent.md` | Agent 13 — README & docs generation |
| `prompts/personas/persona_modifiers.md` | 10 persona injection blocks |
| `prompts/llm_wrapper.md` | ChatGroq wrapper & model routing |

## LangGraph Edge Definitions

```python
# Conditional routing from Router
def route_by_intent(state):
    intent = state["router_output"]["intent"]
    if intent == "explain":
        return "explanation"
    if intent == "review":
        return "code_review"
    if intent == "document":
        return "documentation"
    return "requirement_extraction"

# Conditional routing from Evaluator
def route_after_evaluation(state):
    if state["evaluation"].get("should_regenerate") and state.get("loop_count", 0) < 2:
        return state["evaluation"].get("regenerate_agent", "language_specialist")
    return "explanation"
```

## Variable Injection Map

| Agent | Required Variables |
|-------|--------------------|
| Router | `user_request`, `persona_override`, `language_override` |
| Requirement Extraction | `user_request`, `router_output`, `language`, `persona` |
| Persona | `persona`, `requirements`, `user_request` |
| Context Retrieval | `user_request`, `requirements`, `language`, `retrieved_chunks` |
| Language Specialist | `requirements`, `language`, `persona_prompt_block`, `context_prompt_block` |
| Optimization | `requirements`, `language`, `persona_prompt_block`, `generated_code` |
| Code Review | `requirements`, `language`, `persona_prompt_block`, `optimized_code` |
| Security Review | `requirements`, `language`, `reviewed_code` |
| Unit Test Generator | `requirements`, `language`, `persona_prompt_block`, `sanitized_code` |
| Execution | `language`, `sanitized_code`, `tests` |
| Evaluator | `requirements`, `persona`, `optimized_code`, `review_feedback`, `security_report`, `execution_result` |
| Explanation | `user_request`, `requirements`, `persona_prompt_block`, `sanitized_code`, `optimization_output`, `evaluation` |
| Documentation | All final artifacts + `workflow` |

---

*Generated from master_prompt.md — CodeForge AI Hackathon Project*
