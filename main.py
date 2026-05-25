from orchestrator.story_pipeline import run_story_pipeline
from utils.formatters import format_parent_companion


def is_running_in_streamlit():
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        return get_script_run_ctx() is not None
    except Exception:
        return False


def main():

    (
        calendar_context,
        theme_options,
        selected_theme,
        story_plan,
        story,
        review,
        parent_companion,
        saved_file
    ) = run_story_pipeline()

    print("\n=== CALENDAR CONTEXT ===\n")
    print(calendar_context)

    print("\n=== THEME OPTIONS ===\n")
    print(theme_options)

    print("\n=== SELECTED THEME ===\n")
    print(selected_theme)

    print("\n=== STORY PLAN ===\n")
    print(story_plan)

    print("\n=== FINAL STORY ===\n")
    print(story)

    print("\n=== FINAL REVIEW ===\n")
    print(review)

    print(format_parent_companion(parent_companion))

    print(f"\n=== SAVED TO ===\n{saved_file}")


if __name__ == "__main__":
    if is_running_in_streamlit():
        from streamlit_app import main as streamlit_main

        streamlit_main()
    else:
        main()
