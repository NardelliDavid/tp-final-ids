#!/usr/bin/env bash
set -e

DIR="${1:-.}"
cd "$DIR"

if [ ! -f requirements.txt ]; then
    echo "No se encontró requirements.txt en $(pwd)"
    exit 1
fi

if [ ! -d venv ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

echo "Instalando dependencias..."
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt

echo "Listo. Para activarlo: source venv/bin/activate"