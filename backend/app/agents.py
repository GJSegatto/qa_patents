from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.tools import tool
from agno.utils.log import logger
import asyncio
from fastmcp import Client
from response_models import (
    QuestionAnalyserResponse,
    PatentSearcherResponse,
    ResponseFormulatorResponse,
    QualityJudgeResponse
)

client = Client("mcp_server.py")

@tool
async def search_patents() -> str:
    """
    Connect to MCP Server to retrieve patent informations.

    Args:
        None

    Return:
        JSON with patent informations
    """
    async with client:
        response = await client.call_tool("buscar_patentes", {"query": "soccer ball"})
        return response.content

from prompts import (
    QUESTION_ANALYZER_INSTRUCTION,
    PATENT_SEARCHER_INSTRUCTION,
    RESPONSE_FORMULATOR_INSTRUCTION,
    QUALITY_JUDGE_INSTRUCTION
)

question_analyzer_agent: Agent = Agent(
    name="QueryAnalyzer",
    model=OpenAIChat(id="gpt-5-nano"),
    tools=[ReasoningTools()],
    instructions=QUESTION_ANALYZER_INSTRUCTION,
    description="Especialista em análise semântica de consultas sobre patentes",
    output_schema=QuestionAnalyserResponse,
    markdown=False,
    debug_mode=False
)

patent_searcher_agent: Agent = Agent(
    name="PatentSearcher",
    model=OpenAIChat(id="gpt-5-nano"),
    tools=[
        #ReasoningTools(),
        search_patents
    ],
    tool_call_limit=2,
    instructions=PATENT_SEARCHER_INSTRUCTION,
    description="AI agent, specialist in patent searching.",
    input_schema=QuestionAnalyserResponse,
    output_schema=PatentSearcherResponse,
    markdown=False,
)

response_formulator_agent: Agent = Agent(
    name="ResponseFormulator",
    model=OpenAIChat(id="gpt-5-nano"),
    tools=[ReasoningTools()],
    instructions=RESPONSE_FORMULATOR_INSTRUCTION,
    description="Especialista em formulação de respostas técnicas sobre patentes",
    input_schema=PatentSearcherResponse,
    output_schema=ResponseFormulatorResponse,
    markdown=True,
    debug_mode=False
)

quality_judge_agent: Agent = Agent(
    name="QualityJudge",
    model=OpenAIChat(id="gpt-5-nano"),
    tools=[ReasoningTools()],
    instructions=QUALITY_JUDGE_INSTRUCTION,
    description="Juiz especializado em avaliar qualidade de respostas sobre patentes",
    input_schema=ResponseFormulatorResponse,
    output_schema=QualityJudgeResponse,
    markdown=True,
    debug_mode=False
)

if __name__ == "__main__":
    # Teste do workflow    
    print("🚀 Testando MCPTools")

    async def func():
        try:
            res = await patent_searcher_agent.arun("Use o servidor MCP para recuperar informações de patentes.")
        except:
            logger.error("FZADA")
    
    try:
        asyncio.run(func())
    except:
        logger.error("Deu erro aquiii")
    