from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
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
from os import getenv
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

client = Client(StreamableHttpTransport(url="http://localhost:9000/mcp"))

@tool
async def search_patents(query_question: str) -> str:
    """
    Connect to MCP Server to retrieve patent informations.

    Args:
        None

    Return:
        JSON with patent informations
    """
    async with client:
        response = await client.call_tool(name="search_patents", arguments={"query_question": query_question})
        return response.content

from prompts import (
    QUESTION_ANALYZER_INSTRUCTION,
    PATENT_SEARCHER_INSTRUCTION,
    RESPONSE_FORMULATOR_INSTRUCTION,
    QUALITY_JUDGE_INSTRUCTION
)

def configure_agents(model : str):
    logger.info("Configurando agentes de acordo.")

    if 'gemini' in model.lower():
        api_key = getenv('GOOGLE_API_KEY')
        question_analyzer_agent.model=Gemini(id=model, api_key=api_key)
        question_analyzer_agent.input_schema=None
        question_analyzer_agent.output_schema=None

        patent_searcher_agent.model=Gemini(id=model, api_key=api_key)   
        patent_searcher_agent.input_schema=None
        patent_searcher_agent.output_schema=None

        response_formulator_agent.model=Gemini(id=model, api_key=api_key)
        response_formulator_agent.input_schema=None
        response_formulator_agent.output_schema=None

        quality_judge_agent.model=Gemini(id=model, api_key=api_key)
        quality_judge_agent.input_schema=None
        quality_judge_agent.output_schema=None
    elif 'gpt' in model.lower():
        api_key = getenv('OPENAI_API_KEY')
        question_analyzer_agent.model=OpenAIChat(id=model, api_key=api_key)
        patent_searcher_agent.model=OpenAIChat(id=model, api_key=api_key)
        response_formulator_agent.model=OpenAIChat(id=model, api_key=api_key)
        quality_judge_agent.model=OpenAIChat(id=model, api_key=api_key)
    

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
    