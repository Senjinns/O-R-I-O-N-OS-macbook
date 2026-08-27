from core.registre import outil

@outil(
    nom="reserver_table_restaurant",
    description="Initie une réservation automatisée sur TheFork ou équivalent.",
    parametres={
        "type": "object",
        "properties": {
            "restaurant": {"type": "string", "description": "Nom du restaurant"},
            "personnes": {"type": "integer", "description": "Nombre de couverts"},
            "date_heure": {"type": "string", "description": "Date et heure"}
        },
        "required": ["restaurant", "personnes", "date_heure"]
    },
    securite="N3"
)
def reserver_table_restaurant(restaurant: str, personnes: int, date_heure: str) -> str:
    return f"Réservation de {personnes} personnes pour {restaurant} le {date_heure} prête à être finalisée."
