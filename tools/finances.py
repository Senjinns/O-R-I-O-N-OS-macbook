from core.registre import outil

@outil(
    nom="suivi_abonnements",
    description="Liste les abonnements actifs et les dépenses récurrentes.",
    parametres={"type": "object", "properties": {}},
    securite="N1",
    affichage="toujours"
)
def suivi_abonnements() -> str:
    return "Abonnements actifs ce mois-ci : Claude Pro (20$), Spotify (10.99€), iCloud (2.99€). Total estimé : ~32€/mois."
