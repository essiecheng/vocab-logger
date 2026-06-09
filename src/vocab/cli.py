from typing import Optional

import typer
from rich import print as rprint

from .lookup import lookup_chinese
from .models import Word
from .storage import find_word, load_words, save_words

app = typer.Typer(help="Chinese vocabulary logger and quizzer.")


@app.command()
def add(
    hanzi: str,
    pinyin: Optional[str] = typer.Option(None, help="Override auto-generated pinyin"),
    definition: Optional[str] = typer.Option(None, help="Override auto-generated definition"),
    tags: Optional[str] = typer.Option(None, help="Comma-separated tags, e.g. 'drama,ep3'"),
):
    """Add a Chinese word. Pinyin and definition are looked up automatically."""
    words = load_words()
    if find_word(words, hanzi):
        rprint(f"[yellow]'{hanzi}' is already in your list.[/yellow]")
        raise typer.Exit()

    if pinyin is None or definition is None:
        rprint(f"[dim]Looking up '{hanzi}'...[/dim]")
        try:
            auto_pinyin, auto_def = lookup_chinese(hanzi)
        except Exception as e:
            rprint(f"[red]Lookup failed: {e}[/red]")
            rprint("[yellow]Set OPENAI_API_KEY or pass --pinyin and --definition manually.[/yellow]")
            raise typer.Exit(1)
        pinyin = pinyin or auto_pinyin
        definition = definition or auto_def

    tag_list = [t.strip() for t in tags.split(",")] if tags else []
    words.append(Word(hanzi=hanzi, pinyin=pinyin, definition=definition, tags=tag_list))
    save_words(words)
    rprint(f"[green]Added:[/green] {hanzi} — {pinyin} — {definition}")
    if tag_list:
        rprint(f"  [dim]tags: {', '.join(tag_list)}[/dim]")


@app.command()
def remove(word: str):
    """Remove a word."""
    print(f"remove: {word}")


@app.command(name="list")
def list_words():
    """List all words."""
    print("list")


@app.command()
def quiz():
    """Quiz yourself."""
    print("quiz")


@app.command()
def stats():
    """Show stats."""
    print("stats")


def main():
    app()
