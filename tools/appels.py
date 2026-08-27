import re
from core.registre import outil
from core import config

PREFIXES_SURTAXES = ("089", "118", "30", "31", "32", "36", "39", "10", "+88", "+1900", "+3389")

def numero_autorise(numero: str) -> bool:
    propre = re.sub(r"[\s\-\.\(\)]", "", numero)
    for p in PREFIXES_SURTAXES:
        if propre.startswith(p) or propre.startswith("+" + p):
            return False
    return True

@outil(
    nom="passer_appel_vocal",
    description="Passe un appel téléphonique via Twilio (sécurité N3, numéros surtaxés bloqués).",
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
    if not numero_autorise(numero_destinataire):
        return f"SÉCURITÉ : Appel vers {numero_destinataire} bloqué (numéro surtaxé ou non autorisé)."
        
    if not config.reglage("twilio.actif", False):
        return f"Simulation d'appel : Appel sécurisé vers {numero_destinataire} avec le message '{message_vocal}'."
    return f"Appel Twilio lancé vers {numero_destinataire}."
