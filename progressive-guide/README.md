# Exploring Prefect Background Task Examples

This guide will familiarize you with Prefect background tasks and task servers.

We'll start by running a Prefect task outside of a flow.
Then we'll start a task server and run tasks in the background.
We'll see how we can use multiple task servers to run tasks in parallel.
Then we create our first basic FastAPI application that submits tasks to a Prefect task server when you hit an endpoint.

Then we'll move to using Docker with two examples that mimic real use cases.
One example uses with a FastAPI server with multiple microservices.
The other example uses a Flask server with Marvin to ask an LLM questions and get audio answers.

## Examples

1. Run a Prefect task outside of a flow
1. Start a task server (or two) and run tasks in the background
1. Create a basic FastAPI server that submits tasks to a Prefect task server (WIP - files present, will add as #3 in the guide soon)
1. Use Docker to run a FastAPI server and a few Prefect task servers
1. Use Docker to run a Flask server and a Prefect task server with Marvin and ask the LLM questions

## Prefect Cloud or a Prefect server instance

You can use either Prefect Cloud or a local Prefect server instance for these examples.

You need to have `PREFECT_API_URL`set to use background task servers.

If you're using a local Prefect server instance with a SQLite backing database (the default database), you can save this value to your active Prefect Profile by running the following command in your terminal.

```bash
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```

If using Prefect Cloud, you can set the `PREFECT_API_URL` value to the Prefect Cloud API URL and add your API key.

The Docker examples (examples 3 and 4) use a local Prefect server instance by default.
You can switch to Prefect Cloud by changing the `PREFECT_API_URL` and adding a variable for your API key in the `docker-compose.yaml`.
Or use a local server instance backed by a PostgreSQL database by setting the `PREFECT__DATABASE__CONNECTION_URL`.

## Example 1: Run a Prefect task outside a flow

Step 1: Activate a virtual environment with Prefect 2.16.3 or newer installed.

Here's an example that uses [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html):

```bash
conda deactivate
conda create -n t1 python=3.12
conda activate t1
pip install -U prefect
```

Step 2: Set your Prefect profile to use experimental task scheduling.

```bash
prefect config set PREFECT_EXPERIMENTAL_ENABLE_TASK_SCHEDULING=true
```

Step 3: Start your Prefect server instance.

```bash
prefect server start --host 0.0.0.0
```

Step 4: Make a file named `greeter.py` and save the following code in it.

```python
from prefect import task 

@task(log_prints=True)
def greet(name: str = "Marvin"):
    print(f"Hello, {name}!")

if __name__ == "__main__":
    greet()
```

Step 5: Run the script in the terminal.

```bash
python greeter.py
```

You should see the task run in the terminal.

Optional:

You can see the task run in the UI (when the task run page is implemented - coming soon!).
If you're using a self-hosted Prefect Server instance, you can also see the task runs in the database.

If yo want to inspect the SQLite database, use your favorite interface. We show how to use *DB Browser for SQLite* below.

Download it [here](https://sqlitebrowser.org/dl/), if needed. Install it and open it.

Click *Connect*. Then navigate to your SQLite DB file. It will be in the `~/.prefect` directory by default.

Head to the `task_run` table and you should see all your task runs there. You can scroll down to see your most recent task runs or filter for them.

Hit the refresh button for updates, if needed.

## Example 2: Start a task server and run tasks in the background

In this example, we'll start a task server and run tasks in the background.  

Use your setup from Example 1.

Step 1: Create the task and task server in the file `task_server.py`

```python
from prefect import task
from prefect.task_server import serve


@task
def my_background_task(name: str):
    print(f"Hello, {name}!")


if __name__ == "__main__":
    from task_server import my_b_task
    # the line above shouldn't be necessary once a fix is in place

    serve(my_b_task)
```

Step 2: Start the task server.

Run the script in the terminal.

```bash
python task_server.py
```

The task server is now waiting for runs of the my_background_task task. Let's give it some task runs.

Step 3: Create a file named `task_submitter.py` and save the following code in it

```python
from task_server import my_b_task

if __name__ == "__main__":
    val = my_b_task.submit("Agrajag")
    print(val)
```

Step 4: Open another terminal and run the script.

```bash
python task_submitter.py
```

Note that we return the task run info from the `submit` method. This way we can see the task run UIID and other information about the task run.

Step 5: See the task run in the UI.

Use the task run UUID to see the task run in the UI. The URL will look like this:

<http://127.0.0.1:4200/task-runs/task-run/3ae4ad3a-d679-4bb5-9e2f-230d281f52ee>

Substitute in your UUID at the end of the URL. This UI navigation experience will be improved soon.

Step 6: Start another instance of the task server

In another terminal run:

```bash
python task_server.py
```

Step 7: Submit multiple tasks to the task server with `map`.

Modify the `task_submitter.py` file to submit multiple tasks to the task server by using the `map` method.

```python
from task_server import my_b_task

if __name__ == "__main__":
    my_b_task.map(["Ford", "Prefect", "Slartibartfast"])
```

Run the file and watch the work get distributed across both task servers!

Step 8: Shut down the task servers with *control* + *c*

Alright, you're able to submit tasks to multiple Prefect task servers running in the background!
This is cool because we can observe these tasks executing in parallel and very quickly with web sockets - no polling required.

We start to see the even more of the power of background tasks when we connect to other microservices.

## Example 3: Create a basic FastAPI server that submits tasks to a Prefect task server

WIP
Install FastAPI version 0.107
See the two files in this directory.
Start the FastAPI server with the following command:

```bash
uvicorn first_fastapi:app --reload
```

Control C to stop the server.

Start the Prefect Task server.

Go to `http://127.0.0.1:8000/ptask` in the browser to submit the task!

You should see the task info in the browser.

## Example 4: Use Docker to run a FastAPI server and a Prefect task server

This guide assumes you aren't using pyenv. If you are, that's great, then you can follow the instructions in the main [README](../README.md) to create the virtual environments.

Step 1: Upgrade Docker to the latest version, if you aren't already using it.

Step 2: Install prefect and fastapi into another virtual environment.

```bash
conda deactivate
conda create -n t2 python=3.12
conda activate t2
```

Step 3: Move into the `fastapi-user-signups` directory.

Step 4: Run `make` to pull the Docker images and build the containers.

Step 5: Run `docker compose up` to start the services.

The services should start up and everything should run.
If you have issues and do some troubleshooting, you can then run the following commands to try to get things working.

```bash
make clean
make
docker compose up
```

Step 5: Send a new user signup to the FastAPI server.

```bash
curl -X POST http://localhost:8000/users --header "Content-Type: application/json" --data '{"email": "chris.g@prefect.io", "name": "Guidry"}'
```

Step 5: Explore the tasks by checking out the Docker containers.

You should see that the task server is running and the FastAPI server is running.

There are multiple services that are engaged when the API is hit.

Check out the Python files and the docker-compose.yml file to see how the services are set up.

## Example 5: Use Docker to run a Flask server and the Prefect task server with Marvin

This example will allow us to ask Marvin questions and get answers from the Flask server.

Step 1: Set up another virtual environment with Flask and Prefect installed.

```bash
conda deactivate
conda create -n t3 python=3.12
conda activate t3
pip install httpx playsound
# I had to install the following on macOS 
pip3 install PyObjC 
```

Step 2: Move into the *flask-task-monitoring* directory.

Step 3: Grab an API key from OpenAI and create an *.openai.env* file in the *flask-task-monitoring* top directory with the following contents:

```
OPENAI_API_KEY=my_api_key_goes_here
```

Step 4: Run `make` to pull the Docker images and build the containers.

Step 5: Run `docker compose up` to start the servers in the containers.

Troubleshoot as needed following the process in Example 3.

Step 5: Submit questions to Marvin via Flask

Use the following command to run the script at in the `ask` file and ask Marvin a question.

```bash
python ask.py "What is the meaning of life?"
```

You should receive an audio response.
Have fun asking Marvin other questions.

There's lots more you can do with Prefect background tasks.
We can't wait to see what you build!
