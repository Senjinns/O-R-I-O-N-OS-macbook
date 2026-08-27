from core.registre import outil
from core.util import executer_applescript

@outil(
    nom="creer_note_apple",
    description="Crée une nouvelle note dans l'application Apple Notes sur le Mac.",
    parametres={
        "type": "object",
        "properties": {
            "titre": {"type": "string", "description": "Titre ou première ligne de la note"},
            "contenu": {"type": "string", "description": "Texte détaillé de la note"}
        },
        "required": ["titre", "contenu"]
    },
    securite="N2"
)
def creer_note_apple(titre: str, contenu: str) -> str:
    corps = f"<b>{titre}</b><br><br>{contenu}"
    script = f'''
    tell application "Notes"
        tell account "iCloud"
            make new note with properties {{name:"{titre}", body:"{corps}"}}
        end tell
    end tell
    '''
    succes, msg = executer_applescript(script)
    if succes:
        return f"Note '{titre}' créée dans Apple Notes."
    return f"Note enregistrée avec message : {msg}"
