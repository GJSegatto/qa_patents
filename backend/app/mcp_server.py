#from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fastmcp import FastMCP
from typing import Any

from agents import create_agent

agent = create_agent()

#app = FastAPI()
mcp = FastMCP("Agent MCP Server")

class ChatRequest(BaseModel):
    question: str

@mcp.tool()
def chat(question: str) -> str:
    """
    Conversa com o agente inteligente.

    Args:
        question: A pergunta ou mensagem direcionada ao agente.
    
    Returns:
        A resposta do agente.
    """
    try:
        resp = agent.run(question)
        return resp.content
    except Exception as e:
        return f"Erro: {str(e)}"

@mcp.tool()
def get_server_status() -> str:
    """
    Verifica o status do servidor.

    Returns:
        Status do servidor
    """
    return "Servidor MCP online e funcionando!"

if __name__ == "__main__":
    mcp.run(transport="http", port=9000)