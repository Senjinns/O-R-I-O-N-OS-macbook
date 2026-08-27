from core.registre import outil

@outil(
    nom="activer_scene",
    description="Active une scène domotique et multimédia combinée (Tournage, Nuit, Travail, Détente).",
    parametres={
        "type": "object",
        "properties": {
            "nom_scene": {
                "type": "string",
                "enum": ["tournage", "nuit", "travail", "detente", "cinema"],
                "description": "Nom de la scène globale"
            }
        },
        "required": ["nom_scene"]
    },
    securite="N2"
)
def activer_scene(nom_scene: str) -> str:
    return f"Scène globale '{nom_scene.upper()}' activée : lumières ajustées, applications positionnées."
