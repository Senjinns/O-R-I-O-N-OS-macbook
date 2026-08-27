from core.registre import outil

@outil(
    nom="afficher_sur_overlay",
    description="Affiche un texte ou des données sur l'overlay flottant à l'écran.",
    parametres={
        "type": "object",
        "properties": {
            "texte": {"type": "string", "description": "Texte à afficher"}
        },
        "required": ["texte"]
    },
    securite="N1",
    affichage="toujours"
)
def afficher_sur_overlay(texte: str) -> str:
    return f"Texte affiché sur le HUD : {texte}"
