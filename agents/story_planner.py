from config import MODELS
from openai import OpenAI
from dotenv import load_dotenv
from schemas.story_plan_schema import StoryPlan
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_story_plan():
    print("DEBUG: structured story planner is running")
    with open("prompts/story_planner_prompt.txt", "r", encoding="utf-8") as file:
        planner_prompt = file.read()

    response = client.responses.parse(
        model=MODELS["story_planner"],
        input=planner_prompt,
        text_format=StoryPlan
    )

    print(response)
    story_plan = response.output_parsed

    print(type(story_plan))
    print(story_plan)
    
    return story_plan