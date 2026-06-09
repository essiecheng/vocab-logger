from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Word:
    hanzi: str
    pinyin: str
    definition: str
    tags: list[str] = field(default_factory=list)
    added_at: str = field(default_factory=lambda: datetime.now().isoformat())
    quiz_correct: int = 0
    quiz_attempts: int = 0
