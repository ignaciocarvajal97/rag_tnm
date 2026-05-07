from __future__ import annotations

import httpx


def ollama_chat(
    base_url: str,
    model: str,
    system: str,
    user: str,
    *,
    num_ctx: int = 8192,
    temperature: float = 0.1,
    timeout_s: float = 180.0,
) -> str:
    url = f"{base_url.rstrip('/')}/api/chat"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "options": {"temperature": temperature, "num_ctx": num_ctx},
    }
    with httpx.Client(timeout=timeout_s) as client:
        r = client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
    msg = data.get("message") or {}
    content = msg.get("content")
    if not content:
        raise RuntimeError(f"Respuesta Ollama inesperada: {data!r}")
    return content
