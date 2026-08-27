from core.registre import outil
from core import config

@outil(
    nom="controler_obs",
    description="Contrôle OBS Studio (démarrer/arrêter enregistrement ou stream, changer de scène).",
    parametres={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["start_recording", "stop_recording", "start_streaming", "stop_streaming", "switch_scene"],
                "description": "Action OBS"
            },
            "scene_nom": {"type": "string", "description": "Nom de la scène cible (si action = switch_scene)"}
        },
        "required": ["action"]
    },
    securite="N2"
)
def controler_obs(action: str, scene_nom: str = None) -> str:
    if not config.reglage("obs.actif", False):
        return "OBS WebSocket désactivé dans config.yaml."
    return f"OBS Studio : Action '{action}' exécutée sur la scène '{scene_nom}'."
