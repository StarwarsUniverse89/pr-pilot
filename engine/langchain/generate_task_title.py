import logging

from django.conf import settings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


system_message = """
You generate titles for tasks.
You will get a Github issue description and a user request and create a title for the task that needs to be done.

# Examples
Here are examples of what good task titles look like

- "Fix the broken login page"
- "Add a new feature to the dashboard"
- "Update the API documentation"
- "Refactor the user management code"

# Issue description
{issue_description}

# User request
{user_request}

Task Title:
"""
prompt = PromptTemplate(
    template=system_message,
    input_variables=["issue_description", "user_request"],
)


parser = StrOutputParser()
model = ChatOpenAI(
    model=settings.DEFAULT_GPT_MODEL,
    openai_api_key=settings.OPENAI_API_KEY,
    temperature=0,
)
chain = prompt | model | parser


def generate_task_title(issue_description: str, user_request: str) -> str:
    return (
        chain.invoke(
            {"issue_description": issue_description, "user_request": user_request}
        )
        .lstrip('"')
        .rstrip('"')[:200]
    )
