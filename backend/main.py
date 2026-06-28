"""CodeForge AI — FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import router
from backend.config.settings import get_settings
from backend.utils.helpers import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    setup_logging(settings.log_level)
    if not settings.groq_api_key or settings.groq_api_key == "your_groq_api_key_here":
        import logging

        logging.getLogger("codeforge").warning(
            "GROQ_API_KEY is not set. LLM agents will fail. "
            "Add it to backend/.env or project root .env"
        )
    yield


app = FastAPI(
    title="CodeForge AI",
    description="Persona-Driven Multi-Agent Software Engineering Platform",
    version="1.0.0",
    lifespan=lifespan,
)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api", tags=["codeforge"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "CodeForge AI"}
