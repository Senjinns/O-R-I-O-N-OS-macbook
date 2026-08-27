import logging
import sys
import json
import datetime
from pathlib import Path
from core.confidentialite import masquer_secrets

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_LOGS = RACINE / "logs"
DOSSIER_LOGS.mkdir(parents=True, exist_ok=True)
FICHIER_LOG = DOSSIER_LOGS / "orion.log"
FICHIER_AUDIT = DOSSIER_LOGS / "audit_securite.jsonl"

def enregistrer_audit(nom_outil: str, arguments: dict, securite: str, statut: str, resultat: str, duree_ms: float = 0.0):
    """Écrit une entrée immuable dans le journal d'audit de sécurité."""
    entree = {
        "timestamp": datetime.datetime.now().isoformat(),
        "outil": nom_outil,
        "niveau_securite": securite,
        "arguments": json.loads(masquer_secrets(json.dumps(arguments, ensure_ascii=False))),
        "statut": statut,
        "resultat": masquer_secrets(str(resultat))[:300],
        "duree_ms": round(duree_ms, 2)
    }
    try:
        with open(FICHIER_AUDIT, "a", encoding="utf-8") as f:
            f.write(json.dumps(entree, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[AUDIT] Erreur d'écriture audit : {e}")

class FormateurCouleur(logging.Formatter):
    def format(self, record):
        message = masquer_secrets(record.getMessage())
        record.msg = message
        formatter = logging.Formatter(f"[96m[ORION][0m {message}")
        return formatter.format(record)

def obtenir(nom="orion") -> logging.Logger:
    logger = logging.getLogger(nom)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(FormateurCouleur())
        logger.addHandler(ch)
        
        fh = logging.FileHandler(FICHIER_LOG, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(fh)
    return logger
