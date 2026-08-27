import logging
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_LOGS = RACINE / "logs"
DOSSIER_LOGS.mkdir(parents=True, exist_ok=True)
FICHIER_LOG = DOSSIER_LOGS / "orion.log"

# Codes couleurs ANSI pour le terminal macOS
BLEU = "[94m"
CYAN = "[96m"
VERT = "[92m"
JAUNE = "[93m"
ROUGE = "[91m"
MAGENTA = "[95m"
GRIS = "[90m"
RESET = "[0m"
GRAS = "[1m"

class FormateurCouleur(logging.Formatter):
    FORMATS = {
        logging.DEBUG: GRIS + "[DEBUG] %(message)s" + RESET,
        logging.INFO: CYAN + "[ORION] " + RESET + "%(message)s",
        logging.WARNING: JAUNE + "[ATTENTION] %(message)s" + RESET,
        logging.ERROR: ROUGE + "[ERREUR] %(message)s" + RESET,
        logging.CRITICAL: GRAS + ROUGE + "[CRITIQUE] %(message)s" + RESET,
    }

    def format(self, record):
        fmt = self.FORMATS.get(record.levelno, "%(message)s")
        formatter = logging.Formatter(fmt)
        return formatter.format(record)

def obtenir(nom="orion") -> logging.Logger:
    logger = logging.getLogger(nom)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Console macOS
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(FormateurCouleur())
        logger.addHandler(ch)
        
        # Fichier persistant
        fh = logging.FileHandler(FICHIER_LOG, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s"))
        logger.addHandler(fh)
        
    return logger
