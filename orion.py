#!/usr/bin/env python3
"""
🌌 ORION OS — Assistant Vocal Agentique pour macOS (Apple Silicon M2)
===================================================================
Pipeline : Micro -> openWakeWord / RMS -> Whisper STT -> Claude 3.5 Agent -> Edge-TTS / macOS say
"""

import time
import sys
import threading
import numpy as np
import sounddevice as sd

from core import config, journal, registre, voix, llm, tts, budget
from core.util import sans_accents

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
        self.en_parole = threading.Event()
        self.interruption = threading.Event()

    def demarrer_serveur_fond(self):
        try:
            from core import serveur
            t = threading.Thread(target=serveur.demarrer_serveur, daemon=True)
            t.start()
            LOG.info("Serveur Cockpit et Pont iPhone démarrés en tâche de fond.")
        except Exception as e:
            LOG.warning(f"Impossible de lancer le serveur web : {e}")

    def dire(self, texte: str):
        if not texte:
            return
        LOG.info(f"Orion dit : {texte}")
        self.en_parole.set()
        try:
            tts.tts().synthetiser(texte)
        finally:
            self.en_parole.clear()

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
            
        LOG.info(f"Commande utilisateur : '{requete_propre}'")
        
        # Vérification d'interruption vocale simple
        if any(w in requete_propre for w in MOTS_INTERRUPTION):
            LOG.info("Interruption détectée.")
            self.dire("Je m'arrête.")
            return

        reponse, self.historique = self.agent.repondre_et_agir(requete_propre, self.historique)
        self.dire(reponse)

    def boucle_principale(self):
        self.audio.calibrer_bruit_ambiant()
        self.demarrer_serveur_fond()
        self.dire("Système Orion opérationnel. À vos ordres.")

        LOG.info("En attente de commandes vocales (Parlez naturellement)...")
        
        duree_suite = config.reglage("assistant.duree_ecoute_suite", 8)
        dernier_echange = 0

        while self.actif:
            try:
                # Écoute continue
                audio_data = self.audio.enregistrer_commande()
                if audio_data.size > 0:
                    transcription = self.audio.transcrire_audio(audio_data)
                    if transcription and len(transcription.strip()) > 1:
                        self.executer_requete(transcription)
                        dernier_echange = time.time()
                time.sleep(0.1)
            except KeyboardInterrupt:
                LOG.info("Arrêt demandé par l'utilisateur.")
                self.dire("Arrêt du système. À bientôt.")
                break
            except Exception as e:
                LOG.error(f"Erreur dans la boucle principale : {e}")
                time.sleep(1)

def main():
    orion = OrionOS()
    orion.boucle_principale()

if __name__ == "__main__":
    main()
