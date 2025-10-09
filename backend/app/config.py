"""
Configurações do sistema de análise de patentes multi-agente
"""

# === CONFIGURAÇÕES DOS MODELOS ===
MODELS = {
    "query_analyzer": "gpt-5-nano",         # Análise semântica precisa
    "patent_searcher": "gpt-5-nano",        # Busca e recuperação
    "response_formulator": "gpt-5-nano",    # Formulação de respostas
    "quality_judge": "gpt-5-nano"           # Avaliação de qualidade
}

# === CONFIGURAÇÕES DO MCP ===
MCP_CONFIG = {
    "host": "localhost",
    "port": 9000,
    "endpoint": "/mcp"
}

# === CRITÉRIOS DE AVALIAÇÃO ===
QUALITY_CRITERIA = {
    "min_score": 7.0,  # Pontuação mínima para aprovação
    "weights": {       # Pesos para cada critério
        "precisao_factual": 0.3,
        "completude": 0.25,
        "clareza": 0.2,
        "relevancia": 0.15,
        "confiabilidade": 0.1
    }
}

# === CONFIGURAÇÕES DE WORKFLOW ===
WORKFLOW_CONFIG = {
    "timeout_per_stage": 60,  # Segundos por etapa
    "max_retries": 2,         # Tentativas máximas por etapa
    "enable_debugging": True  # Logs detalhados
}

# === CONFIGURAÇÕES DA API ===
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "reload": True,
    "log_level": "info"
}

# === TEMPLATES DE PROMPTS ===
PROMPT_TEMPLATES = {
    "query_analysis": """
    Analise esta consulta sobre patentes e extraia informações estruturadas:
    
    Consulta: {query}
    
    Extraia e organize em JSON:
    1. Termos técnicos principais
    2. Filtros temporais (anos, períodos)
    3. Filtros geográficos (países, regiões)  
    4. Filtros de empresas/inventores
    5. Tipo de análise desejada
    6. Query refinada para busca
    """,
    
    "patent_search": """
    Execute busca de patentes com base nestes parâmetros:
    
    Análise: {analysis}
    
    Use as ferramentas disponíveis para:
    1. Buscar patentes relevantes
    2. Analisar documentos específicos se necessário
    3. Organizar resultados por relevância
    """,
    
    "response_formulation": """
    Formule uma resposta completa baseada EXCLUSIVAMENTE nos dados fornecidos:
    
    Pergunta original: {original_query}
    Dados encontrados: {search_results}
    
    Estruture a resposta de forma clara e profissional.
    NÃO invente informações não presentes nos dados.
    Em caso de insuficiência de informações, apenas responda diretamente que "Não há informações suficientes."
    """,
    
    "quality_assessment": """
    Avalie a qualidade desta resposta sobre patentes:
    
    Pergunta: {original_query}
    Resposta: {response}
    Dados base: {source_data}
    
    Critérios (0-10 cada):
    - Precisão factual
    - Completude  
    - Clareza
    - Relevância
    - Confiabilidade
    
    Retorne avaliação em JSON com pontuações e aprovação.
    """
}