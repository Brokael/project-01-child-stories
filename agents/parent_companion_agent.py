from config import MODELS, LANGUAGE
from schemas.parent_companion_schema import ParentCompanion
from utils.openai_client import get_openai_client


def generate_parent_companion(
    story_plan,
    story,
    theme_options=None,
    calendar_context=None,
    language=None
):
    if language is None:
        language = LANGUAGE

    with open("prompts/parent_companion_prompt.txt", "r", encoding="utf-8") as file:
        parent_prompt = file.read()

    full_prompt = f"""
{parent_prompt}

Response language: {language}

StoryPlan:
{story_plan}

Story:
{story}

Theme Options:
{theme_options}

Calendar Context:
{calendar_context}
"""

    response = get_openai_client().responses.parse(
        model=MODELS["parent_companion"],
        input=full_prompt,
        text_format=ParentCompanion
    )

    return response.output_parsed
