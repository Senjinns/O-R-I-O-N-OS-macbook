from core.registre import outil
from core import hub_contenu

@outil(
    nom="ajouter_idee_contenu",
    description="Ajoute une idée de contenu vidéo au pipeline du créateur.",
    parametres={
        "type": "object",
        "properties": {
            "titre": {"type": "string", "description": "Titre du projet de vidéo"},
            "notes": {"type": "string", "description": "Détails ou points clés"}
        },
        "required": ["titre"]
    },
    securite="N1"
)
def ajouter_idee_contenu(titre: str, notes: str = "") -> str:
    return hub_contenu.ajouter_idee_video(titre, notes)
