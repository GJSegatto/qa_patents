import asyncio
import json
from typing import Dict, List, Any
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.tools.reasoning import ReasoningTools
from agno.tools import tool
from agno.utils.log import logger
from agno.workflow.v2 import StepOutput, Step, Workflow
from fastmcp import Client

# Cliente MCP para acessar as ferramentas
mcp_client = Client("http://localhost:9000/mcp")

# FERRAMENTAS MCP
@tool(name="buscar_patentes")
def buscar_patentes_tool(query: str) -> str:
    """
    Busca patentes no banco de dados usando a API especializada.
    
    Args:
        query: Termo de busca para as patentes
    
    Returns:
        Resultado da busca de patentes
    """
    logger.info("Utilizando tool: buscar_patentes_tool")
    async def _call_mcp():
        async with mcp_client:
            result = await mcp_client.call_tool("buscar_patentes", {"query": query})
            return result.content
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_call_mcp())
    finally:
        loop.close()

@tool(name="analisar_documento")
def analisar_documento_tool(doc_id: str) -> str:
    """
    Analisa um documento de patente específico.
    
    Args:
        doc_id: ID do documento a ser analisado
    
    Returns:
        Análise do documento
    """
    logger.info("Utilizando tool: analisar_documento_tool")
    async def _call_mcp():
        async with mcp_client:
            result = await mcp_client.call_tool("analisar_documento", {"doc_id": doc_id})
            return result.content
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_call_mcp())
    finally:
        loop.close()

# AGENTES ESPECIALIZADOS

def create_query_analyzer_agent() -> Agent:
    """
    Agente especializado em analisar queries do usuário e extrair filtros semânticos.
    """
    return Agent(
        name="QueryAnalyzer",
        model=OpenAIChat(id="gpt-5-nano"),
        tools=[ReasoningTools()],
        instructions="""
        Você é um especialista em análise semântica de consultas sobre patentes.
        
        Sua função é analisar a pergunta do usuário e extrair:
        1. **Termos técnicos principais** (tecnologias, métodos, processos)
        2. **Filtros temporais** (anos, décadas, períodos específicos)
        3. **Filtros geográficos** (países, regiões)
        4. **Filtros de empresas/inventores** (nomes de empresas, inventores)
        5. **Tipo de análise desejada** (busca simples, comparação, análise técnica)
        
        Sempre responda em formato JSON estruturado com as chaves:
        - "termos_tecnicos": lista de termos principais
        - "filtros_temporais": dicionário com filtros de tempo
        - "filtros_geograficos": lista de países/regiões
        - "filtros_empresas": lista de empresas/inventores
        - "tipo_analise": string descrevendo o tipo de análise
        - "query_refinada": versão otimizada da query para busca
        """,
        description="Especialista em análise semântica de consultas sobre patentes",
        markdown=False,
        debug_mode=True
    )

def create_patent_searcher_agent() -> Agent:
    """
    Agente especializado em buscar e recuperar patentes.
    """
    return Agent(
        name="PatentSearcher",
        model=OpenAIChat(id="gpt-5-nano"),
        tools=[
            ReasoningTools(),
            buscar_patentes_tool,
            analisar_documento_tool
        ],
        instructions="""
        Você é um especialista em busca de patentes.
        
        Sua função é:
        1. Receber parâmetros de busca estruturados
        2. Executar buscas na base de dados de patentes
        3. Analisar documentos específicos quando necessário
        4. Retornar dados estruturados e relevantes
        
        Sempre organize os resultados de forma clara e estruturada.
        Foque nos dados mais relevantes para a consulta original.
        """,
        description="Especialista em busca e recuperação de dados de patentes",
        markdown=False,
        debug_mode=True
    )

def create_response_formulator_agent() -> Agent:
    """
    Agente especializado em formular respostas baseadas nos dados recuperados.
    """
    return Agent(
        name="ResponseFormulator",
        model=OpenAIChat(id="gpt-5-nano"),
        tools=[ReasoningTools()],
        instructions="""
        Você é um especialista em comunicação técnica e análise de patentes.
        
        Sua função é:
        1. Receber dados brutos de patentes
        2. Formular respostas claras e informativas
        3. Manter-se ESTRITAMENTE nos dados fornecidos
        4. Não inventar ou inferir informações não presentes nos dados
        5. Estruturar a resposta de forma didática e profissional
        
        IMPORTANTE: Baseie suas respostas APENAS nos dados fornecidos.
        Se os dados forem insuficientes, indique claramente essa limitação.
        """,
        description="Especialista em formulação de respostas técnicas sobre patentes",
        markdown=True,
        debug_mode=True
    )

