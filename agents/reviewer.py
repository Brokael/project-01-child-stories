from config import MODELS, LANGUAGE
from schemas.story_review_schema import StoryReview
from utils.openai_client import get_openai_client


def review_story(story_plan, story, language=None):
    if language is None:
        language = LANGUAGE

    with open("prompts/reviewer_prompt.txt", "r", encoding="utf-8") as file:
        reviewer_prompt = file.read()

    full_prompt = f"""
{reviewer_prompt}

Review language: {language}

StoryPlan:
{story_plan}

Story:
{story}
"""

    response = get_openai_client().responses.parse(
        model=MODELS["reviewer"],
        input=full_prompt,
        text_format=StoryReview
    )

    review = response.output_parsed

    return review
