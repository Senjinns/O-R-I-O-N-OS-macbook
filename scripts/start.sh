#!/usr/bin/env bash
RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RACINE"
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi
python3 orion.py
