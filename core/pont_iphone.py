from fastapi import APIRouter, HTTPException, Header, Body
from pydantic import BaseModel
from typing import Optional
from core import config, llm, budget

router = APIRouter(prefix="/api", tags=["iPhone & Raccourcis Siri"])
agent_llm = llm.ClaudeAgent()

class RequeteCommande(BaseModel):
    commande: str
    cle_secrete: Optional[str] = None

@router.post("/commande")
async def executer_commande_iphone(payload: RequeteCommande, x_api_key: Optional[str] = Header(None)):
    cle_attendue = config.reglage("serveur.cle_api_pont", "orion-secret-token")
    cle_recue = payload.cle_secrete or x_api_key
    
    if cle_attendue and cle_recue != cle_attendue:
        raise HTTPException(status_code=401, detail="Clé de sécurité invalide.")
    
    reponse, _ = agent_llm.repondre_et_agir(payload.commande)
    return {
        "status": "ok",
        "commande": payload.commande,
        "reponse": reponse
    }

@router.get("/status")
async def status_general():
    return {
        "orion": "actif",
        "systeme": "macOS Apple Silicon",
        "budget": budget.etat()
    }
