"""
Smoke test del RAG: pregunta de negocio sobre servicios en abril 2026.
Usa catálogo en disco + Chroma en directorio temporal (sin tocar ./data/chroma del proyecto).
"""

from pathlib import Path

import pytest

from rag_tnm.catalog_loader import load_catalog_dir
from rag_tnm.vector_store import get_client, ingest_chunks, query_context, reset_collection

CATALOG_DIR = Path(__file__).resolve().parent.parent / "data" / "catalog"

QUESTION = "cuántos servicios se hicieron en abril del 2026"


@pytest.fixture
def collection(tmp_path):
    client = get_client(str(tmp_path / "chroma"))
    col = reset_collection(client, "test_dw_catalog")
    chunks = load_catalog_dir(CATALOG_DIR)
    assert len(chunks) >= 5, "el catálogo de ejemplo debe tener varios fragmentos"
    ingest_chunks(col, chunks)
    return col


def test_retrieval_servicios_abril_includes_schema_snippet(collection):
    docs, _metas = query_context(collection, QUESTION, n_results=6)
    assert docs, "el RAG debe devolver al menos un documento"
    blob = "\n".join(docs).lower()
    assert "servicio" in blob
    assert "2026-04" in blob or "abril" in blob or "etapa_1_fecha" in blob
