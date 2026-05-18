from datetime import date
import requests

from schemas.calendar_event_schema import (
    CalendarContext,
    CalendarEvent
)


HEBCAL_URL = "https://www.hebcal.com/hebcal"
HEBCAL_TIMEOUT_SECONDS = 10


def get_calendar_context():
    today = date.today()

    params = {
        "v": "1",
        "cfg": "json",
        "maj": "on",
        "year": today.year,
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

    data = response.json()

    future_items = []

    for item in data.get("items", []):
        item_date = date.fromisoformat(item.get("date", "")[:10])

        if item_date >= today:
            future_items.append(item)

    future_items = sorted(
        future_items,
        key=lambda item: item.get("date", "")
    )

    upcoming_events = []

    for item in future_items[:5]:
        title = item.get("title", "")
        hebrew = item.get("hebrew", "")
        event_date = item.get("date", "")

        event = CalendarEvent(
            name=title,
            hebrew_name=hebrew,
            start_date=event_date,
            end_date=event_date,
            description=f"Upcoming Jewish event: {title}",
            narrative_values=[],
            story_angles=[]
        )

        upcoming_events.append(event)

    return CalendarContext(
        upcoming_events=upcoming_events
    )

if __name__ == "__main__":

    context = get_calendar_context()

    print("\n=== CALENDAR CONTEXT ===\n")
    print(context)
