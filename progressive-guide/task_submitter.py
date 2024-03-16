from task_server import my_b_task
import asyncio

if __name__ == "__main__":
    val = my_b_task.submit("Agrajag")
    print(val)
