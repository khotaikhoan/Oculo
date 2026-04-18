#!/bin/bash
# Tạo file Oculo.app để kéo vào Dock

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_NAME="Oculo"
APP_PATH="$HOME/Applications/$APP_NAME.app"

echo "Tạo $APP_NAME.app tại $APP_PATH..."

# Tạo AppleScript app bằng osacompile
APPLESCRIPT=$(cat <<APPLEEOF
on run
    set launchScript to "$SCRIPT_DIR/launch_app.sh"
    
    -- Mở Terminal chạy launcher (Terminal sẽ tắt server khi đóng)
    tell application "Terminal"
        activate
        set newTab to do script "bash " & quoted form of launchScript
        set custom title of newTab to "$APP_NAME"
    end tell
end run
APPLEEOF
)

# Compile thành .app
echo "$APPLESCRIPT" | osacompile -o "$APP_PATH"

if [ $? -eq 0 ]; then
    echo "Tạo app thành công: $APP_PATH"

    # Gán icon Oculo
    ICNS_PATH="$SCRIPT_DIR/Oculo.icns"
    if [ ! -f "$ICNS_PATH" ]; then
        echo "Tạo icon..."
        PYTHON=$(command -v python3 || echo "$SCRIPT_DIR/venv/bin/python3")
        "$PYTHON" "$SCRIPT_DIR/make_icon.py"
    fi
    if [ -f "$ICNS_PATH" ]; then
        cp "$ICNS_PATH" "$APP_PATH/Contents/Resources/applet.icns"
        touch "$APP_PATH"
        killall Dock 2>/dev/null || true
        echo "Icon đã gán."
    fi

    echo ""
    echo "Bước tiếp theo:"
    echo "  1. Mở Finder → Applications"
    echo "  2. Kéo '$APP_NAME' vào Dock"
    echo "  3. Click vào icon để dùng"
    echo ""
    echo "Khi muốn tắt server: đóng cửa sổ Terminal '$APP_NAME'"

    # Mở thư mục chứa app
    open "$HOME/Applications"
else
    echo "Lỗi khi tạo app!"
    exit 1
fi
