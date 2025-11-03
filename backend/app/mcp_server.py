from mcp.server.fastmcp import FastMCP
from typing import Any
import json

mcp = FastMCP("Patent Tools MCP Server")

@mcp.tool()
def buscar_patentes(query: str = "") -> str:
    """
    Busca patentes usando a API especializada.
    
    Args:
        query: Termo de busca para patentes

    Returns:
        Resultados da busca de patentes em formato JSON
    """
    try:
        # Por enquanto, simulando uma resposta:
        fake_results = {
            "results": [
                {
                    "id": "US123456",
                    "title": f"Patent related to soccer",
                    "abstract": f"This patent describes innovations in ball technology...",
                    "assignee": "TechFoot Company Inc.",
                    "publication_date": "2023-10-01"
                },
                {
                    "id": "US789012",
                    "title": f"Advanced scouts System",
                    "abstract": f"Novel approach to soccer scouts implementation...",
                    "assignee": "Innovation Corp.",
                    "publication_date": "2023-09-15"
                }
            ]
        }
        return json.dumps(fake_results)
        
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    mcp.run(transport="stdio")