import os
import subprocess

import typer

from yatsm.settings import settings

app = typer.Typer()

DEFAULT_QUEUE = "default"


@app.command()
def start(
    queue_name: str = DEFAULT_QUEUE, redis_dsn: str = settings.redis_dsn,
):
    typer.echo(queue_name)
    typer.echo(redis_dsn)
    typer.echo(os.environ.items())
    cmd = ["dramatiq", "-v", "yatsm.jobs:redis_broker"]
    subprocess.run(cmd, shell=True, check=True, env={"YATSM_REDIS_DSN": redis_dsn})
    # subprocess.run("env", shell=True, check=True)


@app.command()
def echo(message: str, queue_name: str = DEFAULT_QUEUE):
    typer.echo(message)
