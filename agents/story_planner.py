from config import MODELS
from openai import OpenAI
from dotenv import load_dotenv
from schemas.story_plan_schema import StoryPlan
from story_parameters import STORY_PARAMETERS
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_story_plan(selected_theme=None):

    with open("prompts/story_planner_prompt.txt", "r", encoding="utf-8") as file:
        planner_prompt = file.read()

    full_prompt = f"""
{planner_prompt}

Use these story parameters:
{STORY_PARAMETERS}

Selected Theme:
{selected_theme}
"""

    response = client.responses.parse(
        model=MODELS["story_planner"],
        input=full_prompt,
        text_format=StoryPlan
    )

    return response.output_parsed