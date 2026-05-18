from openai import OpenAI
from dotenv import load_dotenv
from config import MODELS
from schemas.theme_option_schema import ThemeOptions
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_theme_options(calendar_context):

    with open("prompts/theme_selector_prompt.txt", "r", encoding="utf-8") as file:
        theme_prompt = file.read()

    full_prompt = f"""
{theme_prompt}

Calendar Context:
{calendar_context}
"""

    response = client.responses.parse(
        model=MODELS["theme_selector"],
        input=full_prompt,
        text_format=ThemeOptions
    )

    return response.output_parsed


if __name__ == "__main__":

    from agents.calendar_context_agent import get_calendar_context

    context = get_calendar_context()

    theme_options = generate_theme_options(context)

    print("\n=== THEME OPTIONS ===\n")
    print(theme_options)