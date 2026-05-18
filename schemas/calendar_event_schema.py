from pydantic import BaseModel
from typing import List


class CalendarEvent(BaseModel):
    name: str
    hebrew_name: str
    start_date: str
    end_date: str
    description: str
    narrative_values: List[str]
    story_angles: List[str]


class CalendarContext(BaseModel):
    upcoming_events: List[CalendarEvent]