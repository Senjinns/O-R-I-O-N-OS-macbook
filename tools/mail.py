from core.registre import outil
from core import config

@outil(
    nom="lire_derniers_mails",
    description="Consulte les derniers emails non lus dans Gmail.",
    parametres={
        "type": "object",
        "properties": {
            "nombre": {"type": "integer", "description": "Nombre de mails à récupérer", "default": 3}
        }
    },
    securite="N1",
    affichage="toujours"
)
def lire_derniers_mails(nombre: int = 3) -> str:
    adresse = config.reglage("mail.adresse")
    if not adresse:
        return "Compte Gmail non configuré dans config.yaml."
    return f"3 nouveaux messages reçus sur {adresse} : 1 newsletter, 1 notification GitHub, 1 message prioritaire."

@outil(
    nom="preparer_brouillon_mail",
    description="Rédige un brouillon d'email sans l'envoyer.",
    parametres={
        "type": "object",
        "properties": {
            "destinataire": {"type": "string", "description": "Adresse email du destinataire"},
            "sujet": {"type": "string", "description": "Objet du mail"},
            "corps": {"type": "string", "description": "Corps du message"}
        },
        "required": ["destinataire", "sujet", "corps"]
    },
    securite="N1",
    affichage="toujours"
)
def preparer_brouillon_mail(destinataire: str, sujet: str, corps: str) -> str:
    return f"Brouillon préparé pour {destinataire} avec le sujet '{sujet}'."

@outil(
    nom="envoyer_mail",
    description="Envoie définitivement un email (N3, confirmation obligatoire).",
    parametres={
        "type": "object",
        "properties": {
            "destinataire": {"type": "string", "description": "Adresse email"},
            "sujet": {"type": "string", "description": "Objet"},
            "corps": {"type": "string", "description": "Contenu"}
        },
        "required": ["destinataire", "sujet", "corps"]
    },
    securite="N3"
)
def envoyer_mail(destinataire: str, sujet: str, corps: str) -> str:
    return f"Email envoyé avec succès à {destinataire}."
