#!/usr/bin/env bash
set -e

RAIZ="$(cd "$(dirname "$0")" && pwd)"

source "$RAIZ/venv/bin/activate"
cd "$RAIZ/frontend"
python app.py