from pydantic import BaseModel
from typing import List


class StoryPlan(BaseModel):
    title: str
    target_age: str
    main_character: str
    setting: str
    core_value: str
    problem: str
    key_moments: List[str]
    ending: str