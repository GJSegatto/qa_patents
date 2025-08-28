from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.post("/chat")
def chat(question: Question):
    #Por enquanto resposta padrão
    return { "answer": f"Você perguntou: {question.question} mesmo?"}

@app.get("/")
def read_root():
    return {"msg": "Backend online!"}
