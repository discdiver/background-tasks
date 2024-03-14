# Exploring Prefect Background Task Examples

This guide will familiarize you with Prefect background task examples.

We'll start by running a Prefect task outside a flow. Then we'll start a task server and run tasks in the background. Next, we'll set up a FastAPI server to submit tasks to the Prefect task server. Then we'll move into Docker with two examples that mimic real use cases with Flask and FastAPI servers.

You can use either Prefect Cloud or a local Prefect server instance for these first examples.

If you're using a local Prefect server instance, you'll need to set the `PREFECT_API_URL` if it isn't already set.
You can save this value to your active Prefect Profile by running the following command in your terminal.

```bash
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```

The Docker examples will use a local Prefect server instance, which you can switch to Prefect Cloud by changing the Docker Compose file settings for the `PREFECT_API_URL`.

## Examples

1. Run a Prefect task outside a flow
2. Start a task server and run tasks in the background
3. Set up a FastAPI server to submit tasks to the Prefect task server
4. Use Docker to run the FastAPI server and the Prefect task server
5. Use Docker to run a Flask server and the Prefect task server with Marvin and ask it questions

## Example 1: Run a Prefect task outside a flow

Step 1: Activate a virtual environment with Prefect 2.16.3 or newer installed.

Here's an example that uses conda.

```bash
conda deactivate
conda create -n t1 python=3.12
conda activate t1
pip install -U prefect
```

Step 2: Set your Prefect profile to use experimental task scheduling and

```bash
prefect config set PREFECT_EXPERIMENTAL_ENABLE_TASK_SCHEDULING=true
```

Step 3: Start your Prefect server instance

```bash
prefect server start --host 0.0.0.0
```

Step 4: Make a file named `greeter1.py` and save the following code in it.

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

You can see the task run in the UI (when the task run page is implemented) or in the local database. To look in the SQLite database, use your favorite interface to SQLite. We use `DB Browser for SQLite` for this example.

Download [here](https://sqlitebrowser.org/dl/) if needed. Install it and open it.

Click *Connect*. Then navigate to your SQLite DB file. It will be in the `~/.prefect` directory by default.

Head to the `task_run` table and you should see all your task runs there. You can scroll down to see your most recent task runs or filter for them.

Hit the refresh button for updates if needed.

Let's now look at using a task server to run tasks in the background.

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

Step 2: Start the task server

Run the script in the terminal.

```bash
python task_server.py
```

The task server is now waiting for runs of the my_background_task task. Let's give it some task runs.

Step 3: Create a file named `task_submitter.py` and save the following code in it.

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

Note that we return the task run info from the submit method. This way we can see the task run ID and other information about the task run.

Step 5: See the task run in the UI

Use the task run UUID to see the task run in the UI. The URL will look like this:

<http://127.0.0.1:4200/task-runs/task-run/3ae4ad3a-d679-4bb5-9e2f-230d281f52ee>

Substitute in your UUID at the end of the URL. This UI navigation experience will be improved in the future.

Step 6: Start another instance of the task server.

In another terminal run:

```bash
python task_server.py
```

Step 7: Submit multiple tasks to the task server with `map`.

Modify the `task_submitter.py` file to submit multiple tasks to the task server.

```python
from task_server import my_b_task

if __name__ == "__main__":
    my_b_task.map(["Ford", "Prefect", "Slartibartfast"])
```

Run the file and watch the work get distributed across both task servers!

Step 8: Shut down the task server with *control* + *c*.

Alright, you're able to submit tasks to a Prefect task server running in the background. This is cool, because we can observe these tasks executing very quickly with websockets - no polling required.

We start to see the real power when we connect to other microservices.

## Example 3

### WIP To be added. Started below. Skip to example 4 for now

Set up a FastAPI server to submit tasks to the Prefect task server

Step-by-step instructions to set up a FastAPI server with Prefect background tasks.

Step 1: Install prefect and fastapi into another virtual environment

```bash
conda deactivate
conda create -n t2 python=3.12
conda activate t2
pip install prefect fastapi==0.107
```

This script will submit the task to the running Prefect task server and print the result with al

Feel free to check out the task in the database or check it out in the UI at

In Prefect Cloud the URL looks like this with the UUID for the task run substituted at the end.

<https://app.prefect.cloud/account/9b649228-0419-40e1-9e0d-44954b5c0ab6/workspace/d137367a-5055-44ff-b91c-6f7366c9e4c4/task-runs/task-run/710c1ba4-5c9e-46f9-983e-0b6d685cfd33>

Let's move on to using Docker with services with a FastAPI server to submit tasks to the Prefect task server.

## Example 4: Use Docker to run the FastAPI server and the Prefect task server

This guide assumes you aren't using pyenv. If you are, that's great then you can follow the instructions in the repo README to create the virtual environments.

Step 1: Upgrade Docker to the latest version, if you aren't already using it.

Step 2: Install prefect and fastapi into another virtual environment

```bash
conda deactivate
conda create -n t2 python=3.12
conda activate t2
pip install prefect fastapi==0.107
```

Step 3: Clone the Prefect Background Task Examples repository if you haven't yet. Move into the `fastapi-user-signups` directory.

Step 4: Run `make` to pull the Docker images and build the containers.

The services should start up and everything should run.

If you have issues and do some troubleshooting, you can then run the following commands to try to get things working.

```bash
make clean
make build
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
pip install prefect flask marvin playsound
# I had to install the following on macOS
pip3 install PyObjC 
```

Step 2: Move into the `flask-task-monitoring` directory

Step 3: Grab an API key from OpenAI and create an .openai.env file in the `flask-task-monitoring` top folder with the following contents:

```
OPENAI_API_KEY=my_api_key_goes_here
```

Step 4: Run `make` to pull the Docker images and build the containers.

Troubleshoot as needed following the process above.

Step 5: Submit questions to Marvin via Flask

Use the following command to run the script at in the `ask` file and ask Marvin a question.

```bash
./ask "What is the meaning of life?"
```

Have fun asking Marvin other questions. You should receive an audio response.
