from __future__ import annotations
import json
from pathlib import Path
from .models import Word

DB_PATH = Path.home() / ".vocab_logger" / "words.json"


def load_words() -> list[Word]:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        return []
    return [Word(**w) for w in json.loads(DB_PATH.read_text())]


def save_words(words: list[Word]) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    DB_PATH.write_text(json.dumps([w.__dict__ for w in words], ensure_ascii=False, indent=2))


def find_word(words: list[Word], hanzi: str) -> Word | None:
    return next((w for w in words if w.hanzi == hanzi), None)
