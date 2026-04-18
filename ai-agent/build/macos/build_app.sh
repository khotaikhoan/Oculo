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
BUNDLE_ID="${OCULO_BUNDLE_ID:-com.oculo.app}"

# Bundle a .env.example if a local .env exists — users can copy it into
# ~/Library/Application Support/Oculo/.env after install.
ADD_DATA_ENV=()
if [ -f ".env" ]; then
  cp .env .env.example
  ADD_DATA_ENV=(--add-data ".env.example:.")
fi

echo "Building $APP_NAME.app (bundle id: $BUNDLE_ID)..."
"$PY" -m PyInstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "$APP_NAME" \
  --icon "$ICON" \
  --osx-bundle-identifier "$BUNDLE_ID" \
  --add-data "static:static" \
  --add-data "Oculo.icns:." \
  "${ADD_DATA_ENV[@]}" \
  --collect-submodules chromadb \
  --collect-submodules sentence_transformers \
  --collect-submodules webview \
  oculo_app.py

APP_PATH="$ROOT_DIR/dist/$APP_NAME.app"

# Strip quarantine that can linger on files copied into the bundle, and
# apply an ad-hoc code signature so Gatekeeper at least recognises the
# bundle as self-consistent (users still need to approve the first open).
if [ -d "$APP_PATH" ]; then
  /usr/bin/xattr -cr "$APP_PATH" 2>/dev/null || true
  /usr/bin/codesign --force --deep --sign - "$APP_PATH" 2>/dev/null || true
fi

echo "Done: $APP_PATH"
