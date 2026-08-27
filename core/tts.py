import subprocess
import asyncio
import os
import tempfile
import threading
from pathlib import Path
from core import config, journal

LOG = journal.obtenir("tts")

_PROCESSUS_AUDIO = None
_VERROU_AUDIO = threading.Lock()

def couper_parole():
    """Interrompt immédiatement la synthèse vocale en cours."""
    global _PROCESSUS_AUDIO
    with _VERROU_AUDIO:
        if _PROCESSUS_AUDIO is not None and _PROCESSUS_AUDIO.poll() is None:
            try:
                _PROCESSUS_AUDIO.terminate()
                LOG.info("Synthèse vocale interrompue par l'utilisateur.")
            except Exception:
                pass
            _PROCESSUS_AUDIO = None

def _jouer_processus(cmd: list) -> bool:
    global _PROCESSUS_AUDIO
    couper_parole()
    try:
        with _VERROU_AUDIO:
            _PROCESSUS_AUDIO = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        _PROCESSUS_AUDIO.wait()
        return True
    except Exception as e:
        LOG.error(f"Erreur lecture audio : {e}")
        return False
    finally:
        with _VERROU_AUDIO:
            _PROCESSUS_AUDIO = None

class TTSProvider:
    def synthetiser(self, texte: str) -> bool:
        raise NotImplementedError

class MacOSTTS(TTSProvider):
    def __init__(self):
        self.voix = config.reglage("tts.macos.voix", "Thomas")
        self.vitesse = config.reglage("tts.macos.vitesse", 190)

    def synthetiser(self, texte: str) -> bool:
        cmd = ["say", "-v", self.voix, "-r", str(self.vitesse), texte]
        return _jouer_processus(cmd)

class EdgeTTSProvider(TTSProvider):
    def __init__(self):
        self.voix = config.reglage("tts.edge_tts.voix", "fr-FR-HenriNeural")
        self.vitesse = config.reglage("tts.edge_tts.vitesse", "+5%")

    async def _generer(self, texte: str, chemin_audio: str):
        import edge_tts
        communicate = edge_tts.Communicate(texte, self.voix, rate=self.vitesse)
        await communicate.save(chemin_audio)

    def synthetiser(self, texte: str) -> bool:
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_path = temp_file.name
        temp_file.close()
        
        try:
            asyncio.run(self._generer(texte, temp_path))
            return _jouer_processus(["afplay", temp_path])
        except Exception as e:
            LOG.warning(f"Edge-TTS indisponible, repli sur macOS say : {e}")
            return MacOSTTS().synthetiser(texte)
        finally:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass

class ElevenLabsTTS(TTSProvider):
    def __init__(self):
        self.cle = config.reglage("tts.elevenlabs.cle", "")
        self.voix_id = config.reglage("tts.elevenlabs.voix_id", "")
        self.modele = config.reglage("tts.elevenlabs.modele", "eleven_flash_v2_5")

    def synthetiser(self, texte: str) -> bool:
        if not self.cle:
            return EdgeTTSProvider().synthetiser(texte)
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_path = temp_file.name
        temp_file.close()
        try:
            from elevenlabs.client import ElevenLabs
            client = ElevenLabs(api_key=self.cle)
            audio_gen = client.text_to_speech.convert(
                voice_id=self.voix_id or "21m00Tcm4TlvDq8ikWAM",
                text=texte,
                model_id=self.modele
            )
            with open(temp_path, "wb") as f:
                for chunk in audio_gen:
                    f.write(chunk)
            return _jouer_processus(["afplay", temp_path])
        except Exception as e:
            LOG.error(f"ElevenLabs erreur : {e}, repli sur Edge-TTS")
            return EdgeTTSProvider().synthetiser(texte)
        finally:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass

_INSTANCE_TTS = None

def tts() -> TTSProvider:
    global _INSTANCE_TTS
    if _INSTANCE_TTS is None:
        f = config.reglage("tts.fournisseur", "edge-tts").lower()
        if f == "elevenlabs" and config.reglage("tts.elevenlabs.cle", ""):
            _INSTANCE_TTS = ElevenLabsTTS()
        elif f == "macos":
            _INSTANCE_TTS = MacOSTTS()
        else:
            _INSTANCE_TTS = EdgeTTSProvider()
    return _INSTANCE_TTS
