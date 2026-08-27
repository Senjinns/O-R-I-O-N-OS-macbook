import sqlite3
import datetime
from pathlib import Path
from typing import List, Dict

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_DATA = RACINE / "data"
DOSSIER_DATA.mkdir(parents=True, exist_ok=True)
DB_PATH = DOSSIER_DATA / "memoire.sqlite"

def _init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS memoire (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categorie TEXT,
            cle TEXT UNIQUE,
            valeur TEXT,
            date_maj TEXT
        )
    """)
    conn.commit()
    conn.close()

_init_db()

def memoriser(cle: str, valeur: str, categorie: str = "general") -> str:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    maintenant = datetime.datetime.now().isoformat()
    cur.execute("""
        INSERT INTO memoire (categorie, cle, valeur, date_maj)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(cle) DO UPDATE SET
            valeur=excluded.valeur,
            categorie=excluded.categorie,
            date_maj=excluded.date_maj
    """, (categorie, cle.strip().lower(), valeur.strip(), maintenant))
    conn.commit()
    conn.close()
    return f"Information mémorisée : {cle} = {valeur}"

def rappeler(cle: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT valeur FROM memoire WHERE cle LIKE ?", (f"%{cle.strip().lower()}%",))
    rows = cur.fetchall()
    conn.close()
    if rows:
        return " | ".join(r[0] for r in rows)
    return "Aucun souvenir trouvé pour cette clé."

def texte_pour_systeme() -> str:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT cle, valeur FROM memoire ORDER BY categorie, cle")
    lignes = [f"- {cle} : {valeur}" for cle, valeur in cur.fetchall()]
    conn.close()
    if lignes:
        return "\n\n[MÉMOIRE LONG TERME SUR L'UTILISATEUR] :\n" + "\n".join(lignes)
    return ""
