from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _env_file_paths() -> tuple[str, ...]:
    paths: list[Path] = [_repo_root() / ".env"]
    sibling_dw = _repo_root().parent / "datawarehouse_tnm"
    sibling_env = sibling_dw / ".env"
    if sibling_env.is_file():
        paths.append(str(sibling_env))
    return tuple(str(p) for p in paths)


def _datawarehouse_root() -> Path:
    sibling = _repo_root().parent / "datawarehouse_tnm"
    if sibling.is_dir():
        return sibling
    return _repo_root().parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_env_file_paths(),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    rag_catalog_dir: Path = _repo_root() / "data" / "catalog"
    rag_chroma_path: Path = _repo_root() / "data" / "chroma"
    rag_collection_name: str = "dw_catalog"

    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "gemma3:4b"
    ollama_num_ctx: int = 8192
    ollama_timeout_s: float = 180.0

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    dest_db_host: str | None = None
    dest_db_port: str = "5432"
    dest_db_name: str | None = None
    dest_db_user: str | None = None
    dest_db_password: str | None = None

    @computed_field
    @property
    def datawarehouse_root(self) -> Path:
        return _datawarehouse_root()


def get_settings() -> Settings:
    return Settings()
