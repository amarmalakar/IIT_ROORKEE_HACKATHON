# CodeForge AI

**Persona-Driven Multi-Agent Software Engineering Platform** — converts natural language into production-quality code using 13 collaborating AI agents orchestrated by LangGraph.

## Features

- 13 specialized LangGraph agents (router → requirements → persona → retrieval → codegen → optimization → review → security → tests → execution → evaluation → explanation → docs)
- 10 developer personas (Interview Prep, Product Ready, Beginner, Senior, etc.)
- 9 programming languages (Python, SQL, Java, TypeScript, Go, PySpark, and more)
- Mandatory optimization agent with complexity analysis
- Dedicated security review agent
- Agent timeline and React Flow workflow visualization
- REST API for full pipeline generation
- Monaco code editor with copy/download

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| Backend | Python, FastAPI, LangGraph, LangChain, ChatGroq |
| Frontend | React, TypeScript, TailwindCSS, Monaco, React Flow |
| Vector Store | FAISS + HuggingFace Embeddings |
| Execution | Python REPL sandbox |

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- GROQ API key ([console.groq.com](https://console.groq.com))

### Backend

```bash
cp .env.example backend/.env
# Edit backend/.env and set GROQ_API_KEY

pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

### Docker

```bash
cp .env.example .env
docker-compose up --build
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/generate` | Full pipeline (primary) |
| POST | `/api/review` | Code + security review |
| POST | `/api/test` | Generate and run tests |
| POST | `/api/evaluate` | Quality gate evaluation |
| GET | `/api/persona` | List personas |
| GET | `/api/workflow` | Graph definition for UI |
| GET | `/api/models` | Available Groq models |
| GET | `/api/download/{artifact}` | Download code/tests/README |

## Project Structure

```
IITR_hackathon/
├── backend/
│   ├── agents/       # 13 LangGraph agent nodes
│   ├── graph/        # Workflow + conditional edges
│   ├── prompts/      # Template loader
│   ├── models/       # Pydantic schemas + state
│   ├── tools/        # REPL + FAISS retriever
│   ├── services/     # Groq LLM wrapper
│   └── api/          # FastAPI REST routes
├── frontend/         # React dashboard
├── prompts/          # Agent prompt templates (Phase 6)
├── tests/            # Pytest suite
└── docs/             # Architecture + API docs
```

## Environment Variables

See [`.env.example`](.env.example):

- `GROQ_API_KEY` — Required for LLM calls
- `DEFAULT_MODEL` — Default Groq model
- `EMBEDDING_MODEL` — HuggingFace embedding model for FAISS

## Running Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for full Mermaid diagrams including:

- 13-agent system overview with regeneration loop
- Sequence diagram (LLM vs local agents)
- State machine with conditional routing
- Rate limiting strategy

## License

MIT — Built for IITR AI Hackathon
