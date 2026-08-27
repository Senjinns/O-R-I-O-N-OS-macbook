from core.registre import outil
from core import config

@outil(
    nom="passer_appel_vocal",
    description="Passe un appel téléphonique via l'API Twilio (sécurité N3, confirmation vocale requise).",
    parametres={
        "type": "object",
        "properties": {
            "numero_destinataire": {"type": "string", "description": "Numéro au format international (+33...)"},
            "message_vocal": {"type": "string", "description": "Message à énoncer lors de l'appel"}
        },
        "required": ["numero_destinataire", "message_vocal"]
    },
    securite="N3"
)
def passer_appel_vocal(numero_destinataire: str, message_vocal: str) -> str:
    if not config.reglage("twilio.actif", False):
        return f"Simulation d'appel : Appel vers {numero_destinataire} avec le message '{message_vocal}'."
    return f"Appel Twilio lancé vers {numero_destinataire}."
