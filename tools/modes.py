from core.registre import outil

@outil(
    nom="activer_mode",
    description="Change le mode de fonctionnement du Mac (Concentration, Ne Pas Déranger, Performance).",
    parametres={
        "type": "object",
        "properties": {
            "mode": {
                "type": "string",
                "enum": ["concentration", "stream", "silencieux", "normal"],
                "description": "Mode système"
            }
        },
        "required": ["mode"]
    },
    securite="N2"
)
def activer_mode(mode: str) -> str:
    return f"Mode '{mode}' activé sur le Mac."
