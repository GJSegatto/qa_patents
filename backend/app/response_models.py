from pydantic import BaseModel

class QuestionAnalyserResponse(BaseModel):
    original_question: str
    technical_terms: list[str]
    temporal_filters: list[str]
    geographical_filters: list[str]
    company_filters: list[str]

class PatentSearcherResponse(BaseModel):
    original_question: str
    patents: list[str]

class ResponseFormulatorResponse(BaseModel):
    original_question: str
    patents: list[str]
    insights: str
    final_answer: str

# TERMINAR
class QualityJudgeResponse(BaseModel):
    original_question: str
    patents: list[str]
