from config import MODELS, LANGUAGE
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_story(story_plan):

    with open("prompts/story_writer_prompt.txt", "r", encoding="utf-8") as file:
        writer_prompt = file.read()

    full_prompt = f"""
{writer_prompt}

Write the story in: {LANGUAGE}

StoryPlan:
{story_plan}
"""

    response = client.responses.create(
        model=MODELS["story_writer"],
        input=full_prompt
    )

    return response.output_text