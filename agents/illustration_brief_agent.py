from config import MODELS, LANGUAGE
from schemas.scene_brief_schema import SceneBrief
from utils.openai_client import get_openai_client


def generate_scene_brief(story, selected_theme=None, selected_event=None, language=None):
    if language is None:
        language = LANGUAGE

    full_prompt = f"""
Create one compact illustration scene brief for a single bedtime story image.

Rules:
- Pick one clear key scene from the story.
- Keep the brief short and concrete.
- No text, letters, logos, captions, or speech bubbles in the image.
- Keep it gentle, child-safe, warm, and suitable for ages 5-7.
- Avoid scary, violent, realistic, or overly complex imagery.
- Response language: {language}

Selected event:
{selected_event}

Selected theme:
{selected_theme}

Story:
{story}
"""

    response = get_openai_client().responses.parse(
        model=MODELS["illustration_brief"],
        input=full_prompt,
        text_format=SceneBrief
    )

    return response.output_parsed
