# Project 01 - Child Stories

This project generates bedtime stories for children with an agentic pipeline.
It combines calendar context, theme selection, story planning, story writing,
review, rewriting, and a short parent companion note.

The current target is a warm, calm story for children aged 5-7, written in
French by default.

## Project Goal

The goal is to explore a small multi-agent writing workflow:

- use external context to inspire a story theme;
- produce a structured story plan;
- generate a child-friendly story;
- review the story against quality criteria;
- rewrite the story based on feedback;
- save the final output and supporting context for later inspection.

The project is intentionally simple and educational. It is useful for learning
how to compose specialized agents into a deterministic pipeline while keeping
prompts, schemas, orchestration, and output formatting separated.

## Current Pipeline

The main entry point is `main.py`, which calls `run_story_pipeline()` from
`orchestrator/story_pipeline.py`.

Current flow:

1. Fetch upcoming Jewish calendar events from Hebcal.
2. Generate several story theme options based on that calendar context.
3. Select one theme using `SELECTED_THEME_OPTION` from `config.py`.
4. Generate a structured story plan.
5. Generate the first story draft.
6. Review the story and assign an overall score.
7. Run at least one rewrite pass, then continue rewriting until the review
   score reaches `MIN_REVIEW_SCORE` or `MAX_REWRITE_PASSES` is reached.
8. Generate a parent companion note explaining values, symbols, and the event
   connection.
9. Save the full run output to the `stories/` folder.
10. Print the main artifacts to the console.

Logs are written to `logs/app.log`.

## Agents and Roles

- `calendar_context_agent.py`
  Fetches upcoming Jewish calendar events from Hebcal and converts them into a
  `CalendarContext` schema.

- `theme_selector_agent.py`
  Uses the calendar context to propose multiple story themes. Its structured
  output is defined by `schemas/theme_option_schema.py`.

- `story_planner.py`
  Turns the selected theme and `STORY_PARAMETERS` into a structured story plan.
  Its output is defined by `schemas/story_plan_schema.py`.

- `story_writer.py`
  Writes the initial story from the story plan.

- `reviewer.py`
  Reviews the story and returns a structured score, strengths, issues, and
  suggested improvements. Its output is defined by
  `schemas/story_review_schema.py`.

- `story_rewriter.py`
  Rewrites the story using the current story, the story plan, and reviewer
  feedback.

- `parent_companion_agent.py`
  Creates a parent-facing companion note that explains the story's values,
  symbolic elements, and connection to the selected calendar context.

## How to Run

1. Create and activate a Python virtual environment.

2. Install the required dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with an OpenAI API key:

   ```text
   OPENAI_API_KEY=your_api_key_here
   ```

   For Streamlit Cloud, add the same key in the app's Secrets settings:

   ```toml
   OPENAI_API_KEY = "your_api_key_here"
   ```

4. Review the basic settings in `config.py`:

   - `DEFAULT_MODEL`
   - `LANGUAGE`
   - `MIN_REVIEW_SCORE`
   - `MAX_REWRITE_PASSES`
   - `SELECTED_THEME_OPTION`

5. Run the project:

   ```powershell
   python main.py
   ```

   Or run the simple Streamlit interface:

   ```powershell
   streamlit run streamlit_app.py
   ```

The Streamlit interface guides the user through event and language
selection, theme selection, story generation, optional illustration, the
Parents Guide, and PDF export.

The Event & Language step currently supports two cultural event sources:

- Jewish calendar events from Hebcal.
- Curated Persian cultural events from `data/cultural_events/persian_events.json`.

The Persian source is local for the MVP and focuses on ancient Iranian,
Persian, and Zoroastrian-influenced seasonal traditions. It intentionally
excludes modern political/state holidays and Islamic holidays. Approximate or
variable dates are marked in the data file.

   If Streamlit Cloud is configured to run `main.py`, the app will still route
   to the Streamlit interface. Running `python main.py` locally keeps the
   original command-line pipeline behavior.

The generated story output is saved in `stories/`. Logs are saved in `logs/`.
PDF exports are saved in `exports/`. Optional generated illustrations are
saved in `illustrations/`. These folders are ignored by Git.

Optional illustration generation uses local style reference images from
`assets/style_references/`. Keep a small number of curated reference images in
that folder so deployed environments can reproduce the intended visual style.
The MVP uses one `gpt-image-1` image edit call per story, with `n=1`,
`quality="low"`, `input_fidelity="low"`, and `size="1024x1024"`. `512x512`
would be preferred for cost control, but it is not a supported size for the
current `gpt-image-1` image edit endpoint; `1024x1024` is the smallest valid
square size for this model.

PDF export uses ReportLab with a Unicode-capable system font when available.
It uses `python-bidi` for right-to-left text ordering and `arabic-reshaper` for
Persian/Farsi and Arabic-script glyph shaping. On Streamlit Cloud, DejaVu fonts
are normally available under the system font directories. If deploying to a
minimal environment without Unicode fonts, add a licensed TTF such as Noto Sans
Hebrew or Noto Naskh Arabic to `assets/fonts/`.

## Current Limitations

- Dependencies are listed in `requirements.txt`, but there is no lockfile yet.
- OpenAI client setup and prompt loading are repeated across agents.
- The pipeline returns a long positional tuple instead of a named result object.
- Theme selection is configured by a fixed option number, not user input or an
  automated ranking step.
- The calendar context depends on live network access to Hebcal.
- There are no automated tests yet.
- The output is saved as plain text only.
- Error handling around OpenAI calls is still minimal.
