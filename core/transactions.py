import time
from core import journal, tts

LOG = journal.obtenir()

MOTS_ACCORD = {"oui", "ouais", "confirme", "vas-y", "fais-le", "ok", "envoie", "valide", "d'accord"}
MOTS_REFUS = {"non", "annule", "arrete", "stop", "pas du tout", "non non"}

def demander_confirmation_vocale(action_description: str, audio_engine) -> bool:
    question = f"Confirmez-vous : {action_description} ?"
    LOG.warning(f"[Sécurité N3] {question}")
    tts.tts().synthetiser(question)
    
    # Écoute de la réponse utilisateur (3s max)
    audio = audio_engine.enregistrer_commande(duree_max=4, silence_fin=1.0)
    reponse = audio_engine.transcrire_audio(audio).lower().strip()
    
    LOG.info(f"[Sécurité N3] Réponse entendue : '{reponse}'")
    if any(m in reponse for m in MOTS_ACCORD):
        return True
    return False
