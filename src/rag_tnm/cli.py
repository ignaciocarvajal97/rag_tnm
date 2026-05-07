from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rag_tnm.runner import run_ask, run_context, run_ingest, run_search


def _cmd_ingest(args: argparse.Namespace) -> int:
    try:
        r = run_ingest(reset=args.reset, catalog_dir=Path(args.catalog_dir) if args.catalog_dir else None)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 1
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1
    print(f"Indexados {r['indexed']} fragmentos en '{r['collection']}' -> {r['chroma_path']}")
    return 0


def _cmd_search(args: argparse.Namespace) -> int:
    for i, hit in enumerate(run_search(args.question, k=args.k), start=1):
        title = hit.get("title", "")
        src = hit.get("source_file", "")
        doc = hit.get("text", "")
        print(f"--- [{i}] {title} {src and f'({src})'}")
        print(doc[:2000] + ("…" if len(doc) > 2000 else ""))
        print()
    return 0


def _cmd_context(args: argparse.Namespace) -> int:
    print(run_context(args.question, k=args.k)["prompt"])
    return 0


def _cmd_serve(args: argparse.Namespace) -> int:
    import uvicorn

    uvicorn.run("rag_tnm.api:app", host=args.host, port=args.port, reload=False)
    return 0


def _cmd_ask(args: argparse.Namespace) -> int:
    out = run_ask(
        args.question,
        k=args.k,
        dry_run=args.dry_run,
        max_rows=args.max_rows,
    )
    if out.error and out.sql is None:
        print(out.error, file=sys.stderr)
        return 1
    if out.sql:
        print("-- SQL generado --")
        print(out.sql)
        print()
    if out.error:
        print(out.error, file=sys.stderr)
    if args.dry_run:
        return 0 if out.sql else 1
    if not out.ok:
        return 1
    cols = out.columns or []
    if not cols:
        print("(sin filas o sin columnas)")
        return 0
    print("\t".join(str(c) for c in cols))
    for row in out.rows or []:
        print("\t".join("" if v is None else str(v) for v in row))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="rag-tnm", description="RAG TNM — catálogo + Chroma + Ollama + DW")
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("ingest", help="Indexar data/catalog en Chroma")
    pi.add_argument("--catalog-dir", default=None)
    pi.add_argument("--reset", action="store_true")
    pi.set_defaults(func=_cmd_ingest)

    ps = sub.add_parser("search", help="Buscar fragmentos por pregunta")
    ps.add_argument("question", type=str)
    ps.add_argument("-k", type=int, default=8)
    ps.set_defaults(func=_cmd_search)

    pc = sub.add_parser("context", help="Prompt Text-to-SQL con contexto recuperado")
    pc.add_argument("question", type=str)
    pc.add_argument("-k", type=int, default=8)
    pc.set_defaults(func=_cmd_context)

    pa = sub.add_parser("ask", help="RAG + Ollama -> SQL -> DW (solo SELECT)")
    pa.add_argument("question", type=str)
    pa.add_argument("-k", type=int, default=8)
    pa.add_argument("--dry-run", action="store_true")
    pa.add_argument("--max-rows", type=int, default=500)
    pa.set_defaults(func=_cmd_ask)

    pu = sub.add_parser("serve", help="Servidor FastAPI (uvicorn)")
    pu.add_argument("--host", default="127.0.0.1")
    pu.add_argument("--port", type=int, default=8000)
    pu.set_defaults(func=_cmd_serve)

    return p


def app() -> None:
    parser = build_parser()
    ns = parser.parse_args()
    raise SystemExit(ns.func(ns))


if __name__ == "__main__":
    app()
