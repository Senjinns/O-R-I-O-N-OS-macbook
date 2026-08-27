from core.registre import outil

@outil(
    nom="cliquer_position",
    description="Clique à des coordonnées X, Y sur l'écran du Mac.",
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
    try:
        import pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.click(x, y)
        return f"Clic exécuté aux coordonnées ({x}, {y})."
    except ImportError:
        return f"Module pyautogui manquant. Clic simulé en ({x}, {y})."
    except Exception as e:
        return f"Erreur de clic : {e}"
