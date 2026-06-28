"""Groq API rate limiting to prevent 429 Too Many Requests."""

from __future__ import annotations

import asyncio
import logging
import time

from backend.config.settings import get_settings

logger = logging.getLogger("codeforge.ratelimit")

_lock = asyncio.Lock()
_last_request_at = 0.0


async def throttle_before_request() -> None:
    """Enforce minimum spacing between Groq API calls."""
    settings = get_settings()
    delay_s = settings.llm_request_delay_ms / 1000.0
    global _last_request_at
    async with _lock:
        now = time.monotonic()
        wait = delay_s - (now - _last_request_at)
        if wait > 0:
            logger.debug("Throttling Groq request for %.2fs", wait)
            await asyncio.sleep(wait)
        _last_request_at = time.monotonic()


async def backoff_on_rate_limit(attempt: int) -> None:
    """Exponential backoff after a 429 rate-limit response."""
    settings = get_settings()
    base = settings.llm_rate_limit_backoff_seconds
    wait = min(base * (2 ** attempt), 30.0)
    logger.warning("Groq rate limit hit — backing off %.1fs (attempt %d)", wait, attempt + 1)
    await asyncio.sleep(wait)


def is_rate_limit_error(exc: BaseException) -> bool:
    msg = str(exc).lower()
    return "429" in msg or "too many requests" in msg or "rate limit" in msg
