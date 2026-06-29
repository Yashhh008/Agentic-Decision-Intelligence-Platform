"""
ADIP — Application Settings

All configuration is loaded from environment variables.
Never hardcode values; always use this module.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Platform-wide configuration loaded from .env"""

    # ── LLM ─────────────────────────────────────────────────────────────────
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.1-flash-lite"
    llm_max_retries: int = 3
    llm_timeout_seconds: int = 60

    # ── Embeddings ───────────────────────────────────────────────────────────
    embedding_model: str = "all-MiniLM-L6-v2"
    faiss_index_path: str = "backend/vectorstore/index/adip.index"
    faiss_metadata_path: str = "backend/vectorstore/index/metadata.json"
    knowledge_base_path: str = "backend/knowledge/enterprise"
    chunk_size: int = 500
    chunk_overlap: int = 50
    retrieval_top_k: int = 5

    # ── Database ─────────────────────────────────────────────────────────────
    database_url: str = "sqlite:///./backend/memory/adip.db"

    # ── API ──────────────────────────────────────────────────────────────────
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:5174",
        "https://*.vercel.app",
        "*",  # Allow all origins for hackathon demo
    ]
    debug: bool = True

    # ── Memory ───────────────────────────────────────────────────────────────
    memory_max_records: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
