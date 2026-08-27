from core.registre import outil

@outil(
    nom="obtenir_meteo",
    description="Récupère la météo et les prévisions en direct pour n'importe quelle ville (service gratuit Open-Meteo / wttr.in).",
    parametres={
        "type": "object",
        "properties": {
            "ville": {"type": "string", "description": "Nom de la ville (ex: Paris, Lyon, Marseille, Montreal)"}
        },
        "required": ["ville"]
    },
    securite="N1"
)
def obtenir_meteo(ville: str = "Paris") -> str:
    try:
        import requests
        url = f"https://wttr.in/{ville}?format=%C:+%t+(ressenti+%f),+Vent+%w,+Humidité+%h"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return f"Météo à {ville} : {resp.text.strip()}."
        return f"Impossible de récupérer la météo pour {ville}."
    except Exception as e:
        return f"Erreur météo : {e}"
