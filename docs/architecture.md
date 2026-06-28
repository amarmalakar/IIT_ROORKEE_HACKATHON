# CodeForge AI — Architecture

## System Overview

CodeForge AI is a persona-driven multi-agent software engineering platform. Natural language requests flow through a LangGraph workflow of 13 specialized agents, orchestrated by a FastAPI backend and visualized in a React dashboard.

```mermaid
flowchart TB
    subgraph frontend [React Frontend]
        UI[Dashboard]
        Monaco[Monaco Editor]
        Timeline[Agent Timeline]
        FlowViz[React Flow Graph]
        APIClient[REST Client]
    end

    subgraph api [FastAPI Backend]
        Routes["POST /api/generate"]
    end

    subgraph graph [LangGraph 13-Agent Workflow]
        R[Router]
        RE[RequirementExtraction]
        P[Persona]
        CR[ContextRetrieval]
        LS[LanguageSpecialist]
        O[Optimization]
        CRv[CodeReview]
        SR[SecurityReview]
        UT[UnitTestGenerator]
        EX[Execution]
        EV[Evaluator]
        EP[Explanation]
        DOC[Documentation]

        R --> RE
        RE --> P
        P --> CR
        CR --> LS
        LS --> O
        O --> CRv
        CRv --> SR
        SR --> UT
        UT --> EX
        EX --> EV
        EV --> EP
        EP --> DOC
        EV -->|"FAIL: loop_count less than 2"| LS
        EV -->|"perf fix"| O
    end

    subgraph services [Services Layer]
        LLM["GroqProvider llama-3.1-8b"]
        RateLimit[Rate Limiter]
        PromptLoader[Prompt Loader]
        FAISS[FAISS Retriever]
        REPL[Python REPL]
        EvalLogic[Deterministic Evaluator]
    end

    UI --> APIClient
    APIClient --> Routes
    Routes --> graph
    graph --> services
    CR --> FAISS
    EX --> REPL
    EV --> EvalLogic
    LLM --> RateLimit
```

## Regeneration Loop

When tests fail or execution errors, the **Evaluator** routes back to **Code Gen** (or **Optimization**) and re-runs the downstream pipeline. Maximum **2 regeneration attempts** (`loop_count < 2`).

```mermaid
flowchart LR
    subgraph attempt1 [Attempt 1]
        A1[Code Gen] --> A2[Optimize]
        A2 --> A3[Review]
        A3 --> A4[Security]
        A4 --> A5[Tests]
        A5 --> A6[Execute]
        A6 --> A7{Evaluator}
    end

    A7 -->|PASS| Explain[Explanation]
    A7 -->|FAIL loop 1| B1[Code Gen retry]
    B1 --> B2[Optimize]
    B2 --> B3[Review]
    B3 --> B4[Security]
    B4 --> B5[Tests]
    B5 --> B6[Execute]
    B6 --> B7{Evaluator}
    B7 -->|PASS| Explain
    B7 -->|FAIL max loops| Explain
    Explain --> Docs[Documentation]
    Docs --> EndNode[END]
```

## Request Lifecycle

```mermaid
sequenceDiagram
    participant User
    participant API as FastAPI
    participant Graph as LangGraph
    participant LLM as ChatGroq
    participant FAISS as FAISS Local
    participant REPL as Python REPL
    participant Eval as Evaluator Logic

    User->>API: POST /api/generate
    API->>Graph: invoke state
    Graph->>LLM: Router
    LLM-->>Graph: router_output JSON
    Graph->>LLM: Requirement Extraction
    Graph->>LLM: Persona
    Graph->>FAISS: Context Retrieval local
    FAISS-->>Graph: context snippets
    Graph->>LLM: Language Specialist
    Graph->>LLM: Optimization
    Graph->>LLM: Code Review
    Graph->>LLM: Security Review
    Graph->>LLM: Unit Test Generator
    Graph->>REPL: Execution sandbox
    REPL-->>Graph: test results stdout stderr
    Graph->>Eval: Deterministic PASS FAIL
    alt FAIL and loop_count less than 2
        Note over Graph,LLM: Regeneration with failure feedback
        Graph->>LLM: Language Specialist retry
        Graph->>LLM: Optimization through Security Tests
        Graph->>REPL: Re-execute tests
        Graph->>Eval: Re-evaluate
    end
    Graph->>LLM: Explanation
    Graph->>LLM: Documentation
    Graph-->>API: final state
    API-->>User: JSON response plus timeline
```

