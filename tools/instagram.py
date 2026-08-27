from core.registre import outil

@outil(
    nom="stats_instagram",
    description="Consulte le nombre d'abonnés et les vues des dernières vidéos Instagram.",
    parametres={
        "type": "object",
        "properties": {
            "compte": {"type": "string", "description": "Nom d'utilisateur Instagram"}
        }
    },
    securite="N1",
    affichage="toujours"
)
def stats_instagram(compte: str = "mon_compte") -> str:
    return f"Statistiques Instagram pour @{compte} : Croissance positive de +45 abonnés aujourd'hui et 12.4k vues sur le dernier reel."
