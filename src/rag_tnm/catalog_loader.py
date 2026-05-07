from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class CatalogChunk:
    """Un fragmento indexable: texto para embedding + metadatos filtrables."""

    id: str
    text: str
    metadata: dict[str, Any]


def _slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^\w\-]+", "-", s, flags=re.UNICODE)
    return re.sub(r"-{2,}", "-", s).strip("-") or "doc"


def load_yaml_catalog(path: Path) -> list[CatalogChunk]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError(f"{path}: el YAML raíz debe ser una lista de documentos")

    out: list[CatalogChunk] = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            continue
        doc_id = str(item.get("id") or f"{path.stem}-{i}")
        title = str(item.get("title") or doc_id)
        body = item.get("content")
        if body is None:
            raise ValueError(f"{path}: documento '{doc_id}' sin campo 'content'")
        text = f"{title}\n\n{body}".strip()
        meta = {k: v for k, v in item.items() if k not in ("id", "title", "content")}
        meta["source_file"] = path.name
        meta["title"] = title
        out.append(CatalogChunk(id=_slug(doc_id), text=text, metadata=meta))
    return out


def load_markdown_catalog(path: Path) -> list[CatalogChunk]:
    """Un .md = un documento; el primer # opcional se usa como título."""
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    lines = text.splitlines()
    title = path.stem
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
    doc_id = _slug(path.stem)
    return [
        CatalogChunk(
            id=doc_id,
            text=f"{title}\n\n{text}",
            metadata={"source_file": path.name, "title": title, "format": "markdown"},
        )
    ]


def load_catalog_dir(catalog_dir: Path) -> list[CatalogChunk]:
    if not catalog_dir.is_dir():
        return []

    chunks: list[CatalogChunk] = []
    for path in sorted(catalog_dir.rglob("*")):
        if path.suffix.lower() in (".yaml", ".yml"):
            chunks.extend(load_yaml_catalog(path))
        elif path.suffix.lower() == ".md":
            chunks.extend(load_markdown_catalog(path))
    return chunks
