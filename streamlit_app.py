from datetime import date
import importlib

import streamlit as st

import agents.calendar_context_agent as calendar_context_agent
import agents.theme_selector_agent as theme_selector_agent
import orchestrator.story_pipeline as story_pipeline
from schemas.calendar_event_schema import CalendarContext
from utils.pdf_export import export_story_pdf


st.set_page_config(
    page_title="Bedtime Story Generator",
    page_icon=":material/menu_book:",
    layout="centered"
)


STEPS = [
    "Event & Language",
    "Theme Selection",
    "Generate",
    "Story",
    "Parents Guide",
    "Export"
]

LANGUAGE_OPTIONS = ["Français", "English", "Hebrew", "Other"]

UI_TEXT = {
    "Français": {
        "app_title": "Generateur d'histoire du soir",
        "intro": "Une session guidee pour creer une histoire calme et familiale.",
        "language": "Langue de l'histoire",
        "custom_language": "Langue souhaitee",
        "load_events": "Charger les evenements",
        "choose_event": "Choisir l'evenement cible",
        "generate_themes": "Generer les themes",
        "choose_theme": "Choisir un theme",
        "generate_story": "Generer l'histoire",
        "story": "Histoire",
        "parents_guide": "Guide Parents",
        "create_pdf": "Creer le PDF",
        "download_pdf": "Telecharger le PDF",
        "back": "Retour",
        "next": "Suivant"
    },
    "English": {
        "app_title": "Bedtime Story Generator",
        "intro": "A guided client session for creating a calm family story.",
        "language": "Story language",
        "custom_language": "Desired language",
        "load_events": "Load events",
        "choose_event": "Choose the target event",
        "generate_themes": "Generate themes",
        "choose_theme": "Choose a theme",
        "generate_story": "Generate Story",
        "story": "Story",
        "parents_guide": "Parents Guide",
        "create_pdf": "Create PDF",
        "download_pdf": "Download PDF",
        "back": "Back",
        "next": "Next"
    },
    "Hebrew": {
        "app_title": "מחולל סיפור לפני השינה",
        "intro": "תהליך מודרך ליצירת סיפור משפחתי רגוע.",
        "language": "שפת הסיפור",
        "custom_language": "שפה רצויה",
        "load_events": "טעינת אירועים",
        "choose_event": "בחירת האירוע",
        "generate_themes": "יצירת נושאים",
        "choose_theme": "בחירת נושא",
        "generate_story": "יצירת סיפור",
        "story": "סיפור",
        "parents_guide": "מדריך להורים",
        "create_pdf": "יצירת PDF",
        "download_pdf": "הורדת PDF",
        "back": "חזרה",
        "next": "הבא"
    }
}


