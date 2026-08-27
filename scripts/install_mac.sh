#!/usr/bin/env bash
set -e
echo "🌌 ========================================================"
echo "   Installation de ORION OS pour macOS (Apple Silicon M2)  "
echo "=========================================================="

if ! command -v brew &> /dev/null; then
    echo "⚠️ Homebrew n'est pas installé. Installez-le depuis https://brew.sh"
    exit 1
fi

echo "📦 Installation de PortAudio et FFmpeg..."
brew install portaudio ffmpeg

echo "🐍 Création de l'environnement virtuel Python..."
python3 -m venv .venv
source .venv/bin/activate

echo "⬇️ Installation des dépendances Python..."
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f config.yaml ]; then
    cp config.example.yaml config.yaml
    echo "✅ Fichier config.yaml créé. Pensez à renseigner votre clé Anthropic !"
fi

echo "🎉 Installation terminée ! Lancez './scripts/start.sh' pour démarrer Orion."
