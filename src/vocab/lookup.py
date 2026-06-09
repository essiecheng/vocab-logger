from __future__ import annotations
import os
import httpx


def lookup_chinese(hanzi: str) -> tuple[str, str]:
    """Return (pinyin, definition) for a Chinese word using the OpenAI API."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    response = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"For the Chinese word or phrase '{hanzi}', provide:\n"
                        "1. Pinyin with tone marks\n"
                        "2. A concise English definition (one line)\n\n"
                        "Respond in exactly this format:\n"
                        "pinyin: <pinyin>\n"
                        "definition: <definition>"
                    ),
                }
            ],
            "max_tokens": 80,
        },
        timeout=15,
    )
    response.raise_for_status()
    text = response.json()["choices"][0]["message"]["content"] or ""
    pinyin, definition = "", ""
    for line in text.strip().splitlines():
        if line.startswith("pinyin:"):
            pinyin = line.split(":", 1)[1].strip()
        elif line.startswith("definition:"):
            definition = line.split(":", 1)[1].strip()
    return pinyin, definition
