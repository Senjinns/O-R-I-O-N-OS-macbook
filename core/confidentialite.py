import re

MOTIFS_SECRETS = [
    (re.compile(r"sk-ant-[a-zA-Z0-9_\-]{20,}", re.IGNORECASE), "[SECRET_ANTHROPIC_MASQUÉ]"),
    (re.compile(r"ghp_[a-zA-Z0-9]{30,}", re.IGNORECASE), "[SECRET_GITHUB_MASQUÉ]"),
    (re.compile(r"gho_[a-zA-Z0-9]{30,}", re.IGNORECASE), "[SECRET_GITHUB_MASQUÉ]"),
    (re.compile(r"Bearer\s+[a-zA-Z0-9_\-\.]{20,}", re.IGNORECASE), "Bearer [TOKEN_MASQUÉ]"),
    (re.compile(r"AC[a-zA-Z0-9]{32}", re.IGNORECASE), "[TWILIO_SID_MASQUÉ]"),
    (re.compile(r"\b(?:\d[ -]*?){13,16}\b"), "[NUMÉRO_CARTE_MASQUÉ]"),
    (re.compile(r"(?i)(?:mot de passe|password|pwd|secret)\s*[:=]\s*\S+"), "mot_de_passe: [MASQUÉ]"),
]

def masquer_secrets(texte: str) -> str:
    """Remplace tous les secrets sensibles détectés par des placeholders sécurisés."""
    if not isinstance(texte, str) or not texte:
        return str(texte) if texte is not None else ""
    
    texte_filtre = texte
    for motif, remplacement in MOTIFS_SECRETS:
        texte_filtre = motif.sub(remplacement, texte_filtre)
    return texte_filtre