def init_session_state():
    defaults = {
        "current_step": 0,
        "calendar_context": None,
        "selected_event": None,
        "language_choice": "Français",
        "custom_language": "",
        "selected_language": "Français",
        "theme_options": None,
        "selected_theme": None,
        "pipeline_result": None,
        "pdf_path": None,
        "last_event_key": None,
        "last_language": "Français"
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def text(key):
    labels = UI_TEXT.get(st.session_state.selected_language, UI_TEXT["English"])
    return labels.get(key, UI_TEXT["English"][key])


def event_label(event):
    hebrew_name = f" / {event.hebrew_name}" if event.hebrew_name else ""
    return f"{event.start_date} - {event.name}{hebrew_name}"


def theme_label(theme):
    return f"{theme.option_number}. {theme.title}"


def selected_event_context():
    return CalendarContext(upcoming_events=[st.session_state.selected_event])


def parse_event_date(event):
    return date.fromisoformat(event.start_date[:10])


def has_current_event_shape(calendar_context):
    if calendar_context is None:
        return False

    events = calendar_context.upcoming_events

    if len(events) != 3:
        return False

    today = date.today()
    event_dates = [parse_event_date(event) for event in events]

    return event_dates[0] < today and all(
        event_date >= today for event_date in event_dates[1:]
    )


def load_event_choices():
    module = importlib.reload(calendar_context_agent)
    return module.get_calendar_context()


def load_theme_options(calendar_context, language):
    module = importlib.reload(theme_selector_agent)
    return module.generate_theme_options(calendar_context, language=language)


def run_generation_pipeline(calendar_context, theme_options, selected_theme, language):
    module = importlib.reload(story_pipeline)
    return module.run_story_pipeline(
        calendar_context=calendar_context,
        theme_options=theme_options,
        selected_theme=selected_theme,
        language=language
    )


def reset_generated_outputs():
    st.session_state.theme_options = None
    st.session_state.selected_theme = None
    st.session_state.pipeline_result = None
    st.session_state.pdf_path = None


def reset_story_outputs():
    st.session_state.pipeline_result = None
    st.session_state.pdf_path = None


def show_progress():
    current_step = st.session_state.current_step
    st.progress((current_step + 1) / len(STEPS))
    st.caption(f"Step {current_step + 1} of {len(STEPS)}: {STEPS[current_step]}")


def show_event_summary(event):
    st.subheader(event.name)
    st.write(f"Date: {event.start_date}")

    if event.hebrew_name:
        st.write(f"Hebrew name: {event.hebrew_name}")

    st.write(event.description)


def show_theme_card(theme):
    with st.container(border=True):
        st.subheader(theme.title)
        st.write(f"Source event: {theme.source_event}")
        st.write(f"Core value: {theme.core_value}")
        st.write(f"Story angle: {theme.story_angle}")
        st.write(theme.description)


def show_selected_theme(theme):
    st.subheader(theme.title)
    st.write(f"Source event: {theme.source_event}")
    st.write(f"Core value: {theme.core_value}")
    st.write(f"Story angle: {theme.story_angle}")


def show_parents_guide(parent_companion):
    st.header(text("parents_guide"))
    st.subheader("Linked event")
    st.write(parent_companion.linked_event)

    st.subheader("Core values")
    for value in parent_companion.core_values:
        st.write(f"- {value}")

    st.subheader("Connection to the story")
    st.write(parent_companion.event_explanation)

    st.subheader("Story elements to understand")
    for symbol in parent_companion.symbol_explanations:
        st.write(f"- {symbol.story_element}: {symbol.symbolic_meaning}")


def go_back():
    st.session_state.current_step = max(0, st.session_state.current_step - 1)


def go_next():
    st.session_state.current_step = min(
        len(STEPS) - 1,
        st.session_state.current_step + 1
    )


def show_navigation(can_go_next=True):
    left, right = st.columns(2)

    with left:
        st.button(
            text("back"),
            on_click=go_back,
            disabled=st.session_state.current_step == 0
        )

    with right:
        st.button(
            text("next"),
            on_click=go_next,
            disabled=not can_go_next or st.session_state.current_step == len(STEPS) - 1
        )


def event_and_language_step():
    st.header(STEPS[0])

    language_choice = st.radio(
        text("language"),
        LANGUAGE_OPTIONS,
        index=LANGUAGE_OPTIONS.index(st.session_state.language_choice),
        horizontal=True
    )
    st.session_state.language_choice = language_choice

    if language_choice == "Other":
        custom_language = st.text_input(
            text("custom_language"),
            value=st.session_state.custom_language
        )
        st.session_state.custom_language = custom_language
        selected_language = custom_language.strip() or "Other"
    else:
        selected_language = language_choice

    if selected_language != st.session_state.last_language:
        st.session_state.selected_language = selected_language
        st.session_state.last_language = selected_language
        reset_generated_outputs()
    else:
        st.session_state.selected_language = selected_language

    if st.button(text("load_events")):
        with st.spinner("Loading event choices..."):
            st.session_state.calendar_context = load_event_choices()
            st.session_state.selected_event = None
            reset_generated_outputs()

    if st.session_state.calendar_context:
        events = st.session_state.calendar_context.upcoming_events
        selected_event = st.radio(
            text("choose_event"),
            events,
            format_func=event_label
        )
        st.session_state.selected_event = selected_event

        event_key = event_label(selected_event)
        if event_key != st.session_state.last_event_key:
            st.session_state.last_event_key = event_key
            reset_generated_outputs()

        show_event_summary(selected_event)

    has_language = (
        st.session_state.language_choice != "Other"
        or bool(st.session_state.custom_language.strip())
    )
    show_navigation(
        can_go_next=st.session_state.selected_event is not None and has_language
    )


def theme_selection_step():
    st.header(STEPS[1])

    show_event_summary(st.session_state.selected_event)

    if st.button(text("generate_themes")):
        with st.spinner("Generating theme options..."):
            st.session_state.theme_options = load_theme_options(
                selected_event_context(),
                st.session_state.selected_language
            )
            st.session_state.selected_theme = None
            reset_story_outputs()

    if st.session_state.theme_options:
        for theme in st.session_state.theme_options.options:
            show_theme_card(theme)

        selected_theme = st.radio(
            text("choose_theme"),
            st.session_state.theme_options.options,
            format_func=theme_label
        )

        if selected_theme != st.session_state.selected_theme:
            st.session_state.selected_theme = selected_theme
            reset_story_outputs()

    show_navigation(can_go_next=st.session_state.selected_theme is not None)


def generate_step():
    st.header(STEPS[2])

    st.subheader("Selected event")
    show_event_summary(st.session_state.selected_event)

    st.subheader("Selected theme")
    show_selected_theme(st.session_state.selected_theme)

    if st.button(text("generate_story")):
        with st.spinner("Generating, reviewing, rewriting, and saving the story..."):
            st.session_state.pipeline_result = run_generation_pipeline(
                selected_event_context(),
                st.session_state.theme_options,
                st.session_state.selected_theme,
                st.session_state.selected_language
            )
            st.session_state.pdf_path = None

    show_navigation(can_go_next=st.session_state.pipeline_result is not None)


def story_step():
    st.header(text("story"))

    final_story = st.session_state.pipeline_result[4]
    st.write(final_story)

    show_navigation()


def parents_guide_step():
    parent_companion = st.session_state.pipeline_result[6]
    show_parents_guide(parent_companion)
    show_navigation()


def export_step():
    st.header(STEPS[5])

    (
        calendar_context,
        theme_options,
        selected_theme,
        story_plan,
        final_story,
        final_review,
        parent_companion,
        saved_file
    ) = st.session_state.pipeline_result

    if st.button(text("create_pdf")):
        with st.spinner("Creating PDF..."):
            st.session_state.pdf_path = export_story_pdf(
                selected_event=st.session_state.selected_event,
                selected_theme=selected_theme,
                final_story=final_story,
                parent_companion=parent_companion,
                language=st.session_state.selected_language,
                story_title=story_plan.title
            )

    if st.session_state.pdf_path:
        st.write(f"PDF saved to: {st.session_state.pdf_path}")

        with open(st.session_state.pdf_path, "rb") as pdf_file:
            st.download_button(
                text("download_pdf"),
                data=pdf_file,
                file_name=st.session_state.pdf_path.name,
                mime="application/pdf"
            )

    show_navigation(can_go_next=False)


def main():
    init_session_state()

    if not has_current_event_shape(st.session_state.calendar_context):
        st.session_state.calendar_context = None
        st.session_state.selected_event = None
        st.session_state.current_step = 0
        reset_generated_outputs()

    st.title(text("app_title"))
    st.write(text("intro"))
    show_progress()

    if st.session_state.current_step == 0:
        event_and_language_step()
    elif st.session_state.current_step == 1:
        theme_selection_step()
    elif st.session_state.current_step == 2:
        generate_step()
    elif st.session_state.current_step == 3:
        story_step()
    elif st.session_state.current_step == 4:
        parents_guide_step()
    elif st.session_state.current_step == 5:
        export_step()


if __name__ == "__main__":
    main()
