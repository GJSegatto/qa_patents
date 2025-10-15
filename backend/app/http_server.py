from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from workflows import process_patent_query

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://192.168.0.100:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.get("/")
async def read_root():
    return {
        "status": "FastAPI Server online e funcionando!",
        "info": "Sistema multi-agente com workflow de análise de patentes ativo",
        "workflow_stages": [
            "1. Análise semântica da consulta",
            "2. Busca de patentes na base de dados", 
            "3. Formulação da resposta",
            "4. Avaliação da qualidade (LLM-as-a-Judge)"
        ]
    }
       
@app.post("/chat") 
async def chat(question: Question):
    try:
        # Usar o workflow multi-agente
        #response = process_patent_query(question.question)
        response = "ola"
        return {"answer": response}
    except Exception as e:
        return {"answer": f"Erro: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(
        "http_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )