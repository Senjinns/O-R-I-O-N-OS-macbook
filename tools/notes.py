from core.registre import outil
from core.util import executer_applescript, echapper_applescript

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
    t_propre = echapper_applescript(titre)
    c_propre = echapper_applescript(contenu)
    corps = f"<b>{t_propre}</b><br><br>{c_propre}"
    
    script = (
        'tell application "Notes"\n'
        '  tell account "iCloud"\n'
        f'    make new note with properties {{name:"{t_propre}", body:"{corps}"}}\n'
        '  end tell\n'
        'end tell'
    )
    succes, msg = executer_applescript(script)
    if succes:
        return f"Note '{titre}' créée avec succès dans Apple Notes."
    return f"Erreur lors de la création de la note : {msg}"
