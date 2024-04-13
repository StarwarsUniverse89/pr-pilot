(userguide)=
# User Guide

Welcome to PR Pilot!

This guide will help you get started with PR Pilot and show you how to use it to automate your tasks.

## Installation

First, [install PR Pilot](https://github.com/apps/pr-pilot-ai) into your repository, then follow the instructions below to create and monitor tasks.

## Creating Tasks

PR Pilot is a **text-to-task** platform, which means you simply describe what you want to do in natural language, and PR Pilot will take care of the rest using its [capabilities](./capabilities.md).

You can give it new tasks in various ways.

### Github Comments

To create a task, simply comment on an issue or PR with the `/pilot` command followed by a description of the task you want to perform.


![First pilot command](img/first_command.png)

The bot will turn your comment into a link to your [dashboard](https://app.pr-pilot.ai), where you can monitor the task's progress.

### API

The PR Pilot API allows you to trigger tasks using your own tools and integrations.

1. Create a new API Key in the PR Pilot [dashboard](https://app.pr-pilot.ai/dashboard/api-keys/).
2. Use the API Key to authenticate your requests to the [PR Pilot API](https://app.pr-pilot.ai/api/swagger-ui/).

Example:
```bash
curl -X POST 'https://app.pr-pilot.ai/api/tasks/' \
-H 'Content-Type: application/json' \
-H 'X-Api-Key: YOUR_API_KEY_HERE' \
-d '{
    "prompt": "Properly format the README.md and add emojis",
    "github_repo": "owner/repo"
}'
```


### Python SDK

Install the [Python SDK](https://github.com/PR-Pilot-AI/pr-pilot-python) using pip:

```bash
pip install pr-pilot
```

Use the `create_task` and `get_task` functions to automate your Github project:

```python
import time

from pr_pilot.util import create_task, get_task

task = create_task("PR-Pilot-AI/pr-pilot", "Summarize the README file and create a Github issue with the result.")

while task.status != "completed":
    print(f"Waiting for task to complete. Status: {task.status}")
    task = get_task(task.id)
    time.sleep(5)
    
print(f"Task completed. Result:\n\n{task.result}")
```

The Python SDK works great for creating [powerful Github Actions](https://github.com/PR-Pilot-AI/pr-pilot/blob/main/.github/workflows/ai_task.py).

### Github Actions

You can create [powerful automations](https://github.com/PR-Pilot-AI/pr-pilot/blob/main/.github/workflows/ai_task_trigger.yml) by combining PR Pilot with Github Actions. Create a secret in your repository with your PR Pilot API Key, then add a new workflow file to your repository.

```yaml
name: AI Task Trigger

on:
  push:
    branches:
      - main

jobs:
  trigger-ai-task:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install PR Pilot SDK
        run: pip install pr-pilot
      - name: Execute AI Task
        env:
          COMMIT_MESSAGE: ${{ github.event.head_commit.message }}
          AUTHOR: ${{ github.event.head_commit.author.username }}
          PR_PILOT_API_KEY: ${{ secrets.PR_PILOT_API_KEY }}
        run: python .github/workflows/ai_task.py
```

### Dashboard

Soon you'll be able to create tasks directly from the [dashboard](https://app.pr-pilot.ai/dashboard/tasks/).


### Slack

Soon, we'll show you how to create tasks directly from Slack.

### via Zapier

Soon, we'll show you how to create tasks via Zapier.

## Monitoring Tasks

While a task is running, **PR Pilot** will create events that you can follow in the [dashboard](https://app.pr-pilot.ai/dashboard/tasks/):

![PR Pilot](img/how_it_works_dashboard.png)

You'll also get a detailed overview of how your credits were spent.

![Monitoring PR Pilot](img/how_it_works_cost.png)