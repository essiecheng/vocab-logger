import json
import pytest
from vocab.models import Word
from vocab.storage import load_words, save_words, find_word


@pytest.fixture
def db_path(tmp_path, monkeypatch):
    """Point DB_PATH to a temp file for each test."""
    import vocab.storage as storage
    path = tmp_path / "words.json"
    monkeypatch.setattr(storage, "DB_PATH", path)
    return path


def make_word(**kwargs) -> Word:
    defaults = dict(hanzi="随便", pinyin="suí biàn", definition="whatever")
    return Word(**{**defaults, **kwargs})


def test_load_empty(db_path):
    assert load_words() == []


def test_save_and_load(db_path):
    words = [make_word(), make_word(hanzi="加油", pinyin="jiā yóu", definition="keep it up")]
    save_words(words)
    loaded = load_words()
    assert len(loaded) == 2
    assert loaded[0].hanzi == "随便"
    assert loaded[1].hanzi == "加油"


def test_save_preserves_chinese(db_path):
    save_words([make_word()])
    raw = json.loads(db_path.read_text())
    assert raw[0]["hanzi"] == "随便"


def test_find_word_found(db_path):
    words = [make_word()]
    assert find_word(words, "随便") is not None


def test_find_word_not_found(db_path):
    words = [make_word()]
    assert find_word(words, "加油") is None
