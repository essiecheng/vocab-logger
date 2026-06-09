import random
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from .lookup import lookup_chinese
from .models import Word
from .storage import find_word, load_words, save_words

console = Console()

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
def remove(hanzi: str):
    """Remove a word from your list."""
    words = load_words()
    if not find_word(words, hanzi):
        rprint(f"[yellow]'{hanzi}' not found.[/yellow]")
        raise typer.Exit()
    save_words([w for w in words if w.hanzi != hanzi])
    rprint(f"[red]Removed:[/red] {hanzi}")


@app.command(name="list")
def list_words(
    recent: int = typer.Option(0, "--recent", "-r", help="Show N most recently added words"),
    random_n: int = typer.Option(0, "--random", help="Show N random words"),
    tag: Optional[str] = typer.Option(None, help="Filter by tag"),
):
    """List words in your vocabulary."""
    words = load_words()
    if not words:
        rprint("[dim]No words yet. Use 'vocab add' to get started.[/dim]")
        raise typer.Exit()

    if tag:
        words = [w for w in words if tag in w.tags]
        if not words:
            rprint(f"[yellow]No words tagged '{tag}'.[/yellow]")
            raise typer.Exit()

    if recent:
        words = sorted(words, key=lambda w: w.added_at, reverse=True)[:recent]
        title = f"Last {len(words)} added"
    elif random_n:
        words = random.sample(words, min(random_n, len(words)))
        title = f"{len(words)} random words"
    else:
        title = f"All vocabulary ({len(words)} words)"

    table = Table(title=title, show_lines=True)
    table.add_column("Hanzi", style="bold cyan")
    table.add_column("Pinyin", style="green")
    table.add_column("Definition")
    table.add_column("Tags", style="dim")
    table.add_column("Added", style="dim")

    for w in words:
        table.add_row(w.hanzi, w.pinyin, w.definition, ", ".join(w.tags), w.added_at[:10])

    console.print(table)


@app.command()
def quiz(
    count: int = typer.Option(10, "--count", "-n", help="Number of questions"),
    recent: int = typer.Option(0, "--recent", help="Quiz only the N most recently added words"),
    mode: str = typer.Option("hanzi", help="'hanzi' (see hanzi, type definition) or 'definition' (see definition, type hanzi)"),
):
    """Quiz yourself on your vocabulary."""
    words = load_words()
    if not words:
        rprint("[dim]No words yet. Use 'vocab add' to get started.[/dim]")
        raise typer.Exit()

    pool = sorted(words, key=lambda w: w.added_at, reverse=True)[:recent] if recent else words
    sample = random.sample(pool, min(count, len(pool)))
    correct = 0

    console.print(f"\n[bold]Quiz — {len(sample)} questions[/bold]  [dim](type 'skip' to skip, Ctrl-C to quit)[/dim]\n")

    try:
        for i, word in enumerate(sample, 1):
            if mode == "hanzi":
                console.print(f"[bold cyan]{i}. {word.hanzi}[/bold cyan]  [dim]{word.pinyin}[/dim]")
                answer = console.input("   Definition: ").strip().lower()
                expected = word.definition.lower()
            else:
                console.print(f"[bold]{i}.[/bold] {word.definition}  [dim](pinyin: {word.pinyin})[/dim]")
                answer = console.input("   Hanzi: ").strip()
                expected = word.hanzi

            if answer == "skip":
                rprint(f"   [dim]Skipped — answer: {word.definition if mode == 'hanzi' else word.hanzi}[/dim]\n")
                continue

            hit = answer in expected or expected in answer
            word.quiz_attempts += 1
            if hit:
                word.quiz_correct += 1
                correct += 1
                rprint("   [green]Correct![/green]\n")
            else:
                rprint(f"   [red]Incorrect.[/red] Answer: [bold]{word.definition if mode == 'hanzi' else word.hanzi}[/bold]\n")

    except (KeyboardInterrupt, typer.Abort):
        rprint("\n[dim]Quiz ended early.[/dim]")

    save_words(words)
    rprint(f"[bold]Score: {correct}/{len(sample)}[/bold]\n")


@app.command()
def stats():
    """Show overall stats and your hardest words."""
    words = load_words()
    if not words:
        rprint("[dim]No words yet.[/dim]")
        raise typer.Exit()

    attempted = [w for w in words if w.quiz_attempts > 0]
    total_correct = sum(w.quiz_correct for w in attempted)
    total_attempts = sum(w.quiz_attempts for w in attempted)
    overall = f"{total_correct / total_attempts:.0%}" if total_attempts else "—"

    rprint(f"\n[bold]Stats[/bold]")
    rprint(f"  Total words:      {len(words)}")
    rprint(f"  Words quizzed:    {len(attempted)}")
    rprint(f"  Overall accuracy: {overall}")

    if attempted:
        hardest = sorted(attempted, key=lambda w: w.quiz_correct / w.quiz_attempts)[:5]
        rprint("\n[bold]Hardest words:[/bold]")
        for w in hardest:
            rprint(f"  [cyan]{w.hanzi}[/cyan]  {w.pinyin}  —  {w.definition}  [dim]({w.quiz_correct}/{w.quiz_attempts})[/dim]")
    rprint()


def main():
    app()
