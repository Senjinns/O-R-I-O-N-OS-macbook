from core.registre import outil

@outil(
    nom="cliquer_position",
    description="Clique à des coordonnées X, Y spécifiques sur l'écran du Mac.",
    parametres={
        "type": "object",
        "properties": {
            "x": {"type": "integer", "description": "Coordonnée X"},
            "y": {"type": "integer", "description": "Coordonnée Y"}
        },
        "required": ["x", "y"]
    },
    securite="N2"
)
def cliquer_position(x: int, y: int) -> str:
    return f"Clic effectué aux coordonnées ({x}, {y})."
