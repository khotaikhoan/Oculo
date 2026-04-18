#!/bin/bash
set -euo pipefail

# Build Oculo.app via PyInstaller (macOS).
# Output: dist/Oculo.app

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$ROOT_DIR"

PY="./venv/bin/python"
if [ ! -x "$PY" ]; then
  echo "Missing venv python at $PY. Run setup.sh first."
  exit 1
fi

echo "Installing build deps (pyinstaller)..."
"$PY" -m pip install -q --upgrade pyinstaller

APP_NAME="Oculo"
ICON="Oculo.icns"

echo "Building $APP_NAME.app..."
"$PY" -m PyInstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "$APP_NAME" \
  --icon "$ICON" \
  --add-data "static:static" \
  --add-data "Oculo.icns:." \
  oculo_app.py

echo "Done: $ROOT_DIR/dist/$APP_NAME.app"

#!/bin/bash
set -euo pipefail

# Build Oculo.app via PyInstaller (macOS).
# Output: dist/Oculo.app

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$ROOT_DIR"

PY="./venv/bin/python"
if [ ! -x "$PY" ]; then
  echo "Missing venv python at $PY. Run setup.sh first."
  exit 1
fi

echo "Installing build deps (pyinstaller)..."
"$PY" -m pip install -q --upgrade pyinstaller

APP_NAME="Oculo"
ICON="Oculo.icns"

echo "Building $APP_NAME.app..."
"$PY" -m PyInstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "$APP_NAME" \
  --icon "$ICON" \
  --add-data "static:static" \
  --add-data "Oculo.icns:." \
  oculo_app.py

echo "Done: $ROOT_DIR/dist/$APP_NAME.app"

