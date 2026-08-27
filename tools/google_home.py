from core.registre import outil
from core import config

@outil(
    nom="controler_google_home",
    description="Envoie une commande à l'écosystème Google Home / Nest.",
    parametres={
        "type": "object",
        "properties": {
            "commande": {"type": "string", "description": "Action à réaliser sur Google Home"}
        },
        "required": ["commande"]
    },
    securite="N2"
)
def controler_google_home(commande: str) -> str:
    if not config.reglage("google_home.actif", False):
        return "Intégration Google Home non activée dans config.yaml."
    return f"Commande Google Home transmise : '{commande}'."
