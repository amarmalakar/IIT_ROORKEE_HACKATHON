# CodeForge AI — API Reference

Base URL: `http://localhost:8000`

## Health

### `GET /health`

Returns service health status.

```json
{"status": "healthy", "service": "CodeForge AI"}
```

---

## Code Generation

### `POST /api/generate`

Run the full 13-agent pipeline.

**Request Body:**

```json
{
  "request": "Write a Python function to reverse a linked list",
  "persona": "interview_preparation",
  "language": "python",
  "model": ""
}
```

**Response:**

```json
{
  "success": true,
  "state": {
    "generated_code": "...",
    "optimized_code": "...",
    "explanation": "...",
    "evaluation": {"verdict": "PASS", "confidence_score": 0.91},
    "agent_timeline": [...]
  },
  "message": "Pipeline completed"
}
```

**Response fields in `state`:**

- `agent_timeline` — per-agent status, summary, duration
- `loop_count` — evaluator regeneration loops
- `errors` — agent-level failures (if any)

---

## Code Review

### `POST /api/review`

Run code review + security review on provided code.

**Request Body:**

```json
{
  "request": "Review this sorting function",
  "code": "def sort_arr(arr): return sorted(arr)",
  "language": "python",
  "persona": "senior_engineer"
}
```

---

## Test Generation

### `POST /api/test`

Generate tests and execute code.

**Request Body:**

```json
{
  "request": "Test the add function",
  "code": "def add(a, b): return a + b",
  "language": "python"
}
```

---

## Evaluation

### `POST /api/evaluate`

Evaluate code quality (PASS/FAIL gate).

**Request Body:**

```json
{
  "code": "def add(a, b): return a + b",
  "tests": "def test_add(): assert add(1,2)==3",
  "language": "python"
}
```

---

## Metadata

### `GET /api/persona`

Returns list of 10 developer personas.

### `GET /api/languages`

Returns 9 supported languages.

### `GET /api/models`

Returns available Groq models with config.

### `GET /api/workflow`

Returns React Flow node/edge definitions.

---

## Download

### `POST /api/download/state`

Download artifact from completed workflow state.

```json
{
  "artifact": "code",
  "state": { "optimized_code": "..." }
}
```

Artifacts: `code`, `tests`, `readme`, `explanation`
