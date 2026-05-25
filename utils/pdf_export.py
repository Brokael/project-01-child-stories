from datetime import datetime
from pathlib import Path
import re
from xml.sax.saxutils import escape


SECTION_LABELS = {
    "Français": {
        "title": "Histoire du soir",
        "event": "Evenement choisi",
        "theme": "Theme choisi",
        "story": "Histoire finale",
        "parents": "Guide Parents",
        "date": "Date",
        "hebrew_name": "Nom hebreu",
        "source_event": "Evenement source",
        "core_value": "Valeur principale",
        "story_angle": "Angle de l'histoire",
        "linked_event": "Evenement lie",
        "core_values": "Valeurs",
        "story_connection": "Lien avec l'histoire",
        "symbols": "Elements a comprendre"
    },
    "English": {
        "title": "Bedtime Story",
        "event": "Selected Event",
        "theme": "Selected Theme",
        "story": "Final Story",
        "parents": "Parents Guide",
        "date": "Date",
        "hebrew_name": "Hebrew name",
        "source_event": "Source event",
        "core_value": "Core value",
        "story_angle": "Story angle",
        "linked_event": "Linked event",
        "core_values": "Core values",
        "story_connection": "Connection to the story",
        "symbols": "Story elements to understand"
    },
    "Hebrew": {
        "title": "סיפור לפני השינה",
        "event": "אירוע נבחר",
        "theme": "נושא נבחר",
        "story": "הסיפור הסופי",
        "parents": "מדריך להורים",
        "date": "תאריך",
        "hebrew_name": "שם עברי",
        "source_event": "אירוע מקור",
        "core_value": "ערך מרכזי",
        "story_angle": "זווית הסיפור",
        "linked_event": "אירוע קשור",
        "core_values": "ערכים",
        "story_connection": "קשר לסיפור",
        "symbols": "מרכיבים להבנה"
    }
}


def get_labels(language):
    return SECTION_LABELS.get(language, SECTION_LABELS["English"])


def slugify(value):
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "story"


def make_pdf_filename(selected_event, story_title):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    event_slug = slugify(selected_event.name)
    title_slug = slugify(story_title)
    return f"{timestamp}_{event_slug}_{title_slug}.pdf"


def add_heading(story, text, style):
    story.append(style(text))


def add_paragraph(story, text, style, spacer):
    if text:
        clean_text = escape(str(text)).replace("\n", "<br/>")
        clean_text = clean_text.replace("&lt;br/&gt;", "<br/>")
        story.append(style(clean_text))
        story.append(spacer)


def export_story_pdf(
    selected_event,
    selected_theme,
    final_story,
    parent_companion,
    language,
    story_title
):
    try:
        from reportlab.lib.pagesizes import LETTER
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    except ImportError as error:
        raise RuntimeError(
            "PDF export requires reportlab. Install it with: pip install reportlab"
        ) from error

    exports_folder = Path("exports")
    exports_folder.mkdir(exist_ok=True)

    pdf_path = exports_folder / make_pdf_filename(selected_event, story_title)

    font_name = "Helvetica"
    font_path = Path("C:/Windows/Fonts/arial.ttf")

    if font_path.exists():
        pdfmetrics.registerFont(TTFont("StoryFont", str(font_path)))
        font_name = "StoryFont"

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "StoryTitle",
        parent=styles["Title"],
        fontName=font_name,
        fontSize=20,
        leading=26,
        spaceAfter=18
    )
    heading_style = ParagraphStyle(
        "StoryHeading",
        parent=styles["Heading2"],
        fontName=font_name,
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=8
    )
    body_style = ParagraphStyle(
        "StoryBody",
        parent=styles["BodyText"],
        fontName=font_name,
        fontSize=11,
        leading=16,
        spaceAfter=8
    )

    labels = get_labels(language)
    spacer = Spacer(1, 0.12 * inch)
    story = []

    add_heading(story, labels["title"], lambda text: Paragraph(text, title_style))

    add_heading(story, labels["event"], lambda text: Paragraph(text, heading_style))
    add_paragraph(story, selected_event.name, lambda text: Paragraph(text, body_style), spacer)
    add_paragraph(
        story,
        f"{labels['date']}: {selected_event.start_date}",
        lambda text: Paragraph(text, body_style),
        spacer
    )
    if selected_event.hebrew_name:
        add_paragraph(
            story,
            f"{labels['hebrew_name']}: {selected_event.hebrew_name}",
            lambda text: Paragraph(text, body_style),
            spacer
        )
    add_paragraph(story, selected_event.description, lambda text: Paragraph(text, body_style), spacer)

    add_heading(story, labels["theme"], lambda text: Paragraph(text, heading_style))
    add_paragraph(story, selected_theme.title, lambda text: Paragraph(text, body_style), spacer)
    add_paragraph(
        story,
        f"{labels['source_event']}: {selected_theme.source_event}",
        lambda text: Paragraph(text, body_style),
        spacer
    )
    add_paragraph(
        story,
        f"{labels['core_value']}: {selected_theme.core_value}",
        lambda text: Paragraph(text, body_style),
        spacer
    )
    add_paragraph(
        story,
        f"{labels['story_angle']}: {selected_theme.story_angle}",
        lambda text: Paragraph(text, body_style),
        spacer
    )
    add_paragraph(story, selected_theme.description, lambda text: Paragraph(text, body_style), spacer)

    add_heading(story, labels["story"], lambda text: Paragraph(text, heading_style))
    add_paragraph(story, final_story, lambda text: Paragraph(text, body_style), spacer)

    add_heading(story, labels["parents"], lambda text: Paragraph(text, heading_style))
    add_paragraph(
        story,
        f"{labels['linked_event']}: {parent_companion.linked_event}",
        lambda text: Paragraph(text, body_style),
        spacer
    )
    add_paragraph(
        story,
        f"{labels['core_values']}: {', '.join(parent_companion.core_values)}",
        lambda text: Paragraph(text, body_style),
        spacer
    )
    add_paragraph(
        story,
        f"{labels['story_connection']}: {parent_companion.event_explanation}",
        lambda text: Paragraph(text, body_style),
        spacer
    )

    symbol_lines = [
        f"- {symbol.story_element}: {symbol.symbolic_meaning}"
        for symbol in parent_companion.symbol_explanations
    ]
    add_paragraph(
        story,
        f"{labels['symbols']}:<br/>" + "<br/>".join(symbol_lines),
        lambda text: Paragraph(text, body_style),
        spacer
    )

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=LETTER,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )
    document.build(story)

    return pdf_path
