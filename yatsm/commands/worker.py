import asyncio

import typer

app = typer.Typer()

DEFAULT_QUEUE = "default"


@app.command()
def start(queue_name: str = DEFAULT_QUEUE):
    typer.echo(queue_name)


@app.command()
def echo(message: str, queue_name: str = DEFAULT_QUEUE):
    typer.echo(message)
