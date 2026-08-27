import json
import datetime
from pathlib import Path
from core import config

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_DATA = RACINE / "data"
DOSSIER_DATA.mkdir(parents=True, exist_ok=True)
FICHIER_BUDGET = DOSSIER_DATA / "budget.json"

# Tarifs Anthropic (estimation EUR par 1k tokens)
TARIFS = {
    "claude-3-5-haiku-20241022": {"in": 0.0008, "out": 0.004, "cache_read": 0.00008},
    "claude-3-5-sonnet-20241022": {"in": 0.003, "out": 0.015, "cache_read": 0.0003}
}

def _charger_donnees():
    if FICHIER_BUDGET.exists():
        try:
            with open(FICHIER_BUDGET, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"historique": {}, "total_mois": 0.0}

def enregistrer(fournisseur: str, modele: str, in_tokens: int, out_tokens: int, cache_read: int = 0):
    donnees = _charger_donnees()
    aujourd_hui = datetime.date.today().isoformat()
    
    tarif = TARIFS.get(modele, {"in": 0.001, "out": 0.005, "cache_read": 0.0001})
    cout = (
        (in_tokens * tarif["in"] / 1000.0) +
        (out_tokens * tarif["out"] / 1000.0) +
        (cache_read * tarif["cache_read"] / 1000.0)
    )
    
    jour = donnees["historique"].setdefault(aujourd_hui, {
        "in_tokens": 0, "out_tokens": 0, "cache_tokens": 0, "cout_eur": 0.0, "appels": 0
    })
    
    jour["in_tokens"] += in_tokens
    jour["out_tokens"] += out_tokens
    jour["cache_tokens"] += cache_read
    jour["cout_eur"] += cout
    jour["appels"] += 1
    
    with open(FICHIER_BUDGET, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=2)

def etat() -> dict:
    donnees = _charger_donnees()
    aujourd_hui = datetime.date.today().isoformat()
    jour = donnees["historique"].get(aujourd_hui, {"cout_eur": 0.0, "appels": 0})
    
    plafond_jour = config.reglage("budget.plafond_jour_eur", 2.0)
    total_jour = jour["cout_eur"]
    pct = (total_jour / plafond_jour) if plafond_jour > 0 else 0.0
    
    return {
        "total_jour": total_jour,
        "plafond_jour": plafond_jour,
        "pct_jour": pct,
        "appels_jour": jour["appels"],
        "depassement": total_jour >= plafond_jour
    }
