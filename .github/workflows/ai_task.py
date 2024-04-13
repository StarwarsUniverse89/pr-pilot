# execute_ai_task.py
import os
from pr_pilot.util import create_task, get_task
import time

commit_message = os.getenv("COMMIT_MESSAGE")
author = os.getenv("AUTHOR")
prompt = f"""
There was a new commit by `{author}` on the main branch. Commit message:

---

{commit_message}

---

If they explicitly mention you and ask you to do something, do it.
Otherwise, just say 'Ignored'.
"""
print(prompt)

task = create_task("PR-Pilot-AI/pr-pilot", prompt)
while task.status != "completed":
    task = get_task(task.id)
    time.sleep(5)

print(f"PR Pilot says:\n\n{task.result}")
