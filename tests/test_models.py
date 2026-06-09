from vocab.models import Word


def test_accuracy_none_when_no_attempts():
    w = Word(hanzi="随便", pinyin="suí biàn", definition="whatever")
    assert w.accuracy is None


def test_accuracy_calculation():
    w = Word(hanzi="随便", pinyin="suí biàn", definition="whatever", quiz_correct=3, quiz_attempts=4)
    assert w.accuracy == 0.75


def test_default_tags_empty():
    w = Word(hanzi="随便", pinyin="suí biàn", definition="whatever")
    assert w.tags == []


def test_tags_not_shared_between_instances():
    w1 = Word(hanzi="随便", pinyin="suí biàn", definition="whatever")
    w2 = Word(hanzi="加油", pinyin="jiā yóu", definition="keep it up")
    w1.tags.append("drama")
    assert w2.tags == []
