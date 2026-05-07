"""API HTTP (FastAPI) para RAG TNM."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel, Field

from rag_tnm.runner import AskOutcome, run_ask, run_context, run_ingest, run_search


class QuestionPayload(BaseModel):
    question: str = Field(..., min_length=1)
    k: int = Field(8, ge=1, le=50)


class IngestPayload(BaseModel):
    reset: bool = False
    catalog_dir: str | None = None


class AskPayload(BaseModel):
    question: str = Field(..., min_length=1)
    k: int = Field(8, ge=1, le=50)
    dry_run: bool = False
    max_rows: int = Field(500, ge=1, le=5000)


def create_app() -> FastAPI:
    app = FastAPI(title="RAG TNM", version="0.1.0", description="RAG + Text-to-SQL sobre catálogo del DW.")

    def _serialize_ask(o: AskOutcome) -> dict[str, Any]:
        body: dict[str, Any] = {
            "ok": o.ok,
            "sql": o.sql,
            "error": o.error,
            "columns": o.columns,
            "rows": [list(r) if r else [] for r in (o.rows or [])],
            "llm_preview": (o.llm_raw[:2000] + "...")
            if o.llm_raw and len(o.llm_raw) > 2000
            else o.llm_raw,
        }
        return body

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/ingest")
    def ingest(body: Annotated[IngestPayload, Body(...)]):
        from pathlib import Path

        cat = Path(body.catalog_dir) if body.catalog_dir else None
        try:
            return run_ingest(reset=body.reset, catalog_dir=cat)
        except FileNotFoundError as e:
            raise HTTPException(400, str(e)) from e
        except ValueError as e:
            raise HTTPException(400, str(e)) from e

    @app.post("/search")
    def search(body: Annotated[QuestionPayload, Body(...)]):
        try:
            return {"hits": run_search(body.question, k=body.k)}
        except Exception as e:
            raise HTTPException(503, str(e)) from e

    @app.post("/context")
    def context(body: Annotated[QuestionPayload, Body(...)]):
        try:
            return run_context(body.question, k=body.k)
        except Exception as e:
            raise HTTPException(503, str(e)) from e

    @app.post("/ask")
    def ask(body: Annotated[AskPayload, Body(...)]):
        out = run_ask(
            body.question,
            k=body.k,
            dry_run=body.dry_run,
            max_rows=body.max_rows,
        )
        if out.error and not out.sql:
            raise HTTPException(502, detail=out.error)
        return _serialize_ask(out)

    return app


app = create_app()
