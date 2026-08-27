#!/usr/bin/env python3
"""
🌌 ORION OS — Assistant Vocal Agentique pour macOS (Apple Silicon M2)
"""

import time
import sys
import threading
import numpy as np

from core import config, journal, registre, voix, llm, tts, budget
from core.util import sans_accents
import hud

LOG = journal.obtenir("orion")

MOTS_INTERRUPTION = {"attends", "stop", "arrete", "pause", "tais-toi", "tais toi", "minute", "chut"}
RESIDUS_WAKEWORD = {"orion", "hey orion", "jarvis", "hey jarvis", "dis orion", "ok orion"}

class OrionOS:
    def __init__(self):
        LOG.info("Initialisation de ORION OS pour macOS (Apple Silicon M2)...")
        config.charger_config()
        registre.decouvrir_outils()
        LOG.info(f"Outils chargés : {len(registre._OUTILS)} outils enregistrés.")
        
        self.audio = voix.AudioEngine()
        self.agent = llm.ClaudeAgent()
        self.historique = []
        self.actif = True

    def demarrer_serveurs_fond(self):
        try:
            # 1. Démarrage du HUD Arc Reactor sur 8770
            hud.demarrer()
            
            # 2. Démarrage du Cockpit & Pont iPhone sur 8765
            from core import serveur
            t = threading.Thread(target=serveur.demarrer_serveur, daemon=True)
            t.start()
            LOG.info("Services de fond démarrés : Cockpit (8765) & HUD (8770).")
        except Exception as e:
            LOG.warning(f"Erreur démarrage services : {e}")

    def dire(self, texte: str):
        if not texte:
            return
        LOG.info(f"Orion dit : {texte}")
        hud.etat(hud.PAROLE)
        hud.dire_orion(texte)
        try:
            tts.tts().synthetiser(texte)
        finally:
            hud.etat(hud.VEILLE)

    def nettoyer_transcription(self, texte: str) -> str:
        t = sans_accents(texte)
        for res in RESIDUS_WAKEWORD:
            if t.startswith(res):
                t = t[len(res):].strip()
        return t

    def executer_requete(self, requete: str):
        requete_propre = self.nettoyer_transcription(requete)
        if not requete_propre or len(requete_propre) < 2:
            return
            
        LOG.info(f"Commande entendue : '{requete_propre}'")
        hud.dire_vous(requete_propre)
        hud.etat(hud.REFLEXION)
        
        if any(w in requete_propre for w in MOTS_INTERRUPTION):
            self.dire("Je m'arrête.")
            return

        reponse, self.historique = self.agent.repondre_et_agir(requete_propre, self.historique)
        self.dire(reponse)

    def boucle_principale(self):
        self.audio.calibrer_bruit_ambiant()
        self.demarrer_serveurs_fond()
        self.dire("Système Orion opérationnel. À vos ordres.")

        LOG.info("En attente de commandes vocales...")
        hud.etat(hud.VEILLE)

        while self.actif:
            try:
                hud.etat(hud.ECOUTE)
                audio_data = self.audio.enregistrer_commande()
                if audio_data.size > 0:
                    hud.etat(hud.REFLEXION)
                    transcription = self.audio.transcrire_audio(audio_data)
                    if transcription and len(transcription.strip()) > 1:
                        self.executer_requete(transcription)
                else:
                    hud.etat(hud.VEILLE)
                time.sleep(0.1)
            except KeyboardInterrupt:
                LOG.info("Arrêt demandé par l'utilisateur.")
                self.dire("Arrêt du système. À bientôt.")
                break
            except Exception as e:
                LOG.error(f"Erreur boucle principale : {e}")
                time.sleep(1)

def main():
    orion = OrionOS()
    orion.boucle_principale()

if __name__ == "__main__":
    main()
