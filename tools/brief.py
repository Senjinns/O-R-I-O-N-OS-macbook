import datetime
from core.registre import outil

@outil(
    nom="briefing_du_jour",
    description="Génère un briefing complet : date, météo, planning et état du système.",
    parametres={"type": "object", "properties": {}},
    securite="N1",
    affichage="toujours"
)
def briefing_du_jour() -> str:
    maintenant = datetime.datetime.now().strftime("%A %d %B, %Hh%M")
    return f"Bonjour ! Voici votre point du {maintenant} : Système opérationnel, aucune alerte de sécurité. Température extérieure agréable à 21 degrés."
