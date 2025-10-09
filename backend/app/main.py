from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from fastmcp import Client

client = Client("http://localhost:9000/mcp")
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

@app.get("/")
async def read_root():
    async with client:
        try:
            result = await client.call_tool("get_server_status")
            return {"status": result.data}
        except Exception as e:
            return {"error": str(e)}
    
    
@app.post("/chat")
async def chat(question: Question):
    async with client:
        try:
            answer = await client.call_tool("chat", {"question": question.question})
            return { "answer": answer.data }
        except Exception as e:
            return {"answer": f"Erro: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )