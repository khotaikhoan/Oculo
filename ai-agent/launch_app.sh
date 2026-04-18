#!/bin/bash
# Oculo Launcher

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$SCRIPT_DIR/venv/bin/python3"
LOG="$SCRIPT_DIR/.server.log"

if [ ! -x "$PYTHON" ]; then
    osascript -e 'display alert "Oculo" message "Không tìm thấy Python venv.\nChạy setup.sh trước." as critical'
    exit 1
fi

# Nếu đã chạy rồi thì không mở thêm
if pgrep -f "oculo_app.py" > /dev/null 2>&1; then
    exit 0
fi

# Kill port cũ nếu còn
lsof -ti tcp:8080 | xargs kill -9 2>/dev/null

# Chạy app — pywebview cần được gọi từ process có GUI context
# open -a Terminal sẽ tạo đúng GUI context trên macOS
exec "$PYTHON" "$SCRIPT_DIR/oculo_app.py" > "$LOG" 2>&1
