from pydantic import BaseModel
from typing import List


class StoryReview(BaseModel):
    overall_score: int
    strengths: List[str]
    issues: List[str]
    suggested_improvements: List[str]