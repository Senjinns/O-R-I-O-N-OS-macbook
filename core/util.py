import unicodedata
import subprocess
from typing import Tuple

def sans_accents(texte: str) -> str:
    if not texte:
        return ""
    texte_norm = unicodedata.normalize("NFD", texte)
    return "".join(c for c in texte_norm if unicodedata.category(c) != "Mn").lower().strip()

def echapper_applescript(texte: str) -> str:
    """Echappe les caracteres speciaux pour eviter toute injection AppleScript."""
    if not texte:
        return ""
    return texte.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").replace("\r", " ")

def executer_applescript(script: str) -> Tuple[bool, str]:
    try:
        process = subprocess.Popen(
            ["osascript", "-e", script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(timeout=10)
        if process.returncode == 0:
            return True, stdout.strip()
        return False, stderr.strip()
    except Exception as e:
        return False, str(e)
