from typing import List
from pydantic import BaseModel


class ProjectInput(BaseModel):
    project_type: str
    timeline_months: int
    team_size: int
    requirements_clarity: str
    dependencies: List[str]


class Risk(BaseModel):
    name: str
    severity: str
    likelihood: str


class EvaluationResult(BaseModel):
    relevance: float
    clarity: float
    coverage: float
