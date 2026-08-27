from core.registre import outil

@outil(
    nom="controler_gestes_webcam",
    description="Active ou désactive la reconnaissance de gestes de la main par webcam.",
    parametres={
        "type": "object",
        "properties": {
            "actif": {"type": "boolean", "description": "True pour activer, False pour stopper"}
        },
        "required": ["actif"]
    },
    securite="N2"
)
def controler_gestes_webcam(actif: bool) -> str:
    return f"Détection de gestes webcam : {'Activée' if actif else 'Désactivée'}."
