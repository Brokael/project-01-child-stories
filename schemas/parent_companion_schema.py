from pydantic import BaseModel
from typing import List


class SymbolExplanation(BaseModel):
    story_element: str
    symbolic_meaning: str


class ParentCompanion(BaseModel):
    linked_event: str
    core_values: List[str]
    event_explanation: str
    symbol_explanations: List[SymbolExplanation]