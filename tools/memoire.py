from core.registre import outil
from core import memoire

@outil(
    nom="se_souvenir",
    description="Mémorise une information importante sur l'utilisateur, ses préférences ou ses projets.",
    parametres={
        "type": "object",
        "properties": {
            "cle": {"type": "string", "description": "Sujet ou mot clé (ex: plat_prefere, prenom_conjoint, projet_en_cours)"},
            "valeur": {"type": "string", "description": "L'information exacte à retenir"}
        },
        "required": ["cle", "valeur"]
    },
    securite="N1"
)
def se_souvenir(cle: str, valeur: str) -> str:
    return memoire.memoriser(cle, valeur)

@outil(
    nom="rappeler_souvenir",
    description="Recherche dans la mémoire à long terme une information enregistrée.",
    parametres={
        "type": "object",
        "properties": {
            "cle": {"type": "string", "description": "Sujet ou terme à rechercher"}
        },
        "required": ["cle"]
    },
    securite="N1",
    affichage="toujours"
)
def rappeler_souvenir(cle: str) -> str:
    return memoire.rappeler(cle)