## State Machine

```mermaid
stateDiagram-v2
    [*] --> Router

    Router --> RequirementExtraction: full_pipeline generate
    Router --> CodeReview: review intent
    Router --> Explanation: explain intent
    Router --> Documentation: document or unsupported

    RequirementExtraction --> Persona
    Persona --> ContextRetrieval
    ContextRetrieval --> LanguageSpecialist
    LanguageSpecialist --> Optimization
    Optimization --> CodeReview
    CodeReview --> SecurityReview
    SecurityReview --> UnitTestGenerator
    UnitTestGenerator --> Execution
    Execution --> Evaluator

    Evaluator --> LanguageSpecialist: FAIL regenerate loop_count less than 2
    Evaluator --> Optimization: FAIL perf regenerate
    Evaluator --> Explanation: PASS or max loops reached

    Explanation --> Documentation
    Documentation --> [*]
```

## LLM vs Local Agents

Not every agent calls Groq. This reduces rate-limit pressure and speeds up the pipeline.

```mermaid
flowchart LR
    subgraph llmAgents [Groq LLM Agents]
        R1[Router]
        R2[Requirements]
        R3[Persona]
        R4[Code Gen]
        R5[Optimization]
        R6[Review]
        R7[Security]
        R8[Tests]
        R9[Explanation]
        R10[Documentation]
    end

    subgraph localAgents [Local No LLM]
        L1[Context Retrieval FAISS]
        L2[Execution REPL]
        L3[Evaluator Rules]
    end
```

## Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `backend/graph/workflow.py` | LangGraph StateGraph, intent routing, regeneration loop |
| `backend/agents/` | 13 agent node implementations |
| `backend/services/evaluation.py` | Deterministic PASS/FAIL and `should_regenerate` |
| `backend/services/rate_limiter.py` | Throttle Groq calls to prevent 429 errors |
| `backend/services/llm.py` | Groq provider with per-agent model routing |
| `backend/prompts/loader.py` | Load and inject Markdown prompt templates |
| `backend/tools/repl.py` | Sandboxed Python execution |
| `backend/tools/retriever.py` | FAISS vector retrieval |
| `backend/api/` | FastAPI REST endpoints |
| `frontend/` | React dashboard with Monaco, timeline, React Flow |

## Graph State Fields

| Field | Set By | Description |
|-------|--------|-------------|
| `request` | Initial | User natural language input |
| `router_output` | Router | Language, intent, persona, workflow |
| `requirements` | Requirement Extraction | Structured JSON requirements |
| `persona_instructions` | Persona | Persona prompt block for downstream agents |
| `retrieved_context` | Context Retrieval | FAISS snippets formatted locally |
| `generated_code` | Language Specialist | Initial code generation |
| `optimized_code` | Optimization | Best solution after comparison |
| `reviewed_code` | Code Review | Code with review fixes applied |
| `security_report` | Security Review | Security audit findings |
| `tests` | Unit Test Generator | Generated test suite |
| `execution_result` | Execution | stdout/stderr/test results |
| `evaluation` | Evaluator | PASS/FAIL, `should_regenerate`, `regenerate_agent` |
| `loop_count` | Evaluator | Regeneration attempt counter max 2 |
| `explanation` | Explanation | Algorithm walkthrough |
| `documentation` | Documentation | README, API docs, diagrams |
| `agent_timeline` | All agents | Audit trail for UI timeline |

## Rate Limiting

Groq free tier enforces request limits. CodeForge throttles calls via `LLM_REQUEST_DELAY_MS` (default 1200ms) and uses `llama-3.1-8b-instant` for all agents to stay within limits.
