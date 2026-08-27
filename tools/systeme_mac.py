import subprocess
import os
from core.registre import outil
from core.util import executer_applescript

@outil(
    nom="controler_volume",
    description="Règle ou coupe le volume sonore principal du Mac.",
    parametres={
        "type": "object",
        "properties": {
            "niveau": {"type": "integer", "description": "Niveau sonore entre 0 et 100", "minimum": 0, "maximum": 100},
            "muet": {"type": "boolean", "description": "Si true, coupe le son du Mac"}
        }
    },
    securite="N2"
)
def controler_volume(niveau: int = None, muet: bool = None) -> str:
    if muet is True:
        executer_applescript("set volume output muted true")
        return "Son coupé sur le Mac."
    elif muet is False:
        executer_applescript("set volume output muted false")
    
    if niveau is not None:
        valeur = max(0, min(100, int(niveau)))
        executer_applescript(f"set volume output volume {valeur}")
        return f"Volume réglé à {valeur}%."
    return "Volume ajusté."

@outil(
    nom="lancer_application",
    description="Ouvre n'importe quelle application installée sur le Mac (Spotify, Chrome, VS Code, Discord, Notes, etc.).",
    parametres={
        "type": "object",
        "properties": {
            "nom_application": {"type": "string", "description": "Nom de l'application (ex: Spotify, Safari, Visual Studio Code, Discord)"}
        },
        "required": ["nom_application"]
    },
    securite="N2"
)
def lancer_application(nom_application: str) -> str:
    try:
        cmd = ["open", "-a", nom_application]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            return f"Application {nom_application} lancée."
        return f"Impossible de trouver l'application {nom_application}."
    except Exception as e:
        return f"Erreur lors du lancement de {nom_application} : {e}"

@outil(
    nom="verrouiller_mac",
    description="Verrouille l'écran ou met en veille l'affichage du Mac.",
    parametres={"type": "object", "properties": {}},
    securite="N2"
)
def verrouiller_mac() -> str:
    try:
        subprocess.run(["pmset", "displaysleepnow"], check=True)
        return "Écran du Mac verrouillé et mis en veille."
    except Exception as e:
        return f"Erreur de verrouillage : {e}"

@outil(
    nom="eteindre_mac",
    description="Met en veille prolongée ou éteint proprement le Mac.",
    parametres={"type": "object", "properties": {}},
    securite="N3"
)
def eteindre_mac() -> str:
    succes, msg = executer_applescript('tell application "System Events" to sleep')
    if succes:
        return "Mise en veille du Mac initiée."
    return f"Échec de mise en veille : {msg}"