def create_quality_judge_agent() -> Agent:
    """
    Agente LLM-as-a-Judge para avaliar a qualidade das respostas.
    """
    return Agent(
        name="QualityJudge",
        model=OpenAIChat(id="gpt-5-nano"),
        tools=[ReasoningTools()],
        instructions="""
        Você é um juiz especializado em avaliar a qualidade de respostas sobre patentes.
        
        Critérios de avaliação:
        1. **Precisão factual** (0-10): A resposta está baseada nos dados fornecidos?
        2. **Completude** (0-10): A resposta aborda adequadamente a pergunta?
        3. **Clareza** (0-10): A resposta é clara e bem estruturada?
        4. **Relevância** (0-10): A resposta é relevante para a consulta original?
        5. **Confiabilidade** (0-10): A resposta evita especulações não fundamentadas?
        
        Formate sua avaliação como JSON com:
        - "pontuacoes": dicionário com cada critério e nota
        - "pontuacao_geral": média das pontuações (0-10)
        - "aprovado": boolean (aprovado se >= 7.0)
        - "observacoes": string com comentários detalhados
        - "sugestoes_melhoria": lista de sugestões específicas
        """,
        description="Juiz especializado em avaliar qualidade de respostas sobre patentes",
        markdown=False,
        debug_mode=True
    )

# FUNÇÕES DE PROCESSAMENTO

def analyze_query_step(step_input) -> StepOutput:
    """
    Etapa 1: Análise semântica da consulta do usuário
    """
    query_analyzer = create_query_analyzer_agent()
    
    prompt = f"""
    Analise esta consulta sobre patentes e extraia filtros semânticos: {step_input.message}
    
    Retorne um JSON estruturado com:
    - "termos_tecnicos": lista de termos principais
    - "filtros_temporais": dicionário com filtros de tempo  
    - "filtros_geograficos": lista de países/regiões
    - "filtros_empresas": lista de empresas/inventores
    - "tipo_analise": tipo de análise desejada
    - "query_refinada": versão otimizada para busca
    """
    
    response = query_analyzer.run(prompt)
    return StepOutput(content=response.content)

def search_patents_step(step_input) -> StepOutput:
    """
    Etapa 2: Busca de patentes na base de dados
    """
    patent_searcher = create_patent_searcher_agent()
    
    prompt = f"""
    Com base nesta análise semântica: {step_input.message}
    
    Execute a busca de patentes relevantes usando as ferramentas disponíveis.
    Organize os resultados por relevância e inclua detalhes importantes.
    """
    
    response = patent_searcher.run(prompt)
    return StepOutput(content=response.content)

def formulate_response_step(step_input) -> StepOutput:
    """
    Etapa 3: Formulação da resposta final
    """
    response_formulator = create_response_formulator_agent()
    
    # Dados de busca da etapa anterior
    search_data = step_input.message
    
    prompt = f"""
    Com base nos dados de patentes encontrados abaixo, formule uma resposta clara e profissional.
    
    Dados encontrados: {search_data}
    
    IMPORTANTE: 
    - Baseie-se EXCLUSIVAMENTE nos dados fornecidos
    - Não invente informações não presentes nos dados
    - Estruture a resposta de forma didática
    - Se os dados forem insuficientes, indique essa limitação
    """
    
    response = response_formulator.run(prompt)
    
    # Incluir metadados para próxima etapa
    result_with_metadata = {
        "response": response.content,
        "source_data": search_data,
        "step": "response_formulation"
    }
    
    return StepOutput(content=json.dumps(result_with_metadata, ensure_ascii=False, indent=2))

