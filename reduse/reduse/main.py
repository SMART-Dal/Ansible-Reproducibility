import typer
from . import detector as dt
from . import parser
from . import smell_detection as sd

app = typer.Typer()


@app.command(name="detect_all")
def detect_all(path: str = typer.Argument(..., help="Path to the file")):
    dt.main_method(path)
    typer.echo("Detection process has finished.")


@app.command(name="check_idempotency")
def check_idempotency(path: str = typer.Argument(..., help="Path to the file")):
    tasks = parser.get_parsed_tasks(path)
    for task in tasks:
        idempotency = sd.check_task_for_idempotency(task=task)
        typer.echo("Idempotency detection process has finished. " + idempotency)
