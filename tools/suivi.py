from core.registre import outil
from core import hub_contenu

@outil(
    nom="pipeline_video",
    description="Affiche l'état d'avancement des vidéos en cours de production (idées, tournage, montage, publication).",
    parametres={"type": "object", "properties": {}},
    securite="N1",
    affichage="toujours"
)
def pipeline_video() -> str:
    return hub_contenu.lister_pipeline()