def evaluate_quality_step(step_input) -> StepOutput:
    """
    Etapa 4: Avaliação da qualidade (LLM-as-a-Judge)
    """
    try:
        # Tentar fazer o parse dos dados da etapa anterior
        step_data = json.loads(step_input.message)
        response_text = step_data.get("response", "")
        source_data = step_data.get("source_data", "")
    except:
        # Usar o conteúdo direto
        response_text = step_input.message
        source_data = ""
    
    quality_judge = create_quality_judge_agent()
    
    prompt = f"""
    Avalie a qualidade desta resposta sobre patentes:
    
    Resposta: {response_text}
    
    Dados fonte: {source_data}
    
    Critérios de avaliação (0-10 cada):
    1. Precisão factual - A resposta está baseada nos dados fornecidos?
    2. Completude - A resposta aborda adequadamente a pergunta?
    3. Clareza - A resposta é clara e bem estruturada?
    4. Relevância - A resposta é relevante para a consulta?
    5. Confiabilidade - A resposta evita especulações não fundamentadas?
    
    Retorne avaliação em JSON com:
    - "pontuacoes": dicionário com cada critério e nota
    - "pontuacao_geral": média das pontuações (0-10)  
    - "aprovado": boolean (aprovado se >= 7.0)
    - "observacoes": comentários detalhados
    - "resposta_final": a resposta que deve ser retornada ao usuário
    """
    
    evaluation = quality_judge.run(prompt)
    
    # Tentar fazer o parse da avaliação e incluir a resposta final
    try:
        eval_data = json.loads(evaluation.content)
        if eval_data.get("aprovado", False):
            # Se aprovado, retorna a resposta original
            final_result = {
                "approved": True,
                "response": response_text,
                "quality_score": eval_data.get("pontuacao_geral", 0),
                "evaluation": eval_data
            }
        else:
            # Retorna aviso
            final_result = {
                "approved": False,
                "response": f"⚠️ Resposta necessita revisão (Pontuação: {eval_data.get('pontuacao_geral', 0)}/10)\n\n{response_text}\n\n📋 Observações: {eval_data.get('observacoes', '')}",
                "quality_score": eval_data.get("pontuacao_geral", 0),
                "evaluation": eval_data
            }
        
        return StepOutput(content=json.dumps(final_result, ensure_ascii=False, indent=2))
    except:
        # Retorna resposta original
        return StepOutput(content=response_text)

# WORKFLOW PRINCIPAL
def create_patent_analysis_workflow() -> Workflow:
    """
    Cria o workflow principal de análise de patentes seguindo padrão sequential.
    """
    
    workflow = Workflow(
        name="PatentAnalysisWorkflow",
        steps=[
            analyze_query_step,      # Etapa 1: Análise semântica
            search_patents_step,     # Etapa 2: Busca de patentes  
            formulate_response_step, # Etapa 3: Formulação da resposta
            evaluate_quality_step    # Etapa 4: Avaliação da qualidade
        ]
    )
    
    return workflow

# FUNÇÃO PRINCIPAL DE EXECUÇÃO

def execute_patent_analysis(user_query: str) -> Dict[str, Any]:
    """
    Executa o workflow completo de análise de patentes.
    
    Args:
        user_query: Pergunta/consulta do usuário
        
    Returns:
        Resultado completo da análise incluindo resposta final e avaliação
    """
    
    try:
        workflow = create_patent_analysis_workflow()
        
        # Executar o workflow sequencial
        logger.info(f"🔍 Iniciando análise de patentes para: {user_query}")
        
        # Usar o método run do workflow que executa todas as etapas sequencialmente
        result = workflow.run(user_query)
        
        # O resultado final estará no conteúdo da última etapa
        final_response = result.content if hasattr(result, 'content') else str(result)
        
        return {
            "user_query": user_query,
            "final_response": final_response,
            "workflow_status": "completed"
        }
        
    except Exception as e:
        logger.error(f"Erro no workflow: {str(e)}")
        return {
            "user_query": user_query,
            "error": str(e),
            "workflow_status": "failed"
        }

# FUNÇÃO SIMPLIFICADA PARA INTEGRAÇÃO

def process_patent_query(user_query: str) -> str:
    """
    Versão simplificada síncrona para integração com FastAPI.
    
    Args:
        user_query: Pergunta do usuário
        
    Returns:
        Resposta final formatada
    """
    
    try:
        result = execute_patent_analysis(user_query)
        
        if result.get("workflow_status") == "failed":
            return f"Erro no processamento: {result.get('error', 'Erro desconhecido')}"
        
        # Tentar extrair resultado da última etapa (avaliação de qualidade)
        final_response = result["final_response"]
        
        try:
            # Tentar parsear como JSON estruturado
            if final_response.strip().startswith("{"):
                quality_result = json.loads(final_response)
                
                if "response" in quality_result:
                    # Resultado estruturado da avaliação
                    return quality_result["response"]
                elif "approved" in quality_result:
                    # Novo formato estruturado
                    return quality_result["response"]
                    
        except json.JSONDecodeError:
            pass
            
        # Se não conseguir parsear como JSON, retorna conteúdo direto
        return final_response
            
    except Exception as e:
        logger.error(f"Erro na execução do workflow: {str(e)}")
        return f"Erro na execução do workflow: {str(e)}"

# TESTE LOCAL
if __name__ == "__main__":
    # Teste do workflow
    test_query = "Buscar patentes sobre inteligência artificial para diagnóstico médico dos últimos 5 anos da Google"
    
    print("🚀 Testando workflow de análise de patentes...")
    result = execute_patent_analysis(test_query)
    print("\n" + "="*50)
    print("RESULTADO FINAL:")
    print("="*50)
    print(result)