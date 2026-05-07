"""Operaciones core usadas por CLI y FastAPI."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from rag_tnm.catalog_loader import load_catalog_dir
from rag_tnm.config import get_settings
from rag_tnm.ollama_client import ollama_chat
from rag_tnm.prompts import (
    OLLAMA_SQL_SYSTEM,
    build_ollama_user_message,
    build_text_to_sql_prompt,
    format_retrieved_chunks,
)
from rag_tnm.sql_exec import DwConnectionParams, connect_dw, extract_sql_from_text, run_select
from rag_tnm.vector_store import get_client, get_or_create_collection, ingest_chunks, query_context, reset_collection


def chroma_collection():
    s = get_settings()
    client = get_client(str(s.rag_chroma_path))
    return get_or_create_collection(client, s.rag_collection_name)


def run_ingest(*, reset: bool = False, catalog_dir: Path | None = None) -> dict[str, Any]:
    s = get_settings()
    catalog = catalog_dir if catalog_dir else s.rag_catalog_dir
    catalog = Path(catalog)
    if not catalog.is_dir():
        raise FileNotFoundError(f"No existe catalogo: {catalog}")
    chunks = load_catalog_dir(catalog)
    if not chunks:
        raise ValueError(f"Sin YAML/MD en {catalog}")

    client = get_client(str(s.rag_chroma_path))
    if reset:
        col = reset_collection(client, s.rag_collection_name)
    else:
        col = get_or_create_collection(client, s.rag_collection_name)
    n = ingest_chunks(col, chunks)
    return {"indexed": n, "collection": s.rag_collection_name, "chroma_path": str(s.rag_chroma_path)}


def run_search(question: str, k: int = 8) -> list[dict[str, Any]]:
    col = chroma_collection()
    docs, metas = query_context(col, question, n_results=k)
    out = []
    for doc, meta in zip(docs, metas):
        out.append(
            {
                "title": meta.get("title", ""),
                "source_file": meta.get("source_file", ""),
                "text": doc,
            }
        )
    return out


def run_context(question: str, k: int = 8) -> dict[str, str]:
    col = chroma_collection()
    docs, metas = query_context(col, question, n_results=k)
    block = format_retrieved_chunks(docs, metas)
    prompt = build_text_to_sql_prompt(block, question)
    return {"prompt": prompt}


@dataclass
class AskOutcome:
    ok: bool
    sql: str | None = None
    columns: list[str] | None = None
    rows: list[tuple[Any, ...]] | None = None
    llm_raw: str | None = None
    error: str | None = None


def run_ask(
    question: str,
    *,
    k: int = 8,
    dry_run: bool = False,
    max_rows: int = 500,
) -> AskOutcome:
    s = get_settings()
    col = chroma_collection()
    docs, metas = query_context(col, question, n_results=k)
    block = format_retrieved_chunks(docs, metas)
    user_msg = build_ollama_user_message(block, question)

    try:
        raw = ollama_chat(
            s.ollama_base_url,
            s.ollama_model,
            OLLAMA_SQL_SYSTEM,
            user_msg,
            num_ctx=s.ollama_num_ctx,
            temperature=0.05,
            timeout_s=s.ollama_timeout_s,
        )
    except httpx.ConnectError as e:
        return AskOutcome(False, llm_raw=None, error=f"Ollama no disponible ({s.ollama_base_url}): {e}")
    except httpx.HTTPStatusError as e:
        return AskOutcome(False, error=f"Ollama HTTP {e.response.status_code}: {e.response.text}")
    except Exception as e:
        return AskOutcome(False, error=f"Error Ollama: {e}")

    sql = extract_sql_from_text(raw)
    if not sql:
        return AskOutcome(False, llm_raw=raw, error="No se extrajo SQL del modelo")

    if dry_run:
        return AskOutcome(True, sql=sql, llm_raw=raw)

    need = ("DEST_DB_HOST", s.dest_db_host), ("DEST_DB_NAME", s.dest_db_name), ("DEST_DB_USER", s.dest_db_user), ("DEST_DB_PASSWORD", s.dest_db_password)
    missing = [k for k, v in need if not v]
    if missing:
        return AskOutcome(
            False,
            sql=sql,
            llm_raw=raw,
            error=f"Faltan credenciales DEST_DB_*: {missing}. Configure .env en rag_tnm o datawarehouse_tnm.",
        )

    port = int(s.dest_db_port or "5432")
    params = DwConnectionParams(
        host=s.dest_db_host or "",
        port=port,
        dbname=s.dest_db_name or "",
        user=s.dest_db_user or "",
        password=s.dest_db_password or "",
    )
    conn = None
    try:
        conn = connect_dw(params)
        cols, rows = run_select(conn, sql, max_rows=max_rows)
        return AskOutcome(True, sql=sql, columns=cols, rows=rows, llm_raw=raw)
    except ValueError as e:
        return AskOutcome(False, sql=sql, llm_raw=raw, error=f"SQL rechazado: {e}")
    except Exception as e:
        return AskOutcome(False, sql=sql, llm_raw=raw, error=f"DB: {e}")
    finally:
        if conn is not None:
            conn.close()
