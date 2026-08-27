from core.registre import outil
from core import config

@outil(
    nom="controler_alexa_routine",
    description="Déclenche une routine ou diffuse une annonce sur les enceintes Amazon Alexa / Echo.",
    parametres={
        "type": "object",
        "properties": {
            "nom_routine": {"type": "string", "description": "Nom de la routine Alexa à activer"}
        },
        "required": ["nom_routine"]
    },
    securite="N2"
)
def controler_alexa_routine(nom_routine: str) -> str:
    if not config.reglage("alexa.actif", False):
        return "Intégration Alexa non activée dans config.yaml."
    return f"Routine Alexa '{nom_routine}' déclenchée."
