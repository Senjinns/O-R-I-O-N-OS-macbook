import subprocess
import base64
import os
import tempfile
from core.registre import outil
from core import config, journal

LOG = journal.obtenir()

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
    cle = config.reglage("anthropic.cle")
    if not cle:
        return "Clé API Anthropic manquante dans config.yaml pour l'analyse visuelle."

    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    temp_path = temp_file.name
    temp_file.close()

    try:
        subprocess.run(["screencapture", "-x", "-t", "jpg", temp_path], check=True)
        
        with open(temp_path, "rb") as f:
            b64_image = base64.b64encode(f.read()).decode("utf-8")
        
        import anthropic
        client = anthropic.Anthropic(api_key=cle)
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
                    {"type": "text", "text": f"Analyse cette capture d'écran et réponds de façon concise à la question : {question}"}
                ]
            }]
        )
        return resp.content[0].text
    except Exception as e:
        return f"Erreur lors de l'analyse d'écran : {e}"
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
