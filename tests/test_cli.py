import pytest
from typer.testing import CliRunner
from vocab.cli import app
import vocab.storage as storage

runner = CliRunner()


@pytest.fixture(autouse=True)
def tmp_db(tmp_path, monkeypatch):
    """Redirect DB_PATH to a temp file for every test."""
    monkeypatch.setattr(storage, "DB_PATH", tmp_path / "words.json")


def test_add_with_manual_fields():
    result = runner.invoke(app, ["add", "随便", "--pinyin", "suí biàn", "--definition", "whatever"])
    assert result.exit_code == 0
    assert "Added" in result.output


def test_add_duplicate():
    runner.invoke(app, ["add", "随便", "--pinyin", "suí biàn", "--definition", "whatever"])
    result = runner.invoke(app, ["add", "随便", "--pinyin", "suí biàn", "--definition", "whatever"])
    assert "already in your list" in result.output


def test_add_with_tags():
    result = runner.invoke(app, ["add", "随便", "--pinyin", "suí biàn", "--definition", "whatever", "--tags", "drama,ep1"])
    assert result.exit_code == 0
    assert "drama" in result.output


def test_list_empty():
    result = runner.invoke(app, ["list"])
    assert "No words yet" in result.output


def test_list_shows_words():
    runner.invoke(app, ["add", "随便", "--pinyin", "suí biàn", "--definition", "whatever"])
    result = runner.invoke(app, ["list"])
    assert "随便" in result.output


def test_remove_existing():
    runner.invoke(app, ["add", "随便", "--pinyin", "suí biàn", "--definition", "whatever"])
    result = runner.invoke(app, ["remove", "随便"])
    assert "Removed" in result.output


def test_remove_nonexistent():
    result = runner.invoke(app, ["remove", "随便"])
    assert "not found" in result.output


def test_stats_empty():
    result = runner.invoke(app, ["stats"])
    assert "No words yet" in result.output


def test_stats_shows_totals():
    runner.invoke(app, ["add", "随便", "--pinyin", "suí biàn", "--definition", "whatever"])
    result = runner.invoke(app, ["stats"])
    assert "Total words" in result.output
    assert "1" in result.output
