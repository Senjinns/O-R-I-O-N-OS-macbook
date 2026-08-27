import subprocess
import base64
import os
from pathlib import Path
from core.registre import outil
from core import config, journal

LOG = journal.obtenir()
TMP_SCREEN = "/tmp/orion_ecran.jpg"

@outil(
    nom="analyser_ecran",
    description="Prend une capture d'écran du Mac et analyse ce qui y est affiché avec Claude Vision.",
    parametres={
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "Ce qu'il faut analyser ou rechercher sur l'écran"}
        },
        "required": ["question"]
    },
    securite="N2",
    affichage="toujours"
)
def analyser_ecran(question: str) -> str:
    try:
        # Capture instantanée macOS
        subprocess.run(["screencapture", "-x", "-t", "jpg", TMP_SCREEN], check=True)
        if not os.path.exists(TMP_SCREEN):
            return "Impossible de capturer l'écran."
        
        with open(TMP_SCREEN, "rb") as f:
            b64_image = base64.b64encode(f.read()).decode("utf-8")
        
        import anthropic
        client = anthropic.Anthropic(api_key=config.reglage("anthropic.cle"))
        modele = config.reglage("anthropic.modele_rapide", "claude-3-5-haiku-20241022")
        
        resp = client.messages.create(
            model=modele,
            max_tokens=600,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": b64_image
                        }
                    },
                    {"type": "text", "text": f"Analyse cette capture d'écran et réponds en une phrase concise à la question suivante : {question}"}
                ]
            }]
        )
        
        try:
            os.remove(TMP_SCREEN)
        except Exception:
            pass
            
        return resp.content[0].text
    except Exception as e:
        return f"Erreur lors de l'analyse d'écran : {e}"
