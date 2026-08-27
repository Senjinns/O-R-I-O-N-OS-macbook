from core.registre import outil
from core import config

@outil(
    nom="changer_personnalite",
    description="Modifie la personnalité d'Orion (orion_sarcastique, neutre, concis).",
    parametres={
        "type": "object",
        "properties": {
            "nom": {
                "type": "string",
                "enum": ["orion_sarcastique", "neutre", "concis"],
                "description": "Nom du persona"
            }
        },
        "required": ["nom"]
    },
    securite="N2"
)
def changer_personnalite(nom: str) -> str:
    config.definir("assistant.personnalite", nom)
    return f"Personnalité basculée sur '{nom}'."
