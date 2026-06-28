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
        Routes[REST API]
    end

    subgraph graph [LangGraph Workflow]
        R[Router] --> RE[RequirementExtraction]
        RE --> P[Persona]
        P --> CR[ContextRetrieval]
        CR --> LS[LanguageSpecialist]
        LS --> O[Optimization]
        O --> CRv[CodeReview]
        CRv --> SR[SecurityReview]
        SR --> UT[UnitTestGenerator]
        UT --> EX[Execution]
        EX --> EV[Evaluator]
        EV --> EP[Explanation]
        EP --> DOC[Documentation]
    end

    subgraph services [Services]
        LLM[GroqProvider]
        PromptLoader[Prompt Loader]
        FAISS[FAISS Retriever]
        REPL[Python REPL]
    end

    UI --> APIClient
    APIClient --> Routes
    Routes --> graph
    graph --> services
```

## Request Lifecycle

```mermaid
sequenceDiagram
    participant User
    participant API as FastAPI
    participant Graph as LangGraph
    participant LLM as ChatGroq
    participant Tools as REPL_FAISS

    User->>API: POST /api/generate
    API->>Graph: invoke(state)
    Graph->>LLM: Router Agent
    LLM-->>Graph: router_output
    Graph->>LLM: Requirement Extraction
    Graph->>LLM: Persona Agent
    Graph->>Tools: FAISS retrieval
    Graph->>LLM: Language Specialist
    Graph->>LLM: Optimization
    Graph->>LLM: Code Review + Security
    Graph->>LLM: Unit Test Generator
    Graph->>Tools: Execution Agent
    Graph->>LLM: Evaluator
    alt FAIL and loop_count less than 2
        Graph->>LLM: Regenerate
    end
    Graph->>LLM: Explanation + Documentation
    Graph-->>API: final state
    API-->>User: stream chunks + timeline
```

## State Machine

```mermaid
stateDiagram-v2
    [*] --> Router
    Router --> RequirementExtraction: full_pipeline / generate
    Router --> CodeReview: review
    Router --> Explanation: explain
    Router --> Documentation: document
    RequirementExtraction --> Persona
    Persona --> ContextRetrieval
    ContextRetrieval --> LanguageSpecialist
    LanguageSpecialist --> Optimization
    Optimization --> CodeReview
    CodeReview --> SecurityReview
    SecurityReview --> UnitTestGenerator
    UnitTestGenerator --> Execution
    Execution --> Evaluator
    Evaluator --> LanguageSpecialist: FAIL regenerate
    Evaluator --> Explanation: PASS or max loops
    Explanation --> Documentation
    Documentation --> [*]
```

## Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `backend/graph/workflow.py` | LangGraph StateGraph compilation and conditional edges |
| `backend/agents/` | 13 agent node implementations |
| `backend/prompts/loader.py` | Load and inject Markdown prompt templates |
| `backend/services/llm.py` | Groq LLM provider with per-agent model routing |
| `backend/tools/repl.py` | Sandboxed Python execution |
| `backend/tools/retriever.py` | FAISS vector retrieval (optional) |
| `backend/api/` | FastAPI REST endpoints |
| `frontend/` | React dashboard with Monaco, timeline, React Flow |

## Graph State Fields

| Field | Set By | Description |
|-------|--------|-------------|
| `request` | Initial | User natural language input |
| `router_output` | Router | Language, intent, persona, workflow |
| `requirements` | Requirement Extraction | Structured JSON requirements |
| `persona_instructions` | Persona | Persona prompt block for downstream agents |
| `retrieved_context` | Context Retrieval | FAISS snippets (optional) |
| `generated_code` | Language Specialist | Initial code generation |
| `optimized_code` | Optimization | Best solution after comparison |
| `reviewed_code` | Code Review | Code with review fixes applied |
| `security_report` | Security Review | Security audit findings |
| `tests` | Unit Test Generator | Generated test suite |
| `execution_result` | Execution | stdout/stderr/test results |
| `evaluation` | Evaluator | PASS/FAIL with confidence score |
| `explanation` | Explanation | Algorithm walkthrough |
| `documentation` | Documentation | README, API docs, diagrams |
| `agent_timeline` | All agents | Audit trail for UI timeline |
