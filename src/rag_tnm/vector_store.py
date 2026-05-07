from __future__ import annotations

from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings

from rag_tnm.catalog_loader import CatalogChunk


def get_client(persist_path: str) -> chromadb.PersistentClient:
    return chromadb.PersistentClient(
        path=persist_path,
        settings=ChromaSettings(anonymized_telemetry=False),
    )


def get_or_create_collection(client: chromadb.PersistentClient, name: str):
    return client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})


def reset_collection(client: chromadb.PersistentClient, name: str):
    try:
        client.delete_collection(name)
    except Exception:
        pass
    return get_or_create_collection(client, name)


def ingest_chunks(collection, chunks: list[CatalogChunk]) -> int:
    if not chunks:
        return 0
    ids = [c.id for c in chunks]
    documents = [c.text for c in chunks]
    metadatas: list[dict[str, Any]] = []
    for c in chunks:
        flat: dict[str, Any] = {}
        for k, v in c.metadata.items():
            if v is None:
                continue
            if isinstance(v, (str, int, float, bool)):
                flat[k] = v
            else:
                flat[k] = str(v)
        metadatas.append(flat)
    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    return len(chunks)


def query_context(
    collection,
    question: str,
    n_results: int = 8,
) -> tuple[list[str], list[dict[str, Any]]]:
    res = collection.query(query_texts=[question], n_results=n_results)
    docs = (res.get("documents") or [[]])[0]
    metas = (res.get("metadatas") or [[]])[0]
    return docs, metas
