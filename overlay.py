from core import journal

LOG = journal.obtenir("overlay")

def memoriser(texte: str, typ: str = "reponse"):
    pass

def afficher(texte: str, type: str = "reponse"):
    LOG.info(f"[OVERLAY] {texte}")

def est_muet() -> bool:
    return False
