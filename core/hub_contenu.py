import json
from pathlib import Path
import datetime

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_DATA = RACINE / "data"
DOSSIER_DATA.mkdir(parents=True, exist_ok=True)
FICHIER_PIPELINE = DOSSIER_DATA / "pipeline_contenu.json"

def _charger_pipeline():
    if FICHIER_PIPELINE.exists():
        try:
            with open(FICHIER_PIPELINE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"videos": []}

def _sauvegarder_pipeline(data):
    with open(FICHIER_PIPELINE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def ajouter_idee_video(titre: str, notes: str = "") -> str:
    data = _charger_pipeline()
    item = {
        "id": len(data["videos"]) + 1,
        "titre": titre,
        "notes": notes,
        "etape": "idee", # idee -> script -> tournage -> montage -> publie
        "date_creation": datetime.date.today().isoformat()
    }
    data["videos"].append(item)
    _sauvegarder_pipeline(data)
    return f"Idée ajoutée : '{titre}' (ID: {item['id']})"

def lister_pipeline() -> str:
    data = _charger_pipeline()
    if not data["videos"]:
        return "Aucun contenu dans le pipeline actuellement."
    lignes = [f"#{v['id']} [{v['etape'].upper()}] {v['titre']}" for v in data["videos"]]
    return "\n".join(lignes)
