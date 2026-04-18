#!/bin/bash
set -euo pipefail

# Create a drag-install DMG for Oculo.app using hdiutil (macOS).
# Requires: dist/Oculo.app already built.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

APP_NAME="Oculo"
APP_PATH="$ROOT_DIR/dist/$APP_NAME.app"

if [ ! -d "$APP_PATH" ]; then
  echo "Missing $APP_PATH. Run build_app.sh first."
  exit 1
fi

STAGING="$ROOT_DIR/dist/dmg-staging"
DMG_OUT="$ROOT_DIR/dist/$APP_NAME.dmg"

rm -rf "$STAGING"
mkdir -p "$STAGING"

cp -R "$APP_PATH" "$STAGING/"

# Clear any quarantine attrs inherited during copy — the DMG recipient will
# still pick up their own quarantine on download, but we avoid baking one in.
/usr/bin/xattr -cr "$STAGING/$APP_NAME.app" 2>/dev/null || true

ln -s /Applications "$STAGING/Applications"

rm -f "$DMG_OUT"

echo "Creating DMG at $DMG_OUT..."
hdiutil create \
  -volname "$APP_NAME" \
  -srcfolder "$STAGING" \
  -ov \
  -format UDZO \
  "$DMG_OUT" >/dev/null

echo "Done: $DMG_OUT"
