from fastmcp import FastMCP
import json, httpx
from os import getenv
from agno.utils.log import logger

mcp = FastMCP("Patent Tools MCP Server")

@mcp.tool
async def search_patents(query_question: str) -> str:
    """
    Busca patentes usando a API externa.
    
    Args:
        query_question: Texto utlizado para a busca na API

    Returns:
        Array de JSON com as patentes similares à query utilizada
    """
    try:
        api_key = getenv('IEL_API_KEY')
        logger.info("COMEÇOU")


        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Generate embedding
        async with httpx.AsyncClient() as client:
            req_embed = await client.post(
                url="http://212.85.22.109:8001/embed",
                json={'text': query_question},
                headers=headers,
                follow_redirects=True
            )
            logger.info("EMBED FEITO")
            try:
                req_embed.raise_for_status()
            except httpx.HTTPStatusError:
                return json.dumps({"error": "embed_request_failed", "status": req_embed.status_code, "body": req_embed.text})

            embed_dict = json.loads(req_embed.text)
            embedding = embed_dict.get("embeddings")

            if not embedding:
                return json.dumps({"error": "no_embedding_in_response"})

            req_sim = await client.post(
                url="http://212.85.22.109:8001/patents/similarity",
                json={"embedding": embedding[0]},
                headers=headers
            )
            
            logger.info("PATENTES FEITO")

            try:
                req_sim.raise_for_status()
            except httpx.HTTPStatusError:
                return json.dumps({"error": "sim_request_failed", "status": req_sim.status_code, "body": req_sim.text})
            
            sim_dict = json.loads(req_sim.text)
            patents = sim_dict.get("similar_patents")

            if patents is None:
                return json.dumps({"error": "no_similar_patents"})
            
            logger.info(json.dumps({"patents": patents}, ensure_ascii=False))

            return json.dumps({"patents": patents}, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": str(e)})
    
if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=9000)