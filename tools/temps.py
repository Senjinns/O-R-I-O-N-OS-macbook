import datetime
import threading
import time
from core.registre import outil
from core import tts

@outil(
    nom="heure_actuelle",
    description="Donne la date et l'heure courante.",
    parametres={"type": "object", "properties": {}},
    securite="N1"
)
def heure_actuelle() -> str:
    maintenant = datetime.datetime.now()
    return maintenant.strftime("Il est %H heures %M le %A %d %B %Y.")

@outil(
    nom="creer_minuteur",
    description="Crée un minuteur vocal de X secondes ou minutes.",
    parametres={
        "type": "object",
        "properties": {
            "secondes": {"type": "integer", "description": "Durée en secondes"}
        },
        "required": ["secondes"]
    },
    securite="N2"
)
def creer_minuteur(secondes: int) -> str:
    def _timer():
        time.sleep(secondes)
        tts.tts().synthetiser("Bip bip bip ! Votre minuteur est terminé.")
        
    t = threading.Thread(target=_timer, daemon=True)
    t.start()
    return f"Minuteur de {secondes} secondes programmé."
