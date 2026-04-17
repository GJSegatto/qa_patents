from fastmcp import FastMCP
import json, httpx
from os import getenv
from agno.utils.log import logger
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

mcp = FastMCP("Patent Tools MCP Server")

embedding_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
index_name = "patent_index_2"
dimensions = 768

@mcp.tool
async def search_patents(query_question: str) -> str:
    """
    Search for patents using external API.
    
    Args:
        query_question: a text in natural language, full of semantic value

    Returns:
        JSON array with similar patents to the used query
    """
    try:
        qdrant_key = getenv('QDRANT_API_KEY')

        # Gera o embedding com o modelo selecionado
        embedding = embedding_model.encode(query_question).tolist()

        if embedding is None:
            logger.error("ERRO AO REALIZAR EMBEDDING")
            return json.dumps({"error": "embbeding_is_none"})
        
        client = QdrantClient(
            url="https://a364e048-1fd9-4c55-88fc-9c70d8b2ca1b.us-east4-0.gcp.cloud.qdrant.io:6333",
            api_key=qdrant_key,
        )

        #Requisição para a base de dados
        response = client.query_points(
            collection_name=index_name,
            query=embedding,
            limit=5
        )

        points = list()
        points = [{"score": p.score, "payload": p.payload} for p in response.points]

        logger.warning(points)

        if len(points) == 0:
            logger.warning("ARRAY DE PATENTES VAZIO")
            return json.dumps({"error": "empty_patents_array"})

        return json.dumps({"patents": points}, ensure_ascii=False)
    
    except Exception as e:
        logger.error(e)
        return json.dumps({"error": str(e)})
    
import asyncio
if __name__ == "__main__":
    #asyncio.run(search_patents("What are the trend in manufacturing food systems?"))
    mcp.run(transport="http", host="127.0.0.1", port=9000)