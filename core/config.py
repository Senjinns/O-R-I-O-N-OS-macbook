import os
from pathlib import Path
from typing import Any, Dict

RACINE = Path(__file__).resolve().parent.parent
FICHIER_CONFIG = RACINE / "config.yaml"
FICHIER_EXAMPLE = RACINE / "config.example.yaml"

_config_cache: Dict[str, Any] = {}

def charger_config() -> Dict[str, Any]:
    global _config_cache
    cible = FICHIER_CONFIG if FICHIER_CONFIG.exists() else FICHIER_EXAMPLE
    try:
        import yaml
        with open(cible, "r", encoding="utf-8") as f:
            _config_cache = yaml.safe_load(f) or {}
    except ImportError:
        # Fallback si pyyaml n'est pas encore installé dans l'environnement courant
        _config_cache = {
            "nom_assistant": "Orion",
            "langue": "fr",
            "mode": "cloud",
            "anthropic": {
                "cle": "",
                "modele_rapide": "claude-3-5-haiku-20241022",
                "modele_expert": "claude-3-5-sonnet-20241022",
                "max_tokens": 1024,
                "temperature": 0.5
            },
            "assistant": {
                "mot_activation": "hey orion",
                "personnalite": "orion_sarcastique"
            },
            "budget": {
                "plafond_jour_eur": 2.0,
                "plafond_mois_eur": 30.0
            }
        }
    except Exception as e:
        print(f"[config] Erreur de lecture de {cible} : {e}")
        _config_cache = {}
    return _config_cache

def reglage(cle: str, defaut: Any = None) -> Any:
    global _config_cache
    if not _config_cache:
        charger_config()
    
    parties = cle.split(".")
    valeur = _config_cache
    for p in parties:
        if isinstance(valeur, dict) and p in valeur:
            valeur = valeur[p]
        else:
            return defaut
    return valeur if valeur is not None else defaut

def definir(cle: str, valeur: Any):
    global _config_cache
    parties = cle.split(".")
    d = _config_cache
    for p in parties[:-1]:
        d = d.setdefault(p, {})
    d[parties[-1]] = valeur
