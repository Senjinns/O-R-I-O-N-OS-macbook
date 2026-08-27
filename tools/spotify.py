from core.registre import outil
from core.util import executer_applescript

@outil(
    nom="controler_spotify",
    description="Pilote l'application Spotify sur Mac (play, pause, suivant, precedent, statut).",
    parametres={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["play", "pause", "playpause", "suivant", "precedent", "statut"],
                "description": "L'action à effectuer sur Spotify"
            }
        },
        "required": ["action"]
    },
    securite="N2"
)
def controler_spotify(action: str) -> str:
    script_map = {
        "play": 'tell application "Spotify" to play',
        "pause": 'tell application "Spotify" to pause',
        "playpause": 'tell application "Spotify" to playpause',
        "suivant": 'tell application "Spotify" to next track',
        "precedent": 'tell application "Spotify" to previous track',
        "statut": 'tell application "Spotify" to get (name of current track & " par " & artist of current track)'
    }
    
    script = script_map.get(action.lower())
    if not script:
        return "Action Spotify non reconnue."
        
    succes, sortie = executer_applescript(script)
    if succes:
        if action == "statut":
            return f"Actuellement en lecture : {sortie}"
        return f"Spotify : {action} exécuté."
    return "Spotify n'est pas actif ou a rencontré une erreur."
