from agents.calendar_context_agent import get_calendar_context
from agents.theme_selector_agent import generate_theme_options
from agents.story_planner import generate_story_plan
from agents.story_writer import generate_story
from agents.reviewer import review_story
from agents.story_rewriter import rewrite_story
from agents.parent_companion_agent import generate_parent_companion
from config import MIN_REVIEW_SCORE, MAX_REWRITE_PASSES, SELECTED_THEME_OPTION
from utils.logger import setup_logger
from datetime import datetime
from pathlib import Path


logger = setup_logger()


def select_theme_option(theme_options):
    for option in theme_options.options:
        if option.option_number == SELECTED_THEME_OPTION:
            return option

    return theme_options.options[0]


def save_story_output(
    story_plan,
    final_story,
    final_review,
    parent_companion,
    calendar_context,
    theme_options,
    selected_theme,
    story_versions,
    review_versions
):
    stories_folder = Path("stories")
    stories_folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = stories_folder / f"story_{timestamp}.txt"

    versions_text = ""

    for index, version in enumerate(story_versions, start=1):
        versions_text += f"""

=== STORY VERSION {index} ===

{version}
"""

    reviews_text = ""

    for index, review in enumerate(review_versions, start=1):
        reviews_text += f"""

=== REVIEW VERSION {index} ===

{review}
"""

    content = f"""
=== CALENDAR CONTEXT ===

{calendar_context}

=== THEME OPTIONS ===

{theme_options}

=== SELECTED THEME ===

{selected_theme}

=== STORY PLAN ===

{story_plan}

{versions_text}

{reviews_text}

=== FINAL STORY ===

{final_story}

=== FINAL REVIEW ===

{final_review}

=== PARENT COMPANION ===

{parent_companion}
"""

    file_path.write_text(content, encoding="utf-8")
    return file_path


def run_story_pipeline():
    logger.info("Starting story pipeline")

    calendar_context = get_calendar_context()
    logger.info("Calendar context generated")

    theme_options = generate_theme_options(calendar_context)
    logger.info("Theme options generated")

    selected_theme = select_theme_option(theme_options)
    logger.info(f"Selected theme option: {selected_theme.option_number} - {selected_theme.title}")

    story_plan = generate_story_plan(selected_theme=selected_theme)
    logger.info("Story plan generated")

    story = generate_story(story_plan)
    logger.info("Initial story generated")

    story_versions = [story]
    review_versions = []

    review = review_story(story_plan, story)
    review_versions.append(review)
    logger.info(f"Initial review score: {review.overall_score}")

    for rewrite_pass in range(1, MAX_REWRITE_PASSES + 1):
        if rewrite_pass > 1 and review.overall_score >= MIN_REVIEW_SCORE:
            logger.info("Quality threshold reached after mandatory rewrite")
            break

        logger.info(f"Rewrite pass {rewrite_pass} started")

        story = rewrite_story(story_plan, story, review)
        story_versions.append(story)

        logger.info(f"Rewrite pass {rewrite_pass} completed")

        review = review_story(story_plan, story)
        review_versions.append(review)

        logger.info(f"Review after rewrite pass {rewrite_pass} score: {review.overall_score}")

    final_story = story
    final_review = review

    parent_companion = generate_parent_companion(
        story_plan=story_plan,
        story=final_story,
        theme_options=theme_options,
        calendar_context=calendar_context
    )
    logger.info("Parent companion generated")

    saved_file = save_story_output(
        story_plan=story_plan,
        final_story=final_story,
        final_review=final_review,
        parent_companion=parent_companion,
        calendar_context=calendar_context,
        theme_options=theme_options,
        selected_theme=selected_theme,
        story_versions=story_versions,
        review_versions=review_versions
    )

    logger.info(f"Story output saved to {saved_file}")

    return (
        calendar_context,
        theme_options,
        selected_theme,
        story_plan,
        final_story,
        final_review,
        parent_companion,
        saved_file
    )