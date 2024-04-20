(userguide)=
# User Guide

Welcome to PR Pilot!

This guide will help you get started with PR Pilot and show you how to use it to automate your tasks.

## Installation

If you haven't done so, [install PR Pilot](https://github.com/apps/pr-pilot-ai/installations/new) into your repository.

## Automating your Project

Depending on your needs and skill level, you can use PR Pilot in different ways:

### Zero-Config, No-Code

If you're new to AI and automation, you can use your **[Smart Project Template](https://github.com/PR-Pilot-AI/smart-project-template)** to get started.
It comes with fully-customizable, no-code [Github workflows](https://docs.github.com/en/actions/using-workflows) out-of-the-box.


### Low-Code Smart Actions

If you're comfortable with Github Actions and want to create your own automations, you can use our **[Smart Actions](https://github.com/PR-Pilot-AI/smart-actions)** to create your own workflows.
These actions are hand-crafted using state-of-the-art prompt engineering techniques and let you automate your Github projects in powerful new ways.


### More Control: Python SDK

To use PR Pilot in your own tools and integrations, you can use the [Python SDK](https://github.com/PR-Pilot-AI/pr-pilot-python):

```bash
pip install pr-pilot
```

Use the `create_task`, `get_task` and `wait_for_result` functions to automate your Github project:

```python
from pr_pilot.util import create_task, wait_for_result

github_repo = "PR-Pilot-AI/pr-pilot"
task = create_task(github_repo, "Summarize the README file and create a Github issue with the result.")
result = wait_for_result(task)
print(result)
```

The Python SDK works great for creating [powerful Github Actions](https://github.com/PR-Pilot-AI/smart-actions).


### Using the REST API

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



### Talk to the Agent in Github Comments

PR Pilot will create issues and PRs for you. To stay in the flow, just use the `/pilot` command followed by a description of the task you want to perform.


![First pilot command](img/first_command.png)

The bot will turn your comment into a link to your [dashboard](https://app.pr-pilot.ai), where you can monitor the task's progress.


## Monitoring Tasks

While a task is running, **PR Pilot** will create events that you can follow in the [dashboard](https://app.pr-pilot.ai/dashboard/tasks/):

![PR Pilot](img/how_it_works_dashboard.png)

You'll also get a detailed overview of how your credits were spent.

![Monitoring PR Pilot](img/how_it_works_cost.png)