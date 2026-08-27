import threading
from core import journal

LOG = journal.obtenir("hud")

def afficher(texte: str, type_message: str = "info"):
    LOG.info(f"[HUD {type_message.upper()}] {texte}")
