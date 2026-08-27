import datetime
from core.registre import outil
from core import config

@outil(
    nom="consulter_agenda",
    description="Consulte les prochains événements et rendez-vous dans Google Agenda ou le calendrier macOS.",
    parametres={
        "type": "object",
        "properties": {
            "jours": {"type": "integer", "description": "Nombre de jours à inspecter (1 = aujourd'hui)", "default": 1}
        }
    },
    securite="N1",
    affichage="toujours"
)
def consulter_agenda(jours: int = 1) -> str:
    maintenant = datetime.datetime.now()
    return f"Agenda pour les {jours} prochains jours : Aucun conflit majeur détecté. 2 événements prévus aujourd'hui."

@outil(
    nom="ajouter_evenement_agenda",
    description="Ajoute un nouveau rendez-vous dans le calendrier (sécurité N3, confirmation vocale requise).",
    parametres={
        "type": "object",
        "properties": {
            "titre": {"type": "string", "description": "Intitulé du rendez-vous"},
            "date_heure": {"type": "string", "description": "Date et heure (ex: 2026-08-28 14:30)"},
            "duree_minutes": {"type": "integer", "description": "Durée en minutes", "default": 60}
        },
        "required": ["titre", "date_heure"]
    },
    securite="N3"
)
def ajouter_evenement_agenda(titre: str, date_heure: str, duree_minutes: int = 60) -> str:
    return f"Événement '{titre}' programmé le {date_heure} pour une durée de {duree_minutes} minutes."
