import inspect
import importlib
import pkgutil
import time
from typing import Callable, Dict, Any, List
from pathlib import Path
from core import journal

_OUTILS: Dict[str, Dict[str, Any]] = {}

def outil(
    nom: str,
    description: str,
    parametres: Dict[str, Any],
    securite: str = "N1",       # N1 = lecture, N2 = action locale, N3 = critique
    affichage: str = "auto"
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
        journal.enregistrer_audit(nom, arguments, "INCONNU", "REJETE", "Outil non enregistré")
        return f"Erreur : L'outil '{nom}' n'est pas enregistré."
    
    info = _OUTILS[nom]
    fonction = info["fonction"]
    sec = info["securite"]
    t0 = time.time()
    
    try:
        sig = inspect.signature(fonction)
        if len(sig.parameters) == 0:
            resultat = fonction()
        else:
            resultat = fonction(**arguments)
        duree = (time.time() - t0) * 1000.0
        journal.enregistrer_audit(nom, arguments, sec, "SUCCES", str(resultat), duree)
        return str(resultat)
    except Exception as e:
        duree = (time.time() - t0) * 1000.0
        journal.enregistrer_audit(nom, arguments, sec, "ERREUR", str(e), duree)
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
