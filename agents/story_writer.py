from config import MODELS, LANGUAGE
from utils.openai_client import get_openai_client


def generate_story(story_plan, language=None):
    if language is None:
        language = LANGUAGE

    with open("prompts/story_writer_prompt.txt", "r", encoding="utf-8") as file:
        writer_prompt = file.read()

    full_prompt = f"""
{writer_prompt}

Write the story in: {language}

StoryPlan:
{story_plan}
"""

    response = get_openai_client().responses.create(
        model=MODELS["story_writer"],
        input=full_prompt
    )

    return response.output_text
