# RAG TNM

RAG sobre el catálogo del data warehouse TNM: **ChromaDB**, **Ollama** (Text-to-SQL) y ejecución **solo SELECT** en PostgreSQL. Incluye API **FastAPI**.

## Requisitos

- Python 3.10+
- [Ollama](https://ollama.com) (`ollama pull qwen2.5-coder:7b` o similar)
- Variables `DEST_DB_*` en `.env` (o en `../datawarehouse_tnm/.env` si clonas junto al ETL)

## Instalación

```bash
cd rag_tnm
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
```

Copia `.env.example` a `.env` y ajusta.

## CLI

```bash
rag-tnm ingest --reset
rag-tnm search "pregunta en lenguaje natural"
rag-tnm context "..."
rag-tnm ask "..." --dry-run
rag-tnm ask "..."
rag-tnm serve --host 127.0.0.1 --port 8000
```

## API FastAPI

Con el servidor en marcha (`rag-tnm serve` o `uvicorn rag_tnm.api:app --reload`):

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Estado |
| POST | `/ingest` | Body JSON: `{"reset": false, "catalog_dir": null}` |
| POST | `/search` | `{"question": "...", "k": 8}` |
| POST | `/context` | `{"question": "...", "k": 8}` → prompt |
| POST | `/ask` | `{"question": "...", "k": 8, "dry_run": false, "max_rows": 500}` |

Documentación interactiva: `http://127.0.0.1:8000/docs`

## Tests

```bash
pytest -q
```

## Notas

- El catálogo vive en `data/catalog/*.yaml` y `*.md`.
- Chroma persiste en `data/chroma/` (ignorado en git).
