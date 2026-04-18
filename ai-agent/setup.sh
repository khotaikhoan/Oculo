#!/bin/bash
echo "=== Cài đặt AI Agent ==="

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài dependencies
pip install -r requirements.txt

# Cài Playwright browsers
playwright install chromium

echo ""
echo "=== Setup hoàn tất ==="
echo "Tiếp theo:"
echo "1. Điền API key vào file .env"
echo "2. Chạy: source venv/bin/activate && python main.py"
