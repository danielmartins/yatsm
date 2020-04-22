import typer
import uvicorn

app = typer.Typer()

DEFAULT_QUEUE = "default"


@app.command()
def start():
    uvicorn.run("yatsm.api:app", host="127.0.0.1", port=8000, log_level="debug")


@app.command()
def echo(message: str, queue_name: str = DEFAULT_QUEUE):
    typer.echo(message)
