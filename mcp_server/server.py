import asyncio
import json
from mcp.server.fastmcp import FastMCP
from core import registre, config

# Initialisation du serveur FastMCP
mcp = FastMCP("ORION OS Tools")

# Découverte automatique de tous les outils Orion
registre.decouvrir_outils()

# Exposition des outils d'Orion comme outils MCP pour Claude Desktop & Cursor
for nom_outil, info in registre._OUTILS.items():
    fonction_origine = info["fonction"]
    desc = info["description"]
    
    # Enregistrement dynamique dans FastMCP
    mcp.add_tool(fonction_origine, name=nom_outil, description=desc)

def demarrer_mcp():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    demarrer_mcp()
