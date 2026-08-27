import json
import queue
import threading
import time
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from core import journal, voix

LOG = journal.obtenir("hud")
PORT_HUD = 8770
FICHIER_HTML = Path(__file__).resolve().parent / "web" / "hud.html"

VEILLE = "veille"
ECOUTE = "ecoute"
REFLEXION = "reflexion"
PAROLE = "parole"
MUET = "muet"

_CLIENTS = set()
_VERROU = threading.Lock()
_HISTORIQUE = deque(maxlen=30)
_SERVEUR = None

def _diffuser(evenement):
    donnees = json.dumps(evenement, ensure_ascii=False)
    with _VERROU:
        morts = []
        for q in _CLIENTS:
            try:
                q.put_nowait(donnees)
            except queue.Full:
                morts.append(q)
        for q in morts:
            _CLIENTS.discard(q)

class GestionnaireHUD(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_POST(self):
        if self.path == "/mute":
            est_muet = voix.basculer_micro()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"muet": est_muet}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == "/flux":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            q = queue.Queue(maxsize=100)
            with _VERROU:
                _CLIENTS.add(q)
                for item in _HISTORIQUE:
                    q.put_nowait(json.dumps(item, ensure_ascii=False))
                etat_initial = MUET if voix.est_micro_muet() else VEILLE
                q.put_nowait(json.dumps({"t": "etat", "v": etat_initial}, ensure_ascii=False))
                q.put_nowait(json.dumps({"t": "muet", "v": voix.est_micro_muet()}, ensure_ascii=False))

            try:
                while True:
                    donnees = q.get()
                    self.wfile.write(f"data: {donnees}\n\n".encode("utf-8"))
                    self.wfile.flush()
            except Exception:
                with _VERROU:
                    _CLIENTS.discard(q)
        else:
            if FICHIER_HTML.exists():
                contenu = FICHIER_HTML.read_bytes()
            else:
                contenu = b"<h1>HUD ORION non trouve</h1>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(contenu)))
            self.end_headers()
            self.wfile.write(contenu)

def demarrer(port=PORT_HUD):
    global _SERVEUR
    if _SERVEUR is not None:
        return
    try:
        _SERVEUR = ThreadingHTTPServer(("127.0.0.1", port), GestionnaireHUD)
        t = threading.Thread(target=_SERVEUR.serve_forever, daemon=True)
        t.start()
        LOG.info(f"HUD Réacteur Arc actif sur http://127.0.0.1:{port}")
    except Exception as e:
        LOG.warning(f"Port HUD {port} indisponible : {e}")

def etat(nom_etat: str):
    _diffuser({"t": "etat", "v": nom_etat})

def niveau(val: float):
    _diffuser({"t": "niveau", "v": round(val, 3)})

def dire_vous(texte: str):
    ev = {"t": "vous", "v": texte}
    _HISTORIQUE.append(ev)
    _diffuser(ev)

def dire_orion(texte: str):
    ev = {"t": "orion", "v": texte}
    _HISTORIQUE.append(ev)
    _diffuser(ev)

def outil(nom_outil: str, desc: str = ""):
    ev = {"t": "outil", "nom": nom_outil, "desc": desc}
    _HISTORIQUE.append(ev)
    _diffuser(ev)
