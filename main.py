from agents.story_planner import generate_story_plan
from agents.story_writer import generate_story
from agents.reviewer import review_story
from agents.story_rewriter import rewrite_story
from config import MIN_REVIEW_SCORE, MAX_REWRITE_PASSES
from datetime import datetime
from pathlib import Path


def save_story_output(story_plan, story, review):
    stories_folder = Path("stories")
    stories_folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = stories_folder / f"story_{timestamp}.txt"

    content = f"""
=== STORY PLAN ===

{story_plan}

=== FINAL STORY ===

{story}

=== FINAL REVIEW ===

{review}
"""

    file_path.write_text(content, encoding="utf-8")
    return file_path


def main():

    story_plan = generate_story_plan()

    print("\n=== STORY PLAN ===\n")
    print(story_plan)

    story = generate_story(story_plan)

    for attempt in range(1, MAX_REWRITE_PASSES + 1):
        print(f"\n=== REVIEW PASS {attempt} ===\n")

        review = review_story(story_plan, story)
        print(review)

        if review.overall_score >= MIN_REVIEW_SCORE:
            print("\nQuality threshold reached.")
            break

        print("\nScore below threshold. Rewriting story...\n")
        story = rewrite_story(story_plan, story, review)

    print("\n=== FINAL STORY ===\n")
    print(story)

    saved_file = save_story_output(story_plan, story, review)

    print(f"\n=== SAVED TO ===\n{saved_file}")


if __name__ == "__main__":
    main()