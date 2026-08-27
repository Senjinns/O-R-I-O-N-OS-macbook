import subprocess
import asyncio
import os
import tempfile
from pathlib import Path
from core import config, journal

LOG = journal.obtenir()

class TTSProvider:
    def synthetiser(self, texte: str) -> bool:
        raise NotImplementedError

class MacOSTTS(TTSProvider):
    def __init__(self):
        self.voix = config.reglage("tts.macos.voix", "Thomas")
        self.vitesse = config.reglage("tts.macos.vitesse", 190)

    def synthetiser(self, texte: str) -> bool:
        try:
            cmd = ["say", "-v", self.voix, "-r", str(self.vitesse), texte]
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            LOG.error(f"[TTS macOS say] Erreur : {e}")
            return False

class EdgeTTSProvider(TTSProvider):
    def __init__(self):
        self.voix = config.reglage("tts.edge_tts.voix", "fr-FR-HenriNeural")
        self.vitesse = config.reglage("tts.edge_tts.vitesse", "+5%")

    async def _generer(self, texte: str, chemin_audio: str):
        import edge_tts
        communicate = edge_tts.Communicate(texte, self.voix, rate=self.vitesse)
        await communicate.save(chemin_audio)

    def synthetiser(self, texte: str) -> bool:
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                temp_path = f.name
            
            asyncio.run(self._generer(texte, temp_path))
            
            # Lecture via afplay natif macOS (faible latence et zéro dépendance C)
            subprocess.run(["afplay", temp_path], check=True)
            try:
                os.remove(temp_path)
            except Exception:
                pass
            return True
        except Exception as e:
            LOG.warning(f"[Edge-TTS] Repli sur macOS say suite à erreur : {e}")
            return MacOSTTS().synthetiser(texte)

class ElevenLabsTTS(TTSProvider):
    def __init__(self):
        self.cle = config.reglage("tts.elevenlabs.cle", "")
        self.voix_id = config.reglage("tts.elevenlabs.voix_id", "")
        self.modele = config.reglage("tts.elevenlabs.modele", "eleven_flash_v2_5")

    def synthetiser(self, texte: str) -> bool:
        if not self.cle:
            return EdgeTTSProvider().synthetiser(texte)
        try:
            from elevenlabs.client import ElevenLabs
            client = ElevenLabs(api_key=self.cle)
            audio_gen = client.text_to_speech.convert(
                voice_id=self.voix_id or "21m00Tcm4TlvDq8ikWAM",
                text=texte,
                model_id=self.modele
            )
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                temp_path = f.name
                for chunk in audio_gen:
                    f.write(chunk)
            
            subprocess.run(["afplay", temp_path], check=True)
            try:
                os.remove(temp_path)
            except Exception:
                pass
            return True
        except Exception as e:
            LOG.error(f"[ElevenLabs] Erreur : {e}, repli sur Edge-TTS")
            return EdgeTTSProvider().synthetiser(texte)

_INSTANCE_TTS = None

def tts() -> TTSProvider:
    global _INSTANCE_TTS
    if _INSTANCE_TTS is None:
        fournisseur = config.reglage("tts.fournisseur", "edge-tts").lower()
        if fournisseur == "elevenlabs" and config.reglage("tts.elevenlabs.cle", ""):
            _INSTANCE_TTS = ElevenLabsTTS()
        elif fournisseur == "macos":
            _INSTANCE_TTS = MacOSTTS()
        else:
            _INSTANCE_TTS = EdgeTTSProvider()
    return _INSTANCE_TTS
