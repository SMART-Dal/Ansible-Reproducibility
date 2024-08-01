import typer
import detector as dt
import parser as parser
import smell_detection as sd

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


if __name__ == "__main__":
    app(detect_all('/home/ghazal/Ansible-Reproducibility/src/extraction/test/manual_validation/ansible-for-devops/apache.yml'))
