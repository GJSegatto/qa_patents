import asyncio, json, re, httpx
from agno.utils.log import logger
from agno.workflow import Step, Workflow, Loop
from agno.workflow.types import StepInput, StepOutput
from agno.db.sqlite import SqliteDb
from typing import Dict, Any
from agents import (
    question_analyzer_agent,
    patent_searcher_agent,
    response_formulator_agent,
    quality_judge_agent
)
from agents import configure_agents

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

def quality_evaluator(step_input: StepInput) -> bool:
    """
    Avalia se a nota da resposta gerada é boa o suficiente
    para ser encaminhada ao usuário.
    """
    try:
        if not step_input:
            return True
        
        judge_resp = step_input[-1].content

        if hasattr(judge_resp, "overall_score") and float(getattr(judge_resp, "overall_score")) >= 7:
            return True
        else:
            return False
    except:
        return False

async def is_api_healthy(step_input: StepInput) -> StepOutput:
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url="http://212.85.22.109:8001/health",
                headers={"Accept": "application/json"}
            )
            content = json.loads(resp.text)
            if resp.status_code == 200:
                if content.get("status") == "healthy" and content.get("database") == "healthy":
                    return StepOutput(content=step_input.input, stop=False)
            else:
                return StepOutput(content=f"API respondeu com {resp.status_code}: {resp.text}", stop=True)
    except Exception as e:
        return StepOutput (content=f"Erro: {e}",stop=True)

patent_analysis_workflow = Workflow(
    name="Patent_Analysis_Workflow",
    description="Workflow do processo completo de análise de patentes e geração de resposta ao usuário.",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db"
    ),
    steps=[
        Step(name="API Healthy Analysis", executor=is_api_healthy),
        analyze_question_step,
        Loop(
            name="answer_development",
            steps=[search_patents_step, formulate_response_step, judging_step],
            end_condition=quality_evaluator,
            max_iterations=3,
        )
    ],
    debug_mode=True
)

async def process_patent_question(user_question: str, model: str) -> Dict[str, Any]:
    configure_agents(model=model)
    try:
        resp = await patent_analysis_workflow.arun(user_question)
        content = getattr(resp, "content", resp)

        if hasattr(content, "final_answer"):
            final = getattr(content, "final_answer")
            return {"final_answer": final}

        if isinstance(content, dict):
            return {"final_answer": content.get("final_answer")}

        if isinstance(content, str):
            s = content.strip()
            s = re.sub(r"^```(?:json)?\s*", "", s, flags=re.I)
            s = re.sub(r"\s*```$", "", s)

            try:
                resp_dict = json.loads(s)
                return {"final_answer": resp_dict.get("final_answer")}
            except json.JSONDecodeError:
                m = re.search(r'"final_answer"\s*:\s*"(?P<fa>.*?)"', s, re.S)
                if m:
                    fa = bytes(m.group("fa"), "utf-8").decode("unicode_escape")
                    return {"final_answer": fa}
                return {"final_answer": s}

        return {"error": "Formato de resposta do modelo não reconhecido"}
    except Exception as e:
        logger.error("Erro no WORKFLOW")
        return {"error": str(e)}

# TESTE LOCAL
if __name__ == "__main__":
    # Teste do workflow
    test_query = "What are the trends in industrial machinery for food manufacturing?"
    
    print("🚀 Testando workflow de análise de patentes...")
    
    async def func():
        await patent_analysis_workflow.aprint_response(
            input=test_query,
            mardkown=True,
            stream=True,
            stream_events=True
        )
    
    asyncio.run(func())