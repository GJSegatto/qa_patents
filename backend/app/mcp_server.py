from fastmcp import FastMCP
import json, httpx
from os import getenv
from agno.utils.log import logger

mcp = FastMCP("Patent Tools MCP Server")

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
        api_key = getenv('IEL_API_KEY')
        logger.info("SERVIDOR MCP INICIADO")

        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        async with httpx.AsyncClient() as client:
            req_embed = await client.post(
                url="http://212.85.22.109:8001/embed",
                json={'text': query_question},
                headers=headers,
                follow_redirects=True
            )
            
            try:
                req_embed.raise_for_status()
            except httpx.HTTPStatusError:
                return json.dumps({"error": "embed_request_failed", "status": req_embed.status_code, "body": req_embed.text})

            logger.info("PROCESSO DE EMBEDDING CONCLUÍDO")

            try:
                embed_dict = json.loads(req_embed.text)
            except Exception:
                return json.dumps({"error": "invalid_embed_response", "body": req_embed.text})
            
            embedding = embed_dict.get("embeddings")
            if embedding is None:
                logger.error("ERRO AO REALIZAR EMBEDDING")
                return json.dumps({"error": "no_embedding_in_response"})

            req_sim = await client.post(
                url="http://212.85.22.109:8001/patents/similarity",
                json={
                    "embedding": embedding[0],
                    "max_results": 5
                },
                headers=headers
            )
            
            logger.info("PATENTES FEITO")

            try:
                req_sim.raise_for_status()
            except httpx.HTTPStatusError:
                logger.error("ERRO AO REALIZAR BUSCA")
                return json.dumps({"error": "sim_request_failed", "status": req_sim.status_code, "body": req_sim.text})
            
            sim_dict = json.loads(req_sim.text)
            patents = sim_dict.get("similar_patents")

            if len(patents) == 0:
                logger.warning("SEM PATENTES SIMILARES")
                return json.dumps({"error": "no_similar_patents"})
            
            allowed = ["publication_number", "publication_date", "title", "abstract", "orgname"]
            filtered_patents = []

            logger.info(patents)

            if isinstance(patents, list):
                for p in patents:
                    if not isinstance(p, dict):
                        continue
                    filt = {i: p.get(i) for i in allowed if i in p}
                    filtered_patents.append(filt)
            else:
                filtered_patents = []

            logger.info(json.dumps({"patents": filtered_patents}, ensure_ascii=False))

            return json.dumps({"patents": filtered_patents}, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": str(e)})
    
if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=9000)