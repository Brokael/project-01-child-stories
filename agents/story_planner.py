from config import MODELS, LANGUAGE
from schemas.story_plan_schema import StoryPlan
from story_parameters import STORY_PARAMETERS
from utils.openai_client import get_openai_client


def generate_story_plan(selected_theme=None, language=None):
    if language is None:
        language = LANGUAGE

    with open("prompts/story_planner_prompt.txt", "r", encoding="utf-8") as file:
        planner_prompt = file.read()

    full_prompt = f"""
{planner_prompt}

Use these story parameters:
{STORY_PARAMETERS}

Story language:
{language}

Selected Theme:
{selected_theme}
"""

    response = get_openai_client().responses.parse(
        model=MODELS["story_planner"],
        input=full_prompt,
        text_format=StoryPlan
    )

    return response.output_parsed
