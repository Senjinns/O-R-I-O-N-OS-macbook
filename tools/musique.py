import asyncio
from core.registre import outil
from core import journal

LOG = journal.obtenir()

@outil(
    nom="identifier_musique",
    description="Identifie la musique en cours d'écoute (style Shazam) via le micro du Mac.",
    parametres={"type": "object", "properties": {}},
    securite="N1",
    affichage="toujours"
)
def identifier_musique() -> str:
    try:
        from shazamio import Shazam
        import sounddevice as sd
        import numpy as np
        import wave
        import tempfile
        import os
        
        tmp_wav = tempfile.mktemp(suffix=".wav")
        fs = 44100
        seconds = 5
        LOG.info("Enregistrement audio pour Shazam (5s)...")
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        
        with wave.open(tmp_wav, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes(myrecording.tobytes())
            
        async def _reconnaitre():
            shazam = Shazam()
            return await shazam.recognize(tmp_wav)
            
        out = asyncio.run(_reconnaitre())
        try:
            os.remove(tmp_wav)
        except Exception:
            pass
            
        track = out.get("track")
        if track:
            titre = track.get("title", "Inconnu")
            artiste = track.get("subtitle", "Inconnu")
            return f"Morceau identifié : '{titre}' par {artiste}."
        return "Aucun morceau reconnu dans l'extrait audio."
    except Exception as e:
        return f"Erreur reconnaissance musicale : {e}"
