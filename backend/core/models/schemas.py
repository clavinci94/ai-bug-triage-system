from pydantic import BaseModel


class IssueIn(BaseModel):
    title: str
    body: str


class IssueOut(BaseModel):
    title: str
    body: str
    url: str


class ClassificationOut(BaseModel):
    category: str
    confidence: float
    rationale: str
