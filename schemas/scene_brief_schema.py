from pydantic import BaseModel


class SceneBrief(BaseModel):
    scene_title: str
    key_moment: str
    characters: str
    setting: str
    mood: str
    visual_details: str
