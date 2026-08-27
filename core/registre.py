import inspect
import importlib
import pkgutil
from typing import Callable, Dict, Any, List
from pathlib import Path

_OUTILS: Dict[str, Dict[str, Any]] = {}

def outil(
    nom: str,
    description: str,
    parametres: Dict[str, Any],
    securite: str = "N1",       # N1 = lecture/inoffensif, N2 = action locale, N3 = critique (confirmation requise)
    affichage: str = "auto"     # toujours, jamais, auto (pour le HUD)
):
    def decorateur(fonction: Callable):
        _OUTILS[nom] = {
            "nom": nom,
            "description": description,
            "parametres": parametres,
            "fonction": fonction,
            "securite": securite,
            "affichage": affichage
        }
        return fonction
    return decorateur

def obtenir_outils_anthropic() -> List[Dict[str, Any]]:
    liste = []
    for info in _OUTILS.values():
        liste.append({
            "name": info["nom"],
            "description": f"[{info['securite']}] {info['description']}",
            "input_schema": info["parametres"]
        })
    return liste

def executer_outil(nom: str, arguments: Dict[str, Any]) -> str:
    if nom not in _OUTILS:
        return f"Erreur : L'outil '{nom}' n'est pas enregistré."
    
    info = _OUTILS[nom]
    fonction = info["fonction"]
    
    try:
        sig = inspect.signature(fonction)
        if len(sig.parameters) == 0:
            resultat = fonction()
        else:
            resultat = fonction(**arguments)
        return str(resultat)
    except Exception as e:
        return f"Erreur lors de l'exécution de '{nom}' : {str(e)}"

def securite_outil(nom: str) -> str:
    return _OUTILS.get(nom, {}).get("securite", "N1")

def affichage_outil(nom: str) -> str:
    return _OUTILS.get(nom, {}).get("affichage", "auto")

def decouvrir_outils():
    racine_tools = Path(__file__).resolve().parent.parent / "tools"
    if not racine_tools.exists():
        return
    
    for module_info in pkgutil.iter_modules([str(racine_tools)]):
        if module_info.name.startswith("_"):
            continue
        try:
            importlib.import_module(f"tools.{module_info.name}")
        except Exception as e:
            print(f"[registre] Impossible de charger tools.{module_info.name}: {e}")
