from prefect import task
from prefect.task_server import serve


@task
def my_b_task(name: str):
    print(f"Hello, {name}!")


if __name__ == "__main__":
    from task_server import my_b_task

    serve(my_b_task)

    # NOTE: The serve() function accepts multiple tasks. The Task Server
    # will listen for submitted task runs for all tasks passed in.
