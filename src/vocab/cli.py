import typer

app = typer.Typer(help="Chinese vocabulary logger and quizzer.")


@app.command()
def add(word: str):
    """Add a word."""
    print(f"add: {word}")


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
