from core.registre import outil
from core import config

@outil(
    nom="controler_lumiere_video",
    description="Allume ou règle les lumières vidéo de tournage (Aputure / Amaran / Elgato Key Light).",
    parametres={
        "type": "object",
        "properties": {
            "allume": {"type": "boolean", "description": "True pour allumer, False pour éteindre"},
            "intensite": {"type": "integer", "description": "Pourcentage de 0 à 100"}
        }
    },
    securite="N2"
)
def controler_lumiere_video(allume: bool = None, intensite: int = None) -> str:
    return f"Éclairage studio vidéo réglé : allume={allume}, intensite={intensite}%."
