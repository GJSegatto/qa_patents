from pydantic import BaseModel
from datetime import date
from typing import Optional

class TemporalFilter(BaseModel):
    start_date: date = None
    end_date: date = None
    period_description: Optional[str] = None

class QuestionAnalyserResponse(BaseModel):
    original_question: str
    technical_terms: list[str]
    temporal_filters: Optional[TemporalFilter]
    geographical_filters: Optional[list[str]]
    company_filters: Optional[list[str]]

class PatentSearcherResponse(BaseModel):
    original_question: str
    patents: list[str]

class ResponseFormulatorResponse(BaseModel):
    original_question: str
    patents: list[str]
    final_answer: str

class EvaluationCriteria(BaseModel):
    factual_accuracy: int
    completeness: int
    clarity: int
    relevance: int
    reliability: int

class QualityJudgeResponse(BaseModel):
    original_question: str
    patents: list[str]
    scores: EvaluationCriteria
    overall_score: float
    approved: bool
    comments: Optional[str]
    final_answer: str
