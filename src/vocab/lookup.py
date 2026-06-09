import os
from openai import OpenAI


def lookup_chinese(hanzi: str) -> tuple[str, str]:
    """Return (pinyin, definition) for a Chinese word using the OpenAI API."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = (
        f"For the Chinese word or phrase '{hanzi}', provide:\n"
        "1. Pinyin with tone marks\n"
        "2. A concise English definition (one line)\n\n"
        "Respond in exactly this format:\n"
        "pinyin: <pinyin>\n"
        "definition: <definition>"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=80,
    )
    text = response.choices[0].message.content or ""
    pinyin, definition = "", ""
    for line in text.strip().splitlines():
        if line.startswith("pinyin:"):
            pinyin = line.split(":", 1)[1].strip()
        elif line.startswith("definition:"):
            definition = line.split(":", 1)[1].strip()
    return pinyin, definition
