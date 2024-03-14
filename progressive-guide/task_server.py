from prefect import task
from prefect.task_server import serve


@task
def my_b_task(name: str):
    print(f"Hello, {name}!")


if __name__ == "__main__":
    from task_server import my_b_task

    serve(my_b_task)

    # NOTE: The serve() function accepts multiple task runs of the same task.
    # You can start multiple task servers.
