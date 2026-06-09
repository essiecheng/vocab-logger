from __future__ import annotations
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

    @property
    def accuracy(self) -> float | None:
        if self.quiz_attempts == 0:
            return None
        return self.quiz_correct / self.quiz_attempts
