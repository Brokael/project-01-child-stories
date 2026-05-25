from config import MODELS, LANGUAGE
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def rewrite_story(story_plan, story, review, language=None):
    if language is None:
        language = LANGUAGE

    with open("prompts/story_rewriter_prompt.txt", "r", encoding="utf-8") as file:
        rewriter_prompt = file.read()

    full_prompt = f"""
{rewriter_prompt}

Rewrite language: {language}

StoryPlan:
{story_plan}

Current story:
{story}

Reviewer feedback:
{review}
"""

    response = client.responses.create(
        model=MODELS["rewriter"],
        input=full_prompt
    )

    return response.output_text
