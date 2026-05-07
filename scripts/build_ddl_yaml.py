"""Genera data/catalog/00_ddl_real.yaml a partir del DDL volcado con pg_dump.

Uso:
    python scripts/build_ddl_yaml.py [INPUT_SQL] [OUTPUT_YAML]

Por defecto:
    INPUT_SQL  = data/catalog/_ddl_real.sql
    OUTPUT_YAML = data/catalog/00_ddl_real.yaml

Genera un fragmento (chunk) por tabla con sus columnas, tipos y PK; al inicio
incluye un "indice" con el listado de todas las tablas. Pensado para que el RAG
ofrezca al LLM la verdad del schema en lugar de descripciones en prosa.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Table:
    name: str
    columns: list[tuple[str, str, bool]] = field(default_factory=list)  # (name, type, not_null)
    pk: list[str] = field(default_factory=list)


CREATE_TABLE_RE = re.compile(
    r"CREATE TABLE public\.(?P<name>\"?[\w]+\"?)\s*\((?P<body>.*?)\);",
    re.DOTALL,
)
PK_RE = re.compile(
    r"ALTER TABLE ONLY public\.(?P<table>\"?[\w]+\"?)\s+ADD CONSTRAINT \w+ PRIMARY KEY \((?P<cols>[^)]+)\);",
    re.IGNORECASE,
)


def _strip_quotes(s: str) -> str:
    return s.strip().strip('"')


_COL_LINE_RE = re.compile(r'^(?P<name>"[^"]+"|[A-Za-z_][A-Za-z0-9_]*)\s+(?P<rest>.+)$')


def parse_ddl(sql: str) -> dict[str, Table]:
    tables: dict[str, Table] = {}

    for m in CREATE_TABLE_RE.finditer(sql):
        name = _strip_quotes(m.group("name"))
        body = m.group("body").strip()
        cols: list[tuple[str, str, bool]] = []
        for raw in body.splitlines():
            line = raw.strip().rstrip(",").strip()
            if not line:
                continue
            if re.match(r"(?i)^(CONSTRAINT|PRIMARY KEY|UNIQUE|FOREIGN KEY|CHECK)\b", line):
                continue
            cm = _COL_LINE_RE.match(line)
            if not cm:
                continue
            col_name = _strip_quotes(cm.group("name"))
            rest = cm.group("rest").strip().rstrip(",")
            not_null = bool(re.search(r"(?i)\bNOT\s+NULL\b", rest))
            type_str = re.sub(r"(?i)\s*NOT\s+NULL\s*$", "", rest).strip()
            type_str = re.sub(r"(?i)\s*DEFAULT\s+.+$", "", type_str).strip()
            cols.append((col_name, type_str, not_null))
        tables[name] = Table(name=name, columns=cols)

    for m in PK_RE.finditer(sql):
        name = _strip_quotes(m.group("table"))
        cols = [_strip_quotes(c) for c in m.group("cols").split(",")]
        if name in tables:
            tables[name].pk = cols

    return tables


def _table_doc(t: Table) -> str:
    lines = [f"Tabla `public.{t.name}`."]
    if t.pk:
        lines.append(f"PK: {', '.join('`' + c + '`' for c in t.pk)}.")
    lines.append("")
    lines.append("Columnas (nombre — tipo, NOT NULL?):")
    for col, typ, nn in t.columns:
        flag = "NOT NULL" if nn else "NULL"
        lines.append(f"- `{col}` — {typ} ({flag})")
    return "\n".join(lines)


def _index_doc(tables: dict[str, Table]) -> str:
    lines = [
        "Índice de tablas reales del esquema `public` (DDL extraído con pg_dump).",
        "",
        "Las únicas tablas que existen son las siguientes. Cualquier tabla NO listada aquí",
        "**no existe** y no debe ser usada en SQL:",
        "",
    ]
    for name in sorted(tables):
        t = tables[name]
        pk = f"PK={'+'.join(t.pk)}" if t.pk else "sin PK"
        lines.append(f"- `public.{name}` ({pk}, {len(t.columns)} columnas)")
    return "\n".join(lines)


def to_yaml(tables: dict[str, Table]) -> str:
    chunks: list[str] = []

    # 1) Índice global (top-level chunk para retrieval)
    chunks.append(
        "- id: ddl-real-indice\n"
        "  title: \"DDL real (pg_dump): índice de tablas\"\n"
        "  schema: public\n"
        "  kind: ddl_index\n"
        "  domain: ddl\n"
        "  source: pg_dump --schema-only public\n"
        "  content: |\n"
        + _indent(_index_doc(tables), 4)
    )

    # 2) Un chunk por tabla
    for name in sorted(tables):
        t = tables[name]
        title = f"DDL real `public.{t.name}`"
        body = _table_doc(t)
        chunks.append(
            f"- id: ddl-real-{name.lower()}\n"
            f"  title: \"{title}\"\n"
            f"  schema: public\n"
            f"  kind: ddl_table\n"
            f"  domain: ddl\n"
            f"  source: pg_dump --schema-only public\n"
            f"  content: |\n"
            + _indent(body, 4)
        )

    return "\n\n".join(chunks) + "\n"


def _indent(text: str, n: int) -> str:
    pad = " " * n
    return "\n".join(pad + line for line in text.splitlines())


def main(argv: list[str]) -> int:
    here = Path(__file__).resolve().parent.parent
    inp = Path(argv[1]) if len(argv) > 1 else here / "data" / "catalog" / "_ddl_real.sql"
    out = Path(argv[2]) if len(argv) > 2 else here / "data" / "catalog" / "00_ddl_real.yaml"
    if not inp.exists():
        print(f"No existe: {inp}", file=sys.stderr)
        return 1
    sql = inp.read_text(encoding="utf-8")
    tables = parse_ddl(sql)
    if not tables:
        print("No se encontraron tablas en el DDL", file=sys.stderr)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(to_yaml(tables), encoding="utf-8")
    print(f"OK -> {out} ({len(tables)} tablas, {out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
