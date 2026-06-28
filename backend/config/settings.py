"""Application configuration via environment variables."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROMPTS_DIR = PROJECT_ROOT / "prompts"


class Settings(BaseSettings):
    """CodeForge AI application settings."""

    model_config = SettingsConfigDict(
        env_file=(
            str(PROJECT_ROOT / ".env"),
            str(PROJECT_ROOT / "backend" / ".env"),
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    groq_api_key: str = ""
    default_model: str = "llama-3.3-70b-versatile"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_timeout_seconds: int = 60
    llm_max_retries: int = 2
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    cors_origins: str = (
        "http://localhost:5173,http://localhost:5174,http://localhost:5175,"
        "http://localhost:3000"
    )
    faiss_index_path: str = "data/faiss_index"
    enable_semantic_search: bool = False
    log_level: str = "INFO"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


SUPPORTED_MODELS: dict[str, dict[str, object]] = {
    "llama-3.3-70b-versatile": {"provider": "groq", "max_tokens": 8192, "temperature": 0.2},
    "llama-3.1-8b-instant": {"provider": "groq", "max_tokens": 8192, "temperature": 0.1},
    "deepseek-r1-distill-llama-70b": {"provider": "groq", "max_tokens": 8192, "temperature": 0.3},
    "qwen-qwq-32b": {"provider": "groq", "max_tokens": 8192, "temperature": 0.2},
    "mixtral-8x7b-32768": {"provider": "groq", "max_tokens": 8192, "temperature": 0.2},
    "gemma2-9b-it": {"provider": "groq", "max_tokens": 8192, "temperature": 0.2},
}

AGENT_MODEL_ROUTING: dict[str, dict[str, object]] = {
    "router": {"model": "llama-3.1-8b-instant", "temperature": 0.1},
    "requirement_extraction": {"model": "llama-3.1-8b-instant", "temperature": 0.1},
    "persona": {"model": "llama-3.1-8b-instant", "temperature": 0.1},
    "context_retrieval": {"model": "llama-3.1-8b-instant", "temperature": 0.1},
    "language_specialist": {"model": "llama-3.3-70b-versatile", "temperature": 0.2},
    "optimization": {"model": "llama-3.3-70b-versatile", "temperature": 0.2},
    "code_review": {"model": "llama-3.1-8b-instant", "temperature": 0.1},
    "security_review": {"model": "llama-3.1-8b-instant", "temperature": 0.1},
    "unit_test_generator": {"model": "llama-3.1-8b-instant", "temperature": 0.2},
    "evaluator": {"model": "llama-3.1-8b-instant", "temperature": 0.1},
    "explanation": {"model": "llama-3.1-8b-instant", "temperature": 0.2},
    "documentation": {"model": "llama-3.1-8b-instant", "temperature": 0.2},
}

PERSONAS: list[dict[str, str]] = [
    {"id": "interview_preparation", "name": "Interview Preparation", "description": "Brute force to optimal with dry runs and complexity analysis"},
    {"id": "product_ready_engineer", "name": "Product Ready Engineer", "description": "Enterprise architecture, logging, SOLID, security"},
    {"id": "beginner_developer", "name": "Beginner Developer", "description": "Simple code with step-by-step explanations"},
    {"id": "mid_level_engineer", "name": "Mid-Level Engineer", "description": "Clean code, type hints, unit tests"},
    {"id": "senior_engineer", "name": "Senior Engineer", "description": "Design patterns, maintainability, performance"},
    {"id": "principal_engineer", "name": "Principal Engineer", "description": "Extensible distributed architecture"},
    {"id": "competitive_programmer", "name": "Competitive Programmer", "description": "Fastest algorithm, minimal memory"},
    {"id": "data_engineer", "name": "Data Engineer", "description": "SQL, PySpark, ETL pipelines"},
    {"id": "ai_engineer", "name": "AI Engineer", "description": "LangChain, RAG, LLM integrations"},
    {"id": "code_mentor", "name": "Code Mentor", "description": "Teaching explanations and practice questions"},
]

LANGUAGES: list[dict[str, str]] = [
    {"id": "python", "name": "Python"},
    {"id": "sql", "name": "SQL"},
    {"id": "java", "name": "Java"},
    {"id": "javascript", "name": "JavaScript"},
    {"id": "typescript", "name": "TypeScript"},
    {"id": "cpp", "name": "C++"},
    {"id": "go", "name": "Go"},
    {"id": "bash", "name": "Bash"},
    {"id": "pyspark", "name": "PySpark"},
]

WORKFLOW_NODES: list[dict[str, object]] = [
    {"id": "router", "label": "Router", "position": {"x": 0, "y": 0}},
    {"id": "requirement_extraction", "label": "Requirements", "position": {"x": 250, "y": 0}},
    {"id": "persona", "label": "Persona", "position": {"x": 500, "y": 0}},
    {"id": "language_specialist", "label": "Code Gen", "position": {"x": 750, "y": 0}},
    {"id": "code_review", "label": "Review", "position": {"x": 1000, "y": 0}},
    {"id": "execution", "label": "Execution", "position": {"x": 1250, "y": 0}},
    {"id": "explanation", "label": "Explanation", "position": {"x": 1500, "y": 0}},
]

WORKFLOW_EDGES: list[dict[str, str]] = [
    {"source": "router", "target": "requirement_extraction"},
    {"source": "requirement_extraction", "target": "persona"},
    {"source": "persona", "target": "language_specialist"},
    {"source": "language_specialist", "target": "code_review"},
    {"source": "code_review", "target": "execution"},
    {"source": "execution", "target": "explanation"},
]


@lru_cache
def get_settings() -> Settings:
    return Settings()
