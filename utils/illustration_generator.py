from datetime import datetime
from pathlib import Path
import base64
import re

from config import MODELS
from utils.openai_client import get_openai_client


STYLE_REFERENCES_FOLDER = Path("assets/style_references")
ILLUSTRATIONS_FOLDER = Path("illustrations")
REFERENCE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
IMAGE_COUNT = 1
IMAGE_SIZE = "1024x1024"
IMAGE_QUALITY = "low"
IMAGE_INPUT_FIDELITY = "low"


def slugify(value):
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "story"


def get_style_reference_paths():
    if not STYLE_REFERENCES_FOLDER.exists():
        return []

    return [
        path
        for path in sorted(STYLE_REFERENCES_FOLDER.iterdir())
        if path.suffix.lower() in REFERENCE_EXTENSIONS
    ]


def build_illustration_prompt(scene_brief, language):
    return f"""
Create one minimalist bedtime story illustration based on this scene brief.

Scene title: {scene_brief.scene_title}
Key moment: {scene_brief.key_moment}
Characters: {scene_brief.characters}
Setting: {scene_brief.setting}
Mood: {scene_brief.mood}
Visual details: {scene_brief.visual_details}

Style requirements:
- Follow the visual style, palette, texture, and simplicity of the provided reference images.
- Gentle children's book illustration.
- Minimalist composition with soft shapes and calm negative space.
- Warm, reassuring, non-scary, and age-appropriate for ages 5-7.
- No text, letters, captions, logos, watermarks, frames, speech bubbles, or UI elements.
- Do not depict realistic identifiable people.
- Keep the image directly related to the selected story scene.

Language context for any cultural interpretation: {language}
"""


def make_illustration_filename(story_title):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    return f"{timestamp}_{slugify(story_title)}.png"


def save_image_from_response(response, story_title):
    ILLUSTRATIONS_FOLDER.mkdir(exist_ok=True)
    image_path = ILLUSTRATIONS_FOLDER / make_illustration_filename(story_title)

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    image_path.write_bytes(image_bytes)

    return image_path


def generate_story_illustration(scene_brief, story_title, language):
    reference_paths = get_style_reference_paths()

    if not reference_paths:
        raise RuntimeError(
            "No style reference images found in assets/style_references."
        )

    image_files = []

    try:
        for reference_path in reference_paths:
            image_files.append(reference_path.open("rb"))

        response = get_openai_client().images.edit(
            model=MODELS["illustration_image"],
            image=image_files,
            prompt=build_illustration_prompt(scene_brief, language),
            n=IMAGE_COUNT,
            size=IMAGE_SIZE,
            quality=IMAGE_QUALITY,
            input_fidelity=IMAGE_INPUT_FIDELITY
        )
    finally:
        for image_file in image_files:
            image_file.close()

    return save_image_from_response(response, story_title)
