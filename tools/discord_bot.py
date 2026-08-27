from core.registre import outil

@outil(
    nom="recapitulatif_discord",
    description="Résume les messages récents et mentions sur Discord.",
    parametres={"type": "object", "properties": {}},
    securite="N1",
    affichage="toujours"
)
def recapitulatif_discord() -> str:
    return "Sur Discord : 2 mentions dans le salon général et aucun message urgent en privé."
