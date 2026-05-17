from config import MODELS, LANGUAGE
from openai import OpenAI
from dotenv import load_dotenv
from schemas.story_review_schema import StoryReview

import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def review_story(story_plan, story):

    with open("prompts/reviewer_prompt.txt", "r", encoding="utf-8") as file:
        reviewer_prompt = file.read()

    full_prompt = f"""
{reviewer_prompt}

Review language: {LANGUAGE}

StoryPlan:
{story_plan}

Story:
{story}
"""

    response = client.responses.parse(
        model=MODELS["reviewer"],
        input=full_prompt,
        text_format=StoryReview
    )

    review = response.output_parsed

    return review