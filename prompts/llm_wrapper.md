# CodeForge AI — LLM Wrapper Prompt

## Role

You are the **LLM Service Layer** for CodeForge AI. All agents invoke language models through this standardized wrapper. Prompts are assembled from agent templates + runtime context.

## Model Configuration

```python
# config/models.py — supported GROQ models
SUPPORTED_MODELS = {
    "llama-3.3-70b-versatile": {"provider": "groq", "max_tokens": 8192, "temperature": 0.2},
    "llama-3.1-8b-instant": {"provider": "groq", "max_tokens": 8192, "temperature": 0.1},
    "deepseek-r1-distill-llama-70b": {"provider": "groq", "max_tokens": 8192, "temperature": 0.3},
    "qwen-qwq-32b": {"provider": "groq", "max_tokens": 8192, "temperature": 0.2},
    "mixtral-8x7b-32768": {"provider": "groq", "max_tokens": 8192, "temperature": 0.2},
    "gemma2-9b-it": {"provider": "groq", "max_tokens": 8192, "temperature": 0.2},
}
```

## Agent-to-Model Routing

| Agent | Recommended Model | Temperature | Reason |
|-------|-------------------|-------------|--------|
| Router | llama-3.1-8b-instant | 0.1 | Fast classification |
| Requirement Extraction | llama-3.3-70b-versatile | 0.2 | Structured JSON accuracy |
| Persona | llama-3.1-8b-instant | 0.1 | Template lookup |
| Context Retrieval | N/A (embedding model) | — | HuggingFace embeddings |
| Language Specialist | llama-3.3-70b-versatile | 0.2 | Code quality |
| Optimization | deepseek-r1-distill-llama-70b | 0.3 | Reasoning for algorithms |
| Code Review | llama-3.3-70b-versatile | 0.2 | Thorough analysis |
| Security Review | llama-3.3-70b-versatile | 0.1 | Low hallucination tolerance |
| Unit Test Generator | llama-3.3-70b-versatile | 0.2 | Test completeness |
| Execution | N/A (Python REPL) | — | No LLM |
| Evaluator | qwen-qwq-32b | 0.2 | Reasoning for scoring |
| Explanation | llama-3.3-70b-versatile | 0.3 | Natural language quality |
| Documentation | llama-3.3-70b-versatile | 0.3 | Long-form generation |

## Prompt Assembly Template

Every agent invocation uses this message structure:

```python
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT + "\n\n" + AGENT_PROMPT_TEMPLATE
    },
    {
        "role": "user",
        "content": format_agent_input(
            user_request=user_request,
            persona_prompt_block=persona_prompt_block,
            requirements=requirements,
            # ... agent-specific variables
        )
    }
]
```

## System Message (Base)

```
You are an agent in the CodeForge AI multi-agent software engineering platform.
Agent Role: {agent_name}
Target Language: {language}
Active Persona: {persona}

Rules:
1. Stay within your agent's single responsibility.
2. Return output in the exact format specified in your agent prompt.
3. Never use placeholders or incomplete implementations.
4. If you cannot complete the task, return a structured error in the expected format.
5. For JSON outputs, return valid JSON only — no markdown fences.
```

## Streaming Configuration

For WebSocket `/chat` endpoint:

```python
async for chunk in llm.astream(messages):
    yield {
        "agent": agent_name,
        "chunk": chunk.content,
        "timestamp": datetime.utcnow().isoformat()
    }
```

## Error Retry Prompt

When an agent fails validation (invalid JSON, missing fields):

```
Your previous response failed validation.

Error: {validation_error}
Expected format: {expected_schema}

Please regenerate your response following the exact output format specified.
Previous response (truncated): {previous_response[:500]}
```

## Swappable Provider Interface

```python
class LLMProvider(Protocol):
    async def invoke(self, messages: list, model: str, **kwargs) -> str: ...
    async def astream(self, messages: list, model: str, **kwargs) -> AsyncIterator[str]: ...

class GroqProvider(LLMProvider):
    """ChatGroq implementation — swap for OpenAIProvider, AnthropicProvider, etc."""
    ...
```

## Environment Variables

```
GROQ_API_KEY=your_key_here
DEFAULT_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_TIMEOUT_SECONDS=60
LLM_MAX_RETRIES=3
```
