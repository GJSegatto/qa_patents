import asyncio
from agno.utils.log import logger
from agno.workflow import Step, Workflow, Loop
from agno.workflow.types import StepOutput
from agno.db.sqlite import SqliteDb
from typing import Dict, Any

from agents import (
    question_analyzer_agent,
    patent_searcher_agent,
    response_formulator_agent,
    quality_judge_agent
)

# FUNÇÕES DE PROCESSAMENTO

analyze_question_step = Step(
    name="Question_Analyzer",
    agent=question_analyzer_agent,
    description="Analisa a pergunta do usuário para obtenção de filtros semânticos."
)

search_patents_step = Step(
    name="Patent_Searcher",
    agent = patent_searcher_agent,
    description="Realiza a busca na base de dados de patentes."
)

formulate_response_step = Step(
    name="Formulate_Response",
    agent=response_formulator_agent,
    description="Gera a resposta para o usuário de acordo com as informações de patentes do passo anterior."
)

judging_step = Step(
    name="Quality_Judge",
    agent=quality_judge_agent,
    description="Julga a qualidade da resposta de acordo com parâmetros previamente definidos."
)

def quality_evaluator(output: StepOutput) -> bool:
    """
    Avalia se a nota da resposta gerada é boa o suficiente
    para ser encaminhada ao usuário.
    """

    if not output:
        return False
    
    print(type(output[-1].content))
    return True

patent_analysis_workflow = Workflow(
    name="Patent_Analysis_Workflow",
    description="Workflow do processo completo de análise de patentes e geração de resposta ao usuário.",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db"
    ),
    steps=[
        analyze_question_step,
        Loop(
            name="answer_development",
            steps=[search_patents_step, formulate_response_step, judging_step],
            end_condition=quality_evaluator,
            max_iterations=3,
        )
    ]
)

async def process_patent_question(user_question: str) -> Dict[str, Any]:
    try:
        resp = await patent_analysis_workflow.arun(user_question)
        if resp and hasattr(resp, 'content'):
            resp_dict = resp.content.model_dump()
            return resp_dict
        else:
            return {"error": "Resposta vazia!"}
    except Exception as e:
        logger.error("Erro no WORKFLOW")
        return {"error": str(e)}

# TESTE LOCAL
if __name__ == "__main__":
    # Teste do workflow
    test_query = "O que foi patenteado nos últimos 10 anos na área do futebol?"
    
    print("🚀 Testando workflow de análise de patentes...")
    
    async def func():
        await patent_analysis_workflow.aprint_response(
            input=test_query,
            mardkown=True,
            stream=True,
            stream_events=True
        )
    
    asyncio.run(func())