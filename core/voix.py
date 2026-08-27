import time
import threading
from core import config, journal

LOG = journal.obtenir("voix")

HALLUCINATIONS_WHISPER = (
    "sous-titres", "sous titres", "merci d'avoir regarde", "merci d'avoir regardé",
    "abonnez-vous", "abonnez vous", "a la prochaine", "n'oubliez pas de",
    "amara.org", "transcription", "musique", "applaudissements", "silence"
)

_MICRO_MUET = threading.Event()

def basculer_micro(force=None) -> bool:
    """Coupe ou réactive le micro. force=True (muet), False (actif), None (bascule)."""
    if force is True or (force is None and not _MICRO_MUET.is_set()):
        _MICRO_MUET.set()
    else:
        _MICRO_MUET.clear()
    
    muet = _MICRO_MUET.is_set()
    LOG.info(f"Microphone : {'🔇 COUPÉ (MUTE)' if muet else '🎙️ ACTIF'}")
    try:
        import hud
        hud.etat("muet" if muet else "veille")
    except Exception:
        pass
    return muet

def est_micro_muet() -> bool:
    return _MICRO_MUET.is_set()

class AudioEngine:
    def __init__(self):
        self.micro_index = config.reglage("audio.micro_index", None)
        self.taux_traitement = 16000
        self.taux_capture = self._detecter_taux_natif()
        self.model_whisper = None
        self.seuil_silence = 0.015
        self.seuil_parole = 0.035

    def _detecter_taux_natif(self) -> int:
        try:
            import sounddevice as sd
            device_info = sd.query_devices(self.micro_index, "input")
            taux_natif = int(device_info.get("default_samplerate", 48000))
            LOG.info(f"Périphérique d'entrée audio : '{device_info.get('name')}' ({taux_natif} Hz natif)")
            return taux_natif
        except Exception:
            return 48000

    def init_whisper(self):
        if self.model_whisper is None:
            try:
                from faster_whisper import WhisperModel
                modele_nom = config.reglage("whisper.modele", "small")
                device = config.reglage("whisper.device", "cpu")
                compute_type = config.reglage("whisper.compute_type", "float32")
                LOG.info(f"Chargement Whisper '{modele_nom}' ({device})...")
                self.model_whisper = WhisperModel(modele_nom, device=device, compute_type=compute_type)
                LOG.info("Whisper opérationnel.")
            except ImportError:
                LOG.warning("faster-whisper non installé (installez les dépendances avec install_mac.sh).")

    def _reechantillonner_16k(self, audio_data):
        import numpy as np
        if self.taux_capture == self.taux_traitement or len(audio_data) == 0:
            return audio_data
        nb_echantillons_cible = int(len(audio_data) * self.taux_traitement / self.taux_capture)
        return np.interp(
            np.linspace(0, len(audio_data), nb_echantillons_cible, endpoint=False),
            np.arange(len(audio_data)),
            audio_data
        ).astype(np.float32)

    def calibrer_bruit_ambiant(self, duree=1.0):
        try:
            import numpy as np
            import sounddevice as sd
            enregistrements = []
            def callback(indata, frames, time_info, status):
                enregistrements.append(np.sqrt(np.mean(indata**2)))
            with sd.InputStream(samplerate=self.taux_capture, channels=1, dtype="float32",
                                device=self.micro_index, callback=callback):
                sd.sleep(int(duree * 1000))
            bruit_moyen = float(np.mean(enregistrements)) if enregistrements else 0.01
            self.seuil_silence = max(0.010, bruit_moyen * 1.4)
            self.seuil_parole = max(0.022, bruit_moyen * 2.5)
            LOG.info(f"Calibration : Silence={self.seuil_silence:.4f}, Parole={self.seuil_parole:.4f}")
        except Exception as e:
            LOG.warning(f"Auto-calibration audio : {e}")

    def transcrire_audio(self, audio_data) -> str:
        if len(audio_data) < (self.taux_traitement * 0.4):
            return ""
        self.init_whisper()
        if not self.model_whisper:
            return ""
        try:
            segments, _ = self.model_whisper.transcribe(
                audio_data,
                beam_size=5,
                language=config.reglage("whisper.langue", "fr"),
                vad_filter=True
            )
            texte = " ".join([seg.text for seg in segments]).strip()
            texte_min = texte.lower()
            if any(h in texte_min for h in HALLUCINATIONS_WHISPER):
                return ""
            return texte
        except Exception as e:
            LOG.error(f"Erreur transcription Whisper : {e}")
            return ""

    def enregistrer_commande(self, duree_max=20, silence_fin=1.2):
        if est_micro_muet():
            time.sleep(0.2)
            try:
                import numpy as np
                return np.array([], dtype=np.float32)
            except Exception:
                return []

        try:
            import numpy as np
            import sounddevice as sd
        except ImportError:
            return []

        frames = []
        silence_start = None
        parole_detectee = False
        t_debut = time.time()
        
        try:
            with sd.InputStream(samplerate=self.taux_capture, channels=1, dtype="float32", device=self.micro_index) as stream:
                while (time.time() - t_debut) < duree_max and not est_micro_muet():
                    bloc, _ = stream.read(int(self.taux_capture * 0.08))
                    rms = np.sqrt(np.mean(bloc**2))
                    frames.append(bloc)
                    
                    try:
                        import hud
                        hud.niveau(min(1.0, float(rms / 0.15)))
                    except Exception:
                        pass
                        
                    if rms > self.seuil_parole:
                        parole_detectee = True
                        silence_start = None
                    elif parole_detectee and rms < self.seuil_silence:
                        if silence_start is None:
                            silence_start = time.time()
                        elif (time.time() - silence_start) >= silence_fin:
                            break
        except Exception as e:
            LOG.error(f"Erreur capture audio : {e}")
            return np.array([], dtype=np.float32)
            
        if not frames or not parole_detectee:
            return np.array([], dtype=np.float32)
            
        audio_brut = np.concatenate(frames, axis=0).flatten()
        return self._reechantillonner_16k(audio_brut)
