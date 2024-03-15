from prefect import task
from prefect.task_server import serve


@task
def my_fastapi_task(name: str):
    print(f"Hello, {name}!")


if __name__ == "__main__":
    from first_fastapi_task_server import my_fastapi_task

    serve(my_fastapi_task)

    # NOTE: The serve() function accepts multiple task runs of the same task.
    # You can start multiple task servers.
