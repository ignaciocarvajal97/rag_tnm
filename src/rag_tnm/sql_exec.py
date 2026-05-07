from __future__ import annotations

import re
from dataclasses import dataclass

import psycopg2
from psycopg2.extensions import connection as PgConnection


@dataclass
class DwConnectionParams:
    host: str
    port: int
    dbname: str
    user: str
    password: str


def extract_sql_from_text(text: str) -> str | None:
    m = re.search(r"```(?:sql)?\s*([\s\S]*?)```", text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m2 = re.search(
        r"(^\s*(?:WITH|SELECT)\s[\s\S]+?)(?:;?\s*$)",
        text,
        re.IGNORECASE | re.MULTILINE,
    )
    if m2:
        return m2.group(1).strip().rstrip(";")
    return None


def assert_read_only_sql(sql: str) -> None:
    s = sql.strip()
    if not s:
        raise ValueError("SQL vacío")
    low = s.lower()
    if not (low.startswith("select") or low.startswith("with")):
        raise ValueError("Solo se permiten consultas SELECT / WITH ... SELECT")
    banned = (
        " insert ",
        " update ",
        " delete ",
        " drop ",
        " truncate ",
        " alter ",
        " create ",
        " grant ",
        " revoke ",
        " copy ",
        "\\copy",
    )
    padded = f" {low} "
    for b in banned:
        if b in padded:
            raise ValueError(f"Instrucción no permitida detectada: {b.strip()}")


def connect_dw(p: DwConnectionParams, *, connect_timeout: int = 15) -> PgConnection:
    return psycopg2.connect(
        host=p.host,
        port=p.port,
        dbname=p.dbname,
        user=p.user,
        password=p.password,
        connect_timeout=connect_timeout,
    )


def run_select(
    conn: PgConnection,
    sql: str,
    *,
    max_rows: int = 500,
    statement_timeout_ms: int = 120_000,
) -> tuple[list[str], list[tuple]]:
    sql = sql.strip().rstrip(";")
    assert_read_only_sql(sql)
    with conn.cursor() as cur:
        cur.execute(f"SET LOCAL statement_timeout = {statement_timeout_ms}")
        cur.execute(sql)
        if cur.description is None:
            return [], []
        cols = [d[0] for d in cur.description]
        rows = cur.fetchmany(max_rows + 1)
        if len(rows) > max_rows:
            rows = rows[:max_rows]
    return cols, rows
