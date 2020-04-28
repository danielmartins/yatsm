import typer

from yatsm.commands import api, worker

app = typer.Typer()

app.add_typer(worker.app, name="worker")
app.add_typer(api.app, name="api")
