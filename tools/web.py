from core.registre import outil

@outil(
    nom="recherche_web",
    description="Effectue une recherche rapide sur Internet et renvoie les résultats clés.",
    parametres={
        "type": "object",
        "properties": {
            "requete": {"type": "string", "description": "Termes de la recherche"}
        },
        "required": ["requete"]
    },
    securite="N1",
    affichage="toujours"
)
def recherche_web(requete: str) -> str:
    try:
        import requests
        url = f"https://api.duckduckgo.com/?q={requete}&format=json&no_html=1&skip_disambig=1"
        resp = requests.get(url, timeout=5).json()
        abstract = resp.get("AbstractText")
        if abstract:
            return f"Résultat pour '{requete}' : {abstract}"
        return f"Recherche complétée pour '{requete}'. Plusieurs sources disponibles en ligne."
    except Exception as e:
        return f"Erreur de recherche web : {e}"
