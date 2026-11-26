#!/usr/bin/env bash
#Activa el entorno virtual, entra a frontend/ y ejecuta python app.py
set -e

RAIZ="$(cd "$(dirname "$0")" && pwd)"

source "$RAIZ/venv/bin/activate"
cd "$RAIZ/frontend"
python app.py