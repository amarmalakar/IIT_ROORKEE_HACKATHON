# CodeForge AI — Hackathon Presentation

## Slide 1: Problem Statement

**Title:** The Gap Between Natural Language and Production Code

- Developers spend hours translating requirements into code, tests, docs, and reviews
- Single-shot LLM code generators produce toy demos, not production-ready software
- No persona awareness, no optimization guarantees, no security review

**Speaker Notes:**
- Open with the pain point: "Ask ChatGPT for code and you get a snippet. Ask a senior engineer and you get architecture, tests, security review, and documentation."
- CodeForge AI bridges that gap with a full AI engineering team.

---

## Slide 2: Motivation

**Title:** Why an AI Software Engineering Team?

- Hackathon challenge: Natural Language → Code Generation
- Our insight: Don't build a code generator — build an engineering team
- 13 agents, each with single responsibility, mirroring real SDLC

**Speaker Notes:**
- Emphasize modularity and explainability as judge differentiators
- Each agent has a prompt template, typed I/O, and clear responsibility

---

## Slide 3: Architecture

**Title:** System Architecture

```
React Dashboard ↔ FastAPI ↔ LangGraph ↔ ChatGroq
                              ↕
                         FAISS + Python REPL
```

- Frontend: Monaco editor, agent timeline, React Flow visualization
- Backend: FastAPI REST API
- Orchestration: LangGraph with typed state

**Speaker Notes:**
- Walk through the three-tier architecture
- Highlight agent timeline populated from REST response

---

## Slide 4: Multi-Agent Workflow

**Title:** 13-Agent Pipeline

Router → Requirements → Persona → Context → Code Gen → **Optimization** → Review → **Security** → Tests → Execution → Evaluator → Explanation → Docs

- Conditional routing by intent (generate, review, explain)
- Evaluator regeneration loop (max 2 retries)

**Speaker Notes:**
- Demo the agent timeline in the UI
- Call out Optimization and Security as mandatory differentiators

---

## Slide 5: Personas

**Title:** 10 Developer Personas

| Persona | Output Style |
|---------|-------------|
| Interview Prep | Brute force → optimal + dry run |
| Product Ready | Enterprise architecture + logging |
| Competitive Programmer | Fastest algorithm, minimal code |
| Code Mentor | Teaching explanations |

**Speaker Notes:**
- Same request, different persona = different code style, tests, and explanations
- Persona prompt blocks injected into every downstream agent

---

## Slide 6: LangGraph

**Title:** LangGraph Orchestration

- `CodeForgeState` TypedDict with 20+ fields
- Conditional edges: intent routing + evaluator regeneration
- Agent timeline audit trail for explainability

**Speaker Notes:**
- Show the state machine diagram from architecture docs
- Explain typed state prevents data loss between agents

---

## Slide 7: Frontend Demo

**Title:** Live Dashboard Demo

- Persona / language / model selectors
- Monaco code editor with syntax highlighting
- Agent timeline with per-agent status after pipeline completes
- Complexity dashboard + execution logs

**Speaker Notes:**
- Live demo: "Write a two-sum function for FAANG interview prep"
- Show agent timeline and final optimized code after REST response

---

## Slide 8: Backend APIs

**Title:** REST API

- `POST /api/generate` — Full pipeline (primary)
- `POST /api/review`, `/test`, `/evaluate` — Targeted operations
- `GET /api/persona`, `/workflow`, `/models` — Metadata

**Speaker Notes:**
- API-first design enables CLI, IDE plugins, CI/CD integration
- Response includes full `state` with `agent_timeline` and `loop_count`

---

## Slide 9: Challenges & Solutions

**Title:** Engineering Challenges

| Challenge | Solution |
|-----------|----------|
| LLM output validation | Pydantic schemas + retry prompts |
| Non-deterministic routing | Router agent with confidence scores |
| Code execution safety | Subprocess sandbox, no network |
| Context retrieval without data | FAISS + keyword fallback |
| Regeneration loops | Evaluator gate with max 2 loops |

**Speaker Notes:**
- Be honest about trade-offs: only Python REPL for live execution
- FAISS is optional — workflow proceeds gracefully without index

---

## Slide 10: Future Scope

**Title:** What's Next

- Multi-language execution (JVM, Node.js sandboxes)
- Custom FAISS index from user's codebase (RAG)
- IDE plugin (VS Code / Cursor integration)
- CI/CD agent for GitHub Actions generation
- Fine-tuned models per agent role
- Collaborative multi-user sessions

**Speaker Notes:**
- End with the vision: "CodeForge AI is not a demo — it's a platform"
- Thank judges, open for questions
