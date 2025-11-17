from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import json, httpx
from os import getenv

from workflows import process_patent_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://192.168.0.100:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class ChatRequisition(BaseModel):
    question: str
    model: str

class SearchRequisition(BaseModel):
    patentId: str

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
async def chat(req: ChatRequisition):
    try:
        response = await process_patent_question(user_question=req.question, model=req.model)

        if isinstance(response, dict) and "final_answer" in response:
            return {"answer": response["final_answer"]}
        
        return {"answer": response}
    except Exception as e:
        return {"answer": f"Erro: {str(e)}"}

@app.post("/search")
async def search(req: SearchRequisition):
    try:
        print(req)
        print(type(req))
        api_key = getenv('IEL_API_KEY')

        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        async with httpx.AsyncClient() as client:
            req = await client.get(
                url="http://212.85.22.109:8001/patents/"+req.patentId,
                headers=headers
            )

        patent = json.loads(req.text)

        return json.dumps({ "answer": patent})
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    uvicorn.run(
        "http_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )