from __future__ import annotations

import httpx


def ollama_chat(
    base_url: str,
    model: str,
    system: str,
    user: str,
    *,
    num_ctx: int = 8192,
    temperature: float = 0,
    timeout_s: float = 180.0,
    extra_messages: list[dict] | None = None,
) -> str:
    """Llama a Ollama /api/chat.

    Si `extra_messages` se entrega, se inserta entre el `system` y el `user`
    final. Útil para few-shot en formato chat (pares user/assistant).
    """
    url = f"{base_url.rstrip('/')}/api/chat"
    messages: list[dict] = [{"role": "system", "content": system}]
    if extra_messages:
        messages.extend(extra_messages)
    messages.append({"role": "user", "content": user})
    payload = {
        "model": model,
        "messages": messages,
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
