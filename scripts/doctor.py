#!/usr/bin/env python3
import sys
import os
import psutil

print("=" * 60)
print("🩺 DIAGNOSTIC ORION OS (macOS Apple Silicon)")
print("=" * 60)
print(f"🐍 Python : {sys.version.split()[0]}")
mem = psutil.virtual_memory()
print(f"💾 RAM : {mem.used / 1024**3:.1f} / {mem.total / 1024**3:.1f} Go ({mem.percent}%)")
try:
    import sounddevice as sd
    devices = sd.query_devices()
    print(f"🎙️ Périphériques audio : {len(devices)} détectés")
except Exception as e:
    print(f"⚠️ Erreur audio : {e}")

if os.path.exists("config.yaml"):
    print("✅ config.yaml : Présent")
else:
    print("⚠️ config.yaml : Absent (copier config.example.yaml)")
print("=" * 60)
