from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.tools.reasoning import ReasoningTools

memory = Memory(
    model=OpenAIChat(id="gpt-5-nano"),
    db=SqliteMemoryDb(table_name="user_memories", db_file="tmp/agent.db"),
    delete_memories=True,
    clear_memories=True
)

agent = Agent(
    model=OpenAIChat(id="gpt-5-nano"),
    tools=[
        ReasoningTools(add_instructions=True),
    ],
    user_id="Gabriel",
    instructions="Seja direto nas suas respostas.",
    description="Você é um assistente inteligente prestativo.",
    markdown=True,
    memory=memory,
    enable_agentic_memory=True,
)

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
    try:
        resp = agent.run(question.question)
        return { "answer": resp.content}
    except Exception as e:
        return {"answer": f"Erro: {str(e)}"}

@app.get("/")
def read_root():
    return {"msg": "Backend online!"}
