import time
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from core import config, journal

LOG = journal.obtenir()

class AudioEngine:
    def __init__(self):
        self.taux = config.reglage("audio.taux_echantillonnage", 16000)
        self.micro_index = config.reglage("audio.micro_index", None)
        self.model_whisper = None
        self.seuil_silence = 0.015
        self.seuil_parole = 0.035

    def init_whisper(self):
        if self.model_whisper is None:
            modele_nom = config.reglage("whisper.modele", "small")
            device = config.reglage("whisper.device", "cpu")
            compute_type = config.reglage("whisper.compute_type", "float32")
            LOG.info(f"Chargement du modèle Whisper '{modele_nom}' ({device})...")
            self.model_whisper = WhisperModel(
                modele_nom,
                device=device,
                compute_type=compute_type
            )
            LOG.info("Modèle Whisper chargé avec succès.")

    def calibrer_bruit_ambiant(self, duree=1.0):
        LOG.info("Auto-calibration du micro avec le bruit ambiant (1s)...")
        enregistrements = []
        
        def callback(indata, frames, time_info, status):
            enregistrements.append(np.sqrt(np.mean(indata**2)))
            
        with sd.InputStream(samplerate=self.taux, channels=1, dtype="float32",
                            device=self.micro_index, callback=callback):
            sd.sleep(int(duree * 1000))
            
        bruit_moyen = float(np.mean(enregistrements)) if enregistrements else 0.01
        self.seuil_silence = max(0.012, bruit_moyen * 1.5)
        self.seuil_parole = max(0.025, bruit_moyen * 2.8)
        LOG.info(f"Niveaux calibrés : Silence={self.seuil_silence:.4f}, Parole={self.seuil_parole:.4f}")

    def transcrire_audio(self, audio_data: np.ndarray) -> str:
        self.init_whisper()
        segments, _ = self.model_whisper.transcribe(
            audio_data,
            beam_size=5,
            language=config.reglage("whisper.langue", "fr"),
            vad_filter=True
        )
        texte = " ".join([seg.text for seg in segments]).strip()
        return texte

    def enregistrer_commande(self, duree_max=20, silence_fin=1.2) -> np.ndarray:
        frames = []
        silence_start = None
        parole_detectee = False
        t_debut = time.time()
        
        with sd.InputStream(samplerate=self.taux, channels=1, dtype="float32", device=self.micro_index) as stream:
            while (time.time() - t_debut) < duree_max:
                bloc, _ = stream.read(1024)
                rms = np.sqrt(np.mean(bloc**2))
                frames.append(bloc)
                
                if rms > self.seuil_parole:
                    parole_detectee = True
                    silence_start = None
                elif parole_detectee and rms < self.seuil_silence:
                    if silence_start is None:
                        silence_start = time.time()
                    elif (time.time() - silence_start) >= silence_fin:
                        break
                        
        if not frames:
            return np.array([], dtype=np.float32)
        return np.concatenate(frames, axis=0).flatten()
