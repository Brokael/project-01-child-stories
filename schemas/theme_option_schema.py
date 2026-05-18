from pydantic import BaseModel
from typing import List


class ThemeOption(BaseModel):
    option_number: int
    title: str
    source_event: str
    core_value: str
    story_angle: str
    description: str


class ThemeOptions(BaseModel):
    options: List[ThemeOption]