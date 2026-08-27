from core.registre import outil
from core.util import executer_applescript

@outil(
    nom="resumer_onglet_actif",
    description="Lit le titre et l'URL de l'onglet actif dans Safari ou Chrome.",
    parametres={"type": "object", "properties": {}},
    securite="N1",
    affichage="toujours"
)
def resumer_onglet_actif() -> str:
    script_safari = 'tell application "Safari" to get (URL of current tab of front window & " - " & name of current tab of front window)'
    succes, sortie = executer_applescript(script_safari)
    if succes:
        return f"Onglet actif dans Safari : {sortie}"
    
    script_chrome = 'tell application "Google Chrome" to get (URL of active tab of front window & " - " & title of active tab of front window)'
    succes_c, sortie_c = executer_applescript(script_chrome)
    if succes_c:
        return f"Onglet actif dans Chrome : {sortie_c}"
        
    return "Aucun navigateur actif détecté."
