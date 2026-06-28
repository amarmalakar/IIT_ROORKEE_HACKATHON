# CodeForge AI — Deployment Guide

## Local Development

### 1. Clone and configure

```bash
git clone <repo-url>
cd IITR_hackathon
cp .env.example .env
```

Edit `.env` and set your `GROQ_API_KEY`.

### 2. Backend

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Access the dashboard at `http://localhost:5173`.

---

## Docker Compose

```bash
cp .env.example .env
# Set GROQ_API_KEY in .env

docker-compose up --build
```

| Service | Port |
|---------|------|
| Backend | 8000 |
| Frontend | 5173 |

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | Yes | — | Groq API key |
| `DEFAULT_MODEL` | No | `llama-3.3-70b-versatile` | Default LLM |
| `EMBEDDING_MODEL` | No | `sentence-transformers/all-MiniLM-L6-v2` | FAISS embeddings |
| `LLM_TIMEOUT_SECONDS` | No | `60` | Request timeout |
| `LLM_MAX_RETRIES` | No | `3` | Retry count |
| `CORS_ORIGINS` | No | `http://localhost:5173` | Allowed origins |
| `FAISS_INDEX_PATH` | No | `data/faiss_index` | Vector index path |
| `LOG_LEVEL` | No | `INFO` | Logging level |

---

## Production Considerations

1. **API Key Security** — Never commit `.env`. Use secrets manager in production.
2. **CORS** — Update `CORS_ORIGINS` to your production frontend URL.
3. **Rate Limiting** — Add rate limiting middleware for public deployments.
4. **Execution Sandbox** — Python REPL runs in subprocess; consider container isolation for production.
5. **FAISS Index** — Pre-build and mount the index volume for faster context retrieval.
6. **Frontend Build** — Run `npm run build` and serve static files via nginx or CDN.

### Production Frontend Build

```bash
cd frontend
npm run build
# Serve dist/ with nginx or integrate into FastAPI static files
```

### Production Backend

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Health Check

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"healthy","service":"CodeForge AI"}`
