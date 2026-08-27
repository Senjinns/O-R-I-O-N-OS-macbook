# 🌌 O-R-I-O-N OS (macOS Apple Silicon Edition)

![Platform](https://img.shields.io/badge/platform-macOS%20(Apple%20Silicon%20M2)-black)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![LLM](https://img.shields.io/badge/LLM-Anthropic%20Claude%203.5-orange)
![STT](https://img.shields.io/badge/STT-Whisper%20(Local%20gratuit)-teal)

**ORION OS** est un assistant vocal et agentique autonome conçu sur mesure pour **macOS** (optimisé pour **MacBook Air M2 8 Go de RAM**).
Inspiré par le projet Jarvis, il intègre l'ensemble de ses fonctionnalités de A à Z, réarchitecturées pour tirer parti du Neural Engine d'Apple Silicon et du modèle de pointe **Anthropic Claude 3.5**.

---

## ✨ Fonctionnalités Majeures

- 🎙️ **100 % Vocal & Fluide** : Transcription locale gratuite et instantanée avec **Whisper**, mot d'activation ("Hey Orion") et interruption vocale (*Barge-in*).
- 🧠 **Cerveau Claude 3.5 Hybride** : Réflexes ultra-rapides et vision d'écran via `claude-3-5-haiku`, raisonnement profond avec `claude-3-5-sonnet` (avec Prompt Caching pour réduire les coûts).
- 🖥️ **Contrôle Natif macOS** : Volume sonore, luminosité, mise en veille, lancement de n'importe quelle application (`open -a`), raccourcis AppleScript.
- 👁️ **Vision de l'Écran** : « Analyse mon écran », « Explique cette erreur », « Résume cette page » (capture macOS + Claude Vision).
- 💡 **Domotique Complète** : Philips Hue, Google Home / Nest, Amazon Alexa, lumières de tournage Amaran.
- 📅 **Productivité & Bureau** : Google Agenda, Gmail (lecture, brouillons, envoi N3), Apple Notes.
- 🎵 **Média & Shazam** : Contrôle Spotify, reconnaissance de morceaux en direct via Shazamio.
- 🎬 **Créateurs & Vidéastes** : Contrôle OBS Studio (streaming, enregistrement, scènes) et pipeline de production vidéo (idées → script → tournage).
- 📱 **Pont iPhone (Siri)** : Déclenchez Orion à distance depuis vos Raccourcis iPhone et widgets lockscreen.
- 📞 **Téléphonie Twilio** : Appels vocaux automatisés et envoi de SMS.
- 🔐 **Sécurité Graduée (N1 / N2 / N3)** : Confirmation vocale obligatoire pour les opérations sensibles (envoi d'emails, extinction, appels).
- 🔌 **Serveur MCP Standard** : Expose tous les outils d'Orion à Claude Desktop, Cursor et Claude Code.
- 🧭 **Cockpit Web Futuriste** : Interface locale (`http://localhost:8765`) avec télémétrie Mac M2 en direct, suivi budgétaire et contrôle manuel.

---

## 🏗️ Architecture Technique

```mermaid
flowchart LR
    Mic([🎙️ Micro Mac]) --> VAD[Auto-Calibration RMS]
    VAD --> STT[faster-whisper / MLX<br/>Local Gratuit]
    STT --> LLM{{🧠 Anthropic Claude 3.5<br/>Haiku & Sonnet}}
    LLM <-->|Appels d'outils| TOOLS[🧰 Boîte à Outils macOS]
    LLM --> TTS{{🔊 Synthèse Vocale<br/>Edge-TTS / macOS 'say' / ElevenLabs}}
    TTS --> SPK([🔊 Haut-parleurs Mac])

    TOOLS -.-> MAC[🖥️ Volume / Luminosité / Apps / Veille]
    TOOLS -.-> HOME[💡 Hue / Google Home / Alexa / Amaran]
    TOOLS -.-> NET[📅 Google Agenda / 📧 Gmail / 💬 Discord]
    TOOLS -.-> MEDIA[🎵 Spotify / 🎬 OBS / 🔍 Shazam]
    TOOLS -.-> MCP[[🔌 Serveur MCP]]
    TOOLS -.-> TEL[📞 Appels Twilio]
```

---

## 🚀 Installation & Démarrage Rapide

### 1. Prérequis
- Un Mac avec macOS 13+ (optimisé Apple Silicon M1/M2/M3/M4).
- [Homebrew](https://brew.sh) installé.
- Une clé API Anthropic ([console.anthropic.com](https://console.anthropic.com)).

### 2. Installation Automatique
```bash
# Cloner le dépôt
git clone https://github.com/votre-compte/O-R-I-O-N-OS-macbook.git
cd O-R-I-O-N-OS-macbook

# Lancer le script d'installation macOS
chmod +x scripts/*.sh
./scripts/install_mac.sh
```

### 3. Configuration
Ouvrez `config.yaml` et renseignez votre clé Anthropic :
```yaml
anthropic:
  cle: "sk-ant-api03-..."
```

### 4. Lancement
```bash
./scripts/start.sh
```

---

## 🧭 Tableau de Bord & Pont iPhone
Une fois lancé, le serveur démarre automatiquement :
- **Cockpit Web** : `http://localhost:8765`
- **Pont iPhone Siri** : Requête POST vers `http://<IP_DU_MAC>:8765/api/commande`

---

## 📄 Licence
Ce projet est distribué sous licence MIT.
