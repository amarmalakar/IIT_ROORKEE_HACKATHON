"""LLM service layer with swappable provider."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import AsyncIterator, Protocol

from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from backend.config.settings import AGENT_MODEL_ROUTING, SUPPORTED_MODELS, get_settings
from backend.prompts.loader import get_prompt_loader
from backend.utils.helpers import truncate_text


class LLMProvider(Protocol):
    async def invoke(self, messages: list[dict[str, str]], model: str, **kwargs: object) -> str: ...
    async def astream(self, messages: list[dict[str, str]], model: str, **kwargs: object) -> AsyncIterator[str]: ...


def _to_lc_messages(messages: list[dict[str, str]]) -> list:
    result = []
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "system":
            result.append(SystemMessage(content=content))
        elif role == "user":
            result.append(HumanMessage(content=content))
        else:
            result.append(AIMessage(content=content))
    return result


class GroqProvider:
    """ChatGroq implementation — swap for other providers via LLMProvider protocol."""

    def __init__(self, api_key: str | None = None) -> None:
        settings = get_settings()
        self.api_key = api_key or settings.groq_api_key
        self.default_model = settings.default_model
        self.max_retries = settings.llm_max_retries
        self._clients: dict[str, ChatGroq] = {}

    def _get_client(self, model: str, temperature: float) -> ChatGroq:
        key = f"{model}:{temperature}"
        if key not in self._clients:
            self._clients[key] = ChatGroq(
                api_key=self.api_key,
                model=model,
                temperature=temperature,
                max_retries=self.max_retries,
            )
        return self._clients[key]

    async def invoke(self, messages: list[dict[str, str]], model: str = "", temperature: float = 0.2) -> str:
        model = model or self.default_model
        client = self._get_client(model, temperature)
        lc_messages = _to_lc_messages(messages)
        response = await asyncio.to_thread(client.invoke, lc_messages)
        return str(response.content)

    async def astream(
        self, messages: list[dict[str, str]], model: str = "", temperature: float = 0.2
    ) -> AsyncIterator[str]:
        model = model or self.default_model
        client = self._get_client(model, temperature)
        lc_messages = _to_lc_messages(messages)
        async for chunk in client.astream(lc_messages):
            if chunk.content:
                yield str(chunk.content)


class LLMService:
    """High-level LLM service with per-agent routing and retry logic."""

    def __init__(self, provider: GroqProvider | None = None) -> None:
        self.provider = provider or GroqProvider()
        self.prompt_loader = get_prompt_loader()

    def get_agent_config(self, agent_name: str, model_override: str = "") -> dict[str, object]:
        routing = AGENT_MODEL_ROUTING.get(agent_name, {})
        model = model_override or str(routing.get("model", get_settings().default_model))
        temperature = float(routing.get("temperature", 0.2))
        return {"model": model, "temperature": temperature}

    async def invoke_agent(
        self,
        agent_name: str,
        variables: dict[str, object],
        language: str = "",
        persona: str = "",
        model_override: str = "",
    ) -> str:
        messages = self.prompt_loader.build_messages(agent_name, variables, language, persona)
        config = self.get_agent_config(agent_name, model_override)
        return await self.provider.invoke(
            messages,
            model=str(config["model"]),
            temperature=float(config["temperature"]),
        )

    async def stream_agent(
        self,
        agent_name: str,
        variables: dict[str, object],
        language: str = "",
        persona: str = "",
        model_override: str = "",
    ) -> AsyncIterator[dict[str, str]]:
        messages = self.prompt_loader.build_messages(agent_name, variables, language, persona)
        config = self.get_agent_config(agent_name, model_override)
        async for chunk in self.provider.astream(
            messages,
            model=str(config["model"]),
            temperature=float(config["temperature"]),
        ):
            yield {
                "agent": agent_name,
                "chunk": chunk,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    async def invoke_with_retry(
        self,
        agent_name: str,
        variables: dict[str, object],
        language: str = "",
        persona: str = "",
        model_override: str = "",
    ) -> str:
        last_error = ""
        response = ""
        for attempt in range(self.provider.max_retries):
            try:
                if attempt == 0:
                    response = await self.invoke_agent(
                        agent_name, variables, language, persona, model_override
                    )
                else:
                    retry_msg = self.prompt_loader.build_retry_message(
                        last_error, f"Valid output for {agent_name}", response
                    )
                    messages = self.prompt_loader.build_messages(
                        agent_name, variables, language, persona
                    )
                    messages.append({"role": "user", "content": retry_msg})
                    config = self.get_agent_config(agent_name, model_override)
                    response = await self.provider.invoke(
                        messages,
                        model=str(config["model"]),
                        temperature=float(config["temperature"]),
                    )
                return truncate_text(response, 50000)
            except Exception as exc:
                last_error = str(exc)
                if attempt == self.provider.max_retries - 1:
                    raise
        return response


_llm_service: LLMService | None = None


def get_llm_service() -> LLMService:
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service


def list_models() -> list[dict[str, object]]:
    return [
        {"id": model_id, **config}
        for model_id, config in SUPPORTED_MODELS.items()
    ]
