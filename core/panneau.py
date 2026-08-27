from fastapi import APIRouter
from core import config, budget, memoire, registre

router = APIRouter(prefix="/api/panneau", tags=["Tableau de Bord"])

@router.get("/info")
async def obtenir_info():
    return {
        "nom": config.reglage("nom_assistant", "Orion"),
        "mode": config.reglage("mode", "cloud"),
        "budget": budget.etat(),
        "outils_charges": list(registre._OUTILS.keys()),
        "memoire": memoire.texte_pour_systeme()
    }
