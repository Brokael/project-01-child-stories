from datetime import date
import requests

from schemas.calendar_event_schema import (
    CalendarContext,
    CalendarEvent
)


HEBCAL_URL = "https://www.hebcal.com/hebcal"
HEBCAL_TIMEOUT_SECONDS = 10


def fetch_calendar_items(year):
    params = {
        "v": "1",
        "cfg": "json",
        "maj": "on",
        "year": year,
        "month": "x",
        "ss": "on",
        "mf": "on",
        "c": "on"
    }

    try:
        response = requests.get(
            HEBCAL_URL,
            params=params,
            timeout=HEBCAL_TIMEOUT_SECONDS
        )
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError(
            f"Unable to fetch calendar context from {HEBCAL_URL}: {error}"
        ) from error

    return response.json().get("items", [])


def get_calendar_context():
    today = date.today()

    items = []

    for year in [today.year - 1, today.year, today.year + 1]:
        items.extend(fetch_calendar_items(year))

    unique_items = {}

    for item in items:
        item_key = (
            item.get("date", ""),
            item.get("title", "")
        )
        unique_items[item_key] = item

    past_items = []
    upcoming_items = []

    for item in unique_items.values():
        item_date = date.fromisoformat(item.get("date", "")[:10])

        if item_date < today:
            past_items.append(item)
        else:
            upcoming_items.append(item)

    past_items = sorted(
        past_items,
        key=lambda item: item.get("date", "")
    )

    upcoming_items = sorted(
        upcoming_items,
        key=lambda item: item.get("date", "")
    )

    selected_items = []

    if past_items:
        selected_items.append(past_items[-1])

    selected_items.extend(upcoming_items[:2])

    relevant_events = []

    for item in selected_items:
        title = item.get("title", "")
        hebrew = item.get("hebrew", "")
        event_date = item.get("date", "")

        event = CalendarEvent(
            name=title,
            hebrew_name=hebrew,
            start_date=event_date,
            end_date=event_date,
            description=f"Relevant Jewish event: {title}",
            narrative_values=[],
            story_angles=[]
        )

        relevant_events.append(event)

    return CalendarContext(
        upcoming_events=relevant_events
    )

if __name__ == "__main__":

    context = get_calendar_context()

    print("\n=== CALENDAR CONTEXT ===\n")
    print(context)
