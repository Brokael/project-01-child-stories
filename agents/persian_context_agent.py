from datetime import date, timedelta
import json
from pathlib import Path

from schemas.calendar_event_schema import CalendarContext, CalendarEvent


PERSIAN_EVENTS_FILE = Path("data/cultural_events/persian_events.json")


def load_persian_events():
    with PERSIAN_EVENTS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_tuesday_before_nowruz(year):
    nowruz = date(year, 3, 20)
    current_day = nowruz - timedelta(days=1)

    while current_day.weekday() != 1:
        current_day -= timedelta(days=1)

    return current_day


def get_event_date(event, year):
    if event.get("date_rule") == "tuesday_before_nowruz":
        return get_tuesday_before_nowruz(year)

    month, day = event["month_day"].split("-")
    return date(year, int(month), int(day))


def build_calendar_event(event, event_date):
    date_note = event.get("date_note", "")
    source_notes = event.get("source_notes", [])

    description = event["description"]

    if date_note:
        description = f"{description}\nDate note: {date_note}"

    if source_notes:
        description = f"{description}\nSources: {'; '.join(source_notes)}"

    return CalendarEvent(
        name=event["name"],
        hebrew_name="",
        start_date=event_date.isoformat(),
        end_date=event_date.isoformat(),
        description=description,
        narrative_values=event.get("narrative_values", []),
        story_angles=event.get("story_angles", []),
        tradition=event.get("tradition", "Persian"),
        date_note=date_note,
        source_notes=source_notes
    )


def get_persian_context():
    today = date.today()
    events = load_persian_events()
    dated_events = []

    for year in [today.year - 1, today.year, today.year + 1]:
        for event in events:
            dated_events.append(
                (get_event_date(event, year), event)
            )

    past_events = [
        item for item in dated_events if item[0] < today
    ]
    upcoming_events = [
        item for item in dated_events if item[0] >= today
    ]

    past_events = sorted(past_events, key=lambda item: item[0])
    upcoming_events = sorted(upcoming_events, key=lambda item: item[0])

    selected_events = []

    if past_events:
        selected_events.append(past_events[-1])

    selected_events.extend(upcoming_events[:2])

    return CalendarContext(
        upcoming_events=[
            build_calendar_event(event, event_date)
            for event_date, event in selected_events
        ]
    )


if __name__ == "__main__":
    context = get_persian_context()
    print(context)
