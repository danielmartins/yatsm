import typer

from yatsm.commands import worker

app = typer.Typer()

app.add_typer(worker.app, name="worker")
