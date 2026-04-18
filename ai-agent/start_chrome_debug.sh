#!/bin/bash
# Mở Chrome với remote debugging port 9222
# Chạy script này 1 lần trước khi dùng AI Agent browser tools
# Chrome sẽ dùng profile hiện tại của bạn (có sẵn login, cookies)

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

if [ ! -f "$CHROME" ]; then
    echo "Không tìm thấy Google Chrome. Thử Chromium..."
    CHROME="/Applications/Chromium.app/Contents/MacOS/Chromium"
fi

if [ ! -f "$CHROME" ]; then
    echo "Không tìm thấy Chrome/Chromium."
    exit 1
fi

# Kiểm tra port 9222 đã có Chrome chưa
if curl -s http://localhost:9222/json/version > /dev/null 2>&1; then
    echo "Chrome debug đã đang chạy tại port 9222."
    exit 0
fi

echo "Mở Chrome với remote debugging port 9222..."
"$CHROME" \
    --remote-debugging-port=9222 \
    --no-first-run \
    --no-default-browser-check \
    &

echo "Chrome đang khởi động... Đợi 2 giây"
sleep 2

if curl -s http://localhost:9222/json/version > /dev/null 2>&1; then
    echo "Chrome debug sẵn sàng tại http://localhost:9222"
else
    echo "Chrome đang khởi động, thử lại sau vài giây."
fi
