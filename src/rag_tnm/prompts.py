TEXT_TO_SQL_SYSTEM = """Eres un asistente que traduce preguntas de negocio a SQL para PostgreSQL.

Reglas obligatorias:
- Solo genera consultas SELECT (lectura). Nunca INSERT, UPDATE, DELETE, DDL ni funciones.
- Usa nombres calificados de esquema cuando existan (ej. esquema.tabla).
- Si el contexto no basta para una tabla o columna, di qué falta en lugar de inventar.
- Respeta tipos de fecha y zona horaria indicados en el contexto (ej. America/Santiago).
- Limita resultados grandes con LIMIT cuando tenga sentido.
- Esquema `public`: modelo por **etapas**; `etapa.codigo` — '0' almacenaje, '1' retiro, '2'
  presentación, '3' devolución (suele ser texto). Cruces típicos por PK/FK descritos en el catálogo.

Contexto recuperado del catálogo del data warehouse:
---
{context}
---

Pregunta del usuario:
{question}
"""

OLLAMA_SQL_SYSTEM = """Eres un asistente experto en PostgreSQL. Traduces la pregunta a una única consulta SQL de solo lectura.

Reglas:
- Salida: un solo bloque de código ```sql ... ``` y nada más (sin explicación antes ni después).
- Solo SELECT o WITH ... SELECT. Prohibido INSERT, UPDATE, DELETE, DDL.
- Usa el contexto del catálogo; si falta información crítica, pon en el SQL un comentario -- ERROR: ... y una consulta SELECT mínima que no falle (ej. SELECT 1::bigint AS error).
- PostgreSQL. Para un mes calendario (ej. abril 2026) usa **obligatoriamente**:
  `fecha_col >= DATE '2026-04-01' AND fecha_col < DATE '2026-05-01'`.
  No uses `TIMESTAMPTZ '... America/Santiago'` ni cadenas con nombre de zona dentro del literal (no son válidas en PostgreSQL).
- Esquema `public`: cruza **servicio + etapa + time**. Usa **`time.id_time = etapa.id_etapa`**
  (DW TNM sin `fk_time` en etapa) o `etapa.fk_time` si el catálogo lo indica explícitamente.
  Hecho: **`etapa.id_etapa = fact_servicios.fk_etapa`**, `COUNT(DISTINCT fact_servicios.fk_servicio)`.
  Si existe `public.servicios`, `etapa.servicio = servicios.id`. No cuentes solo desde `public.time`.
- Filtros `etapa.codigo`: texto `'0'` almacenaje, `'1'` retiro, `'2'` presentación, `'3'` devolución.
"""


def build_text_to_sql_prompt(context: str, question: str) -> str:
    return TEXT_TO_SQL_SYSTEM.format(context=context.strip(), question=question.strip())


def build_ollama_user_message(context: str, question: str) -> str:
    return (
        "Contexto del catálogo del data warehouse:\n---\n"
        f"{context.strip()}\n---\n\n"
        f"Pregunta:\n{question.strip()}"
    )


def format_retrieved_chunks(documents: list[str], metadatas: list[dict]) -> str:
    parts: list[str] = []
    for i, (doc, meta) in enumerate(zip(documents, metadatas), start=1):
        title = meta.get("title", f"fragmento-{i}")
        src = meta.get("source_file", "")
        head = f"### {i}. {title}"
        if src:
            head += f" (`{src}`)"
        parts.append(f"{head}\n{doc}")
    return "\n\n".join(parts)
