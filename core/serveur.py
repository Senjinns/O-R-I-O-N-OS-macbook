import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from core import pont_iphone, panneau, config, journal

LOG = journal.obtenir()
RACINE = Path(__file__).resolve().parent.parent
DOSSIER_WEB = RACINE / "web"

app = FastAPI(title="ORION OS API & Cockpit")

app.include_router(pont_iphone.router)
app.include_router(panneau.router)

if DOSSIER_WEB.exists():
    app.mount("/", StaticFiles(directory=str(DOSSIER_WEB), html=True), name="web")

def demarrer_serveur():
    hote = config.reglage("serveur.hote", "0.0.0.0")
    port = int(config.reglage("serveur.port", 8765))
    LOG.info(f"Démarrage du serveur web ORION sur http://{hote}:{port}")
    uvicorn.run(app, host=hote, port=port, log_level="warning")
