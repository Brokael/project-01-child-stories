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
IMAGE_INPUT_FIDELITY = "high"
STORY_CONTEXT_LIMIT = 1200
VISUAL_STYLE_PROFILE = """
Minimalist child-friendly storybook illustration.
Soft bedtime atmosphere.
Simple rounded shapes.
Gentle composition.
Low-detail background.
Warm, calm, harmonious palette.
Subtle hand-drawn or painted storybook feeling.
No photorealism.
No complex scenery.
No text, letters, captions, signs, or written words.
Inspired by the local style references without copying them directly.
"""
REFERENCE_STYLE_INSTRUCTIONS = """
The attached input images are local style references from assets/style_references.
Use them as the primary visual style source, not as story content.
Match their overall simplicity, palette, texture, softness, line quality, shape language, and child-friendly mood.
Do not copy a specific character, object, or exact composition from the references.
Prefer broad, rounded silhouettes, quiet negative space, and a soft paper-cut or gouache-like finish.
Avoid 3D render, anime, comic-book style, glossy digital art, realistic people, complex scenery, and dramatic lighting.
"""


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


def compact_story_context(story_text):
    story_text = " ".join(str(story_text).split())

    if len(story_text) <= STORY_CONTEXT_LIMIT:
        return story_text

    return f"{story_text[:STORY_CONTEXT_LIMIT].rstrip()}..."


def build_illustration_prompt(scene_brief, language, story_context=None):
    story_context_section = ""

    if story_context:
        story_context_section = f"""
Selected story context:
{compact_story_context(story_context)}
"""

    return f"""
Create one minimalist bedtime story illustration based on this scene brief.
Use the scene brief as the composition target and the selected story context as continuity support.

Scene title: {scene_brief.scene_title}
Key moment: {scene_brief.key_moment}
Characters: {scene_brief.characters}
Setting: {scene_brief.setting}
Mood: {scene_brief.mood}
Visual details: {scene_brief.visual_details}
{story_context_section}

Style requirements:
- Visual style profile:
{VISUAL_STYLE_PROFILE.strip()}

- Local reference guidance:
{REFERENCE_STYLE_INSTRUCTIONS.strip()}

- Treat the local reference images as more important than generic model style defaults.
- If there is a conflict, keep the story scene content but follow the reference images for visual treatment.
- Keep one clear focal moment from the story.
- Keep the setting sparse and readable.
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

    return image_path.resolve()


def generate_story_illustration(scene_brief, story_title, language, story_context=None):
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
            prompt=build_illustration_prompt(scene_brief, language, story_context),
            n=IMAGE_COUNT,
            size=IMAGE_SIZE,
            quality=IMAGE_QUALITY,
            input_fidelity=IMAGE_INPUT_FIDELITY
        )
    finally:
        for image_file in image_files:
            image_file.close()

    return save_image_from_response(response, story_title)
