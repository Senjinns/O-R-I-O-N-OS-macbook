import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.header import decode_header
from core.registre import outil
from core import config, journal

LOG = journal.obtenir("mail")

@outil(
    nom="lire_derniers_mails",
    description="Consulte les derniers emails non lus dans Gmail via IMAP sécurisé.",
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
    mdp = config.reglage("mail.mot_de_passe_app")
    serveur_imap = config.reglage("mail.serveur_imap", "imap.gmail.com")
    
    if not adresse or not mdp:
        return f"Simulation Gmail : 2 nouveaux messages reçus pour {adresse or 'utilisateur'}."
        
    try:
        mail = imaplib.IMAP4_SSL(serveur_imap)
        mail.login(adresse, mdp)
        mail.select("inbox")
        status, messages = mail.search(None, 'UNSEEN')
        ids = messages[0].split()
        
        if not ids:
            return "Aucun email non lu dans votre boîte de réception."
            
        derniers = ids[-nombre:]
        resultats = []
        for i in reversed(derniers):
            _, data = mail.fetch(i, "(RFC822.HEADER)")
            msg = email.message_from_bytes(data[0][1])
            sujet, enc = decode_header(msg.get("Subject", "Sans sujet"))[0]
            if isinstance(sujet, bytes):
                sujet = sujet.decode(enc or "utf-8", errors="ignore")
            expediteur = msg.get("From", "Inconnu")
            resultats.append(f"- De {expediteur} : {sujet}")
            
        mail.close()
        mail.logout()
        return "Derniers emails non lus :\n" + "\n".join(resultats)
    except Exception as e:
        return f"Erreur de connexion IMAP : {e}"

@outil(
    nom="envoyer_mail",
    description="Envoie un email via SMTP SSL (N3, confirmation obligatoire).",
    parametres={
        "type": "object",
        "properties": {
            "destinataire": {"type": "string", "description": "Adresse email"},
            "sujet": {"type": "string", "description": "Objet"},
            "corps": {"type": "string", "description": "Contenu du message"}
        },
        "required": ["destinataire", "sujet", "corps"]
    },
    securite="N3"
)
def envoyer_mail(destinataire: str, sujet: str, corps: str) -> str:
    adresse = config.reglage("mail.adresse")
    mdp = config.reglage("mail.mot_de_passe_app")
    serveur_smtp = config.reglage("mail.serveur_smtp", "smtp.gmail.com")
    
    if not adresse or not mdp:
        return f"Simulation : Email envoyé avec succès à {destinataire} (sujet: '{sujet}')."
        
    try:
        msg = MIMEText(corps, "plain", "utf-8")
        msg["Subject"] = sujet
        msg["From"] = adresse
        msg["To"] = destinataire
        
        with smtplib.SMTP_SSL(serveur_smtp, 465) as server:
            server.login(adresse, mdp)
            server.sendmail(adresse, [destinataire], msg.as_string())
        return f"Email envoyé avec succès à {destinataire}."
    except Exception as e:
        return f"Erreur lors de l'envoi SMTP : {e}"
