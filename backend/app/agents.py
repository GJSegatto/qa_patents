from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.tools import tool
from agno.utils.log import logger
from agno.workflow import WorkflowAgent
from os import getenv
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from response_models import (
    QuestionAnalyserResponse,
    PatentSearcherResponse,
    ResponseFormulatorResponse,
    QualityJudgeResponse
)

client = Client(StreamableHttpTransport(url="http://localhost:9000/mcp"))

@tool
async def search_patents(query_question: str) -> str:
    """
    Connect to MCP Server to retrieve patent informations.

    Args:
        query_qustion: a text in natural language, full of semantic value

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

def configure_agents(model: str, behavior: str):
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
        response_formulator_agent.instructions=RESPONSE_FORMULATOR_INSTRUCTION + (behavior if behavior else "")

        quality_judge_agent.model=Gemini(id=model, api_key=api_key)
        quality_judge_agent.input_schema=None
        quality_judge_agent.output_schema=None
    elif 'gpt' in model.lower():
        api_key = getenv('OPENAI_API_KEY')
        question_analyzer_agent.model=OpenAIResponses(id=model, api_key=api_key)
        patent_searcher_agent.model=OpenAIResponses(id=model, api_key=api_key)
        response_formulator_agent.model=OpenAIResponses(id=model, api_key=api_key)
        quality_judge_agent.model=OpenAIResponses(id=model, api_key=api_key)
    
question_analyzer_agent: Agent = Agent(
    name="QueryAnalyzer",
    model=OpenAIResponses(id="gpt-5-nano"),
    tools=[ReasoningTools()],
    instructions=QUESTION_ANALYZER_INSTRUCTION,
    description=" Specialist in semantic analysis about patent questions.",
    output_schema=QuestionAnalyserResponse,
    markdown=False,
)

patent_searcher_agent: Agent = Agent(
    name="PatentSearcher",
    model=OpenAIResponses(id="gpt-5-nano"),
    tools=[
        search_patents
    ],
    tool_call_limit=2,
    instructions=PATENT_SEARCHER_INSTRUCTION,
    description="Specialist in patent database searching.",
    input_schema=QuestionAnalyserResponse,
    output_schema=PatentSearcherResponse,
    markdown=False,
)

response_formulator_agent: Agent = Agent(
    name="ResponseFormulator",
    model=OpenAIResponses(id="gpt-5-nano"),
    tools=[ReasoningTools()],
    instructions=RESPONSE_FORMULATOR_INSTRUCTION,
    description="Specialist in technical response formulation about patents.",
    input_schema=PatentSearcherResponse,
    output_schema=ResponseFormulatorResponse,
    markdown=True,
)

quality_judge_agent: Agent = Agent(
    name="QualityJudge",
    model=OpenAIResponses(id="gpt-5-nano"),
    tools=[ReasoningTools()],
    instructions=QUALITY_JUDGE_INSTRUCTION,
    description="Judge specialized on evaluating the quality of answaers about patents.",
    input_schema=ResponseFormulatorResponse,
    output_schema=QualityJudgeResponse,
    markdown=True,
)

workflow_agent = WorkflowAgent(
    model=OpenAIResponses(id="gpt-5-nano"),
)