from core.registre import outil
from core import config

@outil(
    nom="controler_lumieres_hue",
    description="Allume, éteint ou ajuste la luminosité/couleur des lumières Philips Hue.",
    parametres={
        "type": "object",
        "properties": {
            "allume": {"type": "boolean", "description": "True pour allumer, False pour éteindre"},
            "luminosite": {"type": "integer", "description": "Luminosité de 1 à 254", "minimum": 1, "maximum": 254},
            "piece": {"type": "string", "description": "Nom du groupe ou de la pièce (ex: Salon, Chambre)"}
        }
    },
    securite="N2"
)
def controler_lumieres_hue(allume: bool = None, luminosite: int = None, piece: str = None) -> str:
    try:
        import requests
    except ImportError:
        return "Module 'requests' non installé."
        
    pont = config.reglage("hue.pont_ip")
    cle = config.reglage("hue.cle_utilisateur")
    
    if not pont or not cle:
        return "Philips Hue non configuré dans config.yaml (pont_ip / cle_utilisateur)."
    
    try:
        url = f"http://{pont}/api/{cle}/groups/0/action"
        corps = {}
        if allume is not None:
            corps["on"] = allume
        if luminosite is not None:
            corps["bri"] = luminosite
            
        r = requests.put(url, json=corps, timeout=3)
        if r.status_code == 200:
            return f"Lumières Hue ajustées : {'Allumées' if allume else 'Éteintes' if allume is False else ''}."
        return f"Réponse Hue : {r.text}"
    except Exception as e:
        return f"Erreur de communication Hue : {e}"
