from config import MODELS, LANGUAGE
from openai import OpenAI
from dotenv import load_dotenv
from schemas.parent_companion_schema import ParentCompanion
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_parent_companion(story_plan, story, theme_options=None, calendar_context=None):

    with open("prompts/parent_companion_prompt.txt", "r", encoding="utf-8") as file:
        parent_prompt = file.read()

    full_prompt = f"""
{parent_prompt}

Response language: {LANGUAGE}

StoryPlan:
{story_plan}

Story:
{story}

Theme Options:
{theme_options}

Calendar Context:
{calendar_context}
"""

    response = client.responses.parse(
        model=MODELS["parent_companion"],
        input=full_prompt,
        text_format=ParentCompanion
    )

    return response.output_parsed