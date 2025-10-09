from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.tools.reasoning import ReasoningTools
from agno.tools import tool
from fastmcp import Client
import asyncio

# Cliente MCP para acessar as ferramentas
mcp_client = Client("http://localhost:9000/mcp")

@tool(name="buscar_patentes")
def buscar_patentes_tool(query: str) -> str:
    """
    Busca patentes no banco de dados usando a API especializada.
    
    Args:
        query: Termo de busca para as patentes
    
    Returns:
        Resultado da busca de patentes
    """
    async def _call_mcp():
        async with mcp_client:
            result = await mcp_client.call_tool("buscar_patentes", {"query": query})
            return result.content
    
    # Executar a chamada assíncrona
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_call_mcp())
    finally:
        loop.close()

@tool(name="analisar_documento")
def analisar_documento_tool(doc_path: str) -> str:
    """
    Analisa um documento de patente específico.
    
    Args:
        doc_path: Caminho ou ID do documento a ser analisado
    
    Returns:
        Análise do documento
    """
    async def _call_mcp():
        async with mcp_client:
            result = await mcp_client.call_tool("analisar_documento", {"doc_path": doc_path})
            return result.content
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_call_mcp())
    finally:
        loop.close()

def create_agent():
    """Cria e configura um agente."""

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
            buscar_patentes_tool,  # Ferramenta MCP integrada
            analisar_documento_tool,  # Ferramenta MCP integrada
        ],
        instructions="""
        Você é um assistente especializado em patentes. 
        Use as ferramentas disponíveis quando o usuário:
        - Buscar informações sobre patentes
        - Quiser analisar documentos específicos
        - Precisar de análises técnicas
        """,
        description="Assistente inteligente especializado em análise de patentes.",
        markdown=True,
        memory=memory,
        enable_agentic_memory=True,
    )
    
    return agent