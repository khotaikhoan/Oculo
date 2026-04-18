# Oculo

**Oculo** là AI agent chạy local trên **macOS** — giao diện web chat streaming, điều khiển shell và ứng dụng, tự động hóa trình duyệt qua Playwright, bộ nhớ dài hạn với ChromaDB, và hệ thống error recovery thông minh.

Toàn bộ ứng dụng nằm trong **`ai-agent/`** (Flask backend + static frontend, không cần build).

---

## Mục lục

1. [Tính năng](#tính-năng)
2. [Kiến trúc](#kiến-trúc)
3. [Cấu trúc thư mục](#cấu-trúc-thư-mục)
4. [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
5. [Cài đặt](#cài-đặt)
6. [Biến môi trường](#biến-môi-trường)
7. [Chạy server](#chạy-server)
8. [API Reference](#api-reference)
9. [Công cụ (Tools)](#công-cụ-tools)
10. [Error Recovery](#error-recovery)
11. [Bộ nhớ dài hạn](#bộ-nhớ-dài-hạn)
12. [Giao diện](#giao-diện)
13. [Phát triển](#phát-triển)
14. [Bảo mật](#bảo-mật)

---

## Tính năng

### Agent & Tools
- Gọi công cụ thật: terminal, AppleScript, đọc/ghi file, thông báo macOS, lịch trình
- Tự động hóa Chrome qua Playwright — navigate, click, fill, evaluate JS, multi-tab, vision click
- Screenshot + phân tích màn hình bằng vision model
- Trích xuất dữ liệu có cấu trúc (`extract_data`)

### Streaming & UX
- SSE real-time — text token, tool call, tool result, retry/fallback events
- Hủy stream theo `stream_id`
- Đa hội thoại với sidebar, lưu lịch sử local
- Giao diện sáng/tối, PWA (cài được trên desktop/mobile)
- Live browser view — hiện screenshot realtime khi agent điều khiển Chrome
- Automation Panel — kỹ năng, checkpoint, pipeline, giám sát, xuất dữ liệu
- @mention files — gõ `@` để đính kèm file từ Desktop/Downloads
- ↑ Arrow để chỉnh sửa message cuối
- Proactive suggestions — gợi ý hành động contextual sau mỗi turn
- Tool result diffing — hiện diff before/after khi agent ghi file

### Model & Tối ưu
- Hỗ trợ Anthropic API và OpenAI-compatible endpoint (Gemini, proxy...)
- Smart model routing — query đơn giản → Haiku (rẻ hơn ~10x), phức tạp → Sonnet
- Prompt caching với `cache_control: ephemeral` — tiết kiệm ~90% input tokens
- Nén lịch sử hội thoại khi context dài (threshold 14 messages)
- Trim tool results trong history — tiết kiệm ~60% context
- Resize ảnh đính kèm tự động (max 1024px)
- Cache kết quả tool (shell commands idempotent)
- Chạy song song nhiều tool độc lập
- Mask dữ liệu nhạy cảm trước khi gửi về client

### Error Recovery
- Phân loại lỗi 3 tầng: Transient → Recoverable → Fatal
- Retry thông minh với exponential backoff + full jitter
- Fallback registry — khi tool fail, tự động thử cách khác
- Progress checkpoint — task dài fail có thể resume từ bước đang dở

### Bộ nhớ & Tự động hóa
- ChromaDB persistent + embedding `all-MiniLM-L6-v2` (local, không gửi ra ngoài)
- Gom/củng cố bộ nhớ cũ tự động mỗi 30 phút
- Pipeline đa-agent: Research → Execute → Review
- Proactive monitor: theo dõi file, calendar, system metrics

---

## Kiến trúc

```
User (browser)
    │  HTTP/SSE
    ▼
Flask server (server.py)
    ├── stream_agent()              ← vòng lặp agentic chính
    │       ├── Anthropic Messages API  (hoặc OpenAI-compat)
    │       ├── run_tool_resilient()    ← error recovery wrapper
    │       │       ├── run_with_retry()        (retry_engine.py)
    │       │       ├── execute_fallback()      (fallback_registry.py)
    │       │       └── record_step()           (task_progress.py)
    │       └── run_tool()              ← dispatcher gốc
    │               ├── tools/desktop.py    (shell, AppleScript, file)
    │               ├── tools/browser.py   (Playwright)
    │               └── tools/vision_dom.py (Vision + DOM hybrid)
    ├── memory/store.py             ← ChromaDB
    ├── utils/                      ← các module tiện ích
    └── agents/orchestrator.py      ← pipeline đa-agent
```

**SSE events từ server về client:**

| Event | Ý nghĩa |
|---|---|
| `text` | Token văn bản từ model |
| `tool_call` | Agent gọi tool (kèm `before_content` cho write_file) |
| `tool_stream` | Output streaming của `run_shell` |
| `tool_result` | Kết quả tool (có thể masked) |
| `browser_frame` | Screenshot live từ browser (kèm URL) |
| `screenshot_captured` | Ảnh chụp màn hình inline |
| `retry_attempt` | Đang retry với delay |
| `fallback_attempt` | Chuyển sang fallback strategy |
| `model_selected` | Model được chọn cho turn này |
| `decomposition` | Danh sách subtask |
| `history_compressed` | Lịch sử đã được nén |
| `token_usage` | Thống kê token |
| `done` | Kết thúc turn |
| `interrupted` | Stream bị hủy |

---

## Cấu trúc thư mục

```
Oculo/
├── README.md
└── ai-agent/
    ├── server.py               # Flask app, vòng lặp agentic, tất cả routes
    ├── config.py               # Cấu hình tập trung
    ├── requirements.txt        # Python dependencies
    ├── .env                    # API keys và config (KHÔNG commit)
    ├── setup.sh                # Script cài đặt nhanh
    ├── start_chrome_debug.sh   # Khởi Chrome với remote debugging
    │
    ├── static/                 # Frontend (SPA, không cần build)
    │   ├── index.html          # Entry point
    │   ├── app.js              # Toàn bộ UI logic (~6300 dòng)
    │   ├── style.css           # Styles (~3000 dòng)
    │   ├── tokens.css          # Design tokens (màu, spacing, z-index...)
    │   ├── manifest.json       # PWA manifest
    │   └── sw.js               # Service worker
    │
    ├── tools/
    │   ├── browser.py          # Playwright: navigate, click, fill, tabs, CDP
    │   ├── desktop.py          # shell, AppleScript, screenshot, file ops
    │   ├── human_behavior.py   # Mouse/keyboard giả lập hành vi người thật
    │   ├── vision_dom.py       # Vision + DOM hybrid (analyze, click, type)
    │   └── page_classifier.py  # Phân loại trạng thái trang (captcha, login...)
    │
    ├── memory/
    │   ├── store.py            # ChromaDB wrapper: save, search, consolidate
    │   └── chroma_db/          # Dữ liệu ChromaDB (persistent)
    │
    ├── utils/
    │   ├── error_classifier.py # Phân loại lỗi 3 tầng
    │   ├── retry_engine.py     # Exponential backoff + full jitter
    │   ├── fallback_registry.py# Fallback strategies cho từng tool
    │   ├── task_progress.py    # SQLite checkpoint — resume task dài
    │   ├── model_router.py     # Định tuyến model theo độ phức tạp
    │   ├── model_display.py    # Metadata hiển thị model
    │   ├── prompt_compressor.py# Nén lịch sử hội thoại
    │   ├── context_injector.py # Inject context môi trường (có điều kiện)
    │   ├── cost_optimizer.py   # Prompt caching, tool filtering, memory threshold
    │   ├── tool_cache.py       # Cache kết quả tool
    │   ├── tool_parallel.py    # Chạy song song tool calls
    │   ├── tool_summarizer.py  # Tóm tắt output tool dài
    │   ├── self_corrector.py   # Verify sau write_file, browser_navigate
    │   ├── task_decomposer.py  # Phân rã task thành subtasks
    │   ├── checkpoint.py       # Checkpoint messages history
    │   ├── api_key_manager.py  # Xoay vòng API keys
    │   ├── data_masker.py      # Mask PII/sensitive data
    │   ├── openai_bridge.py    # Convert Anthropic ↔ OpenAI format
    │   ├── openai_compat.py    # OpenAI-compatible client
    │   └── preference_tracker.py # Học preference người dùng
    │
    ├── agents/
    │   └── orchestrator.py     # Pipeline: Research → Execute → Review
    │
    ├── proactive/
    │   └── monitor.py          # File/calendar/system watcher
    │
    ├── data/
    │   └── task_progress.db    # SQLite — task progress (tự tạo khi chạy)
    │
    └── tests/
        ├── test_e2e_browser_human.py
        ├── test_e2e_vision_dom.py
        ├── test_human_behavior.py
        └── test_page_classifier.py
```

---

## Yêu cầu hệ thống

- **macOS** — một số tính năng phụ thuộc AppleScript, `pyautogui`, screenshot macOS
- **Python 3.10+** (khuyến nghị 3.11 hoặc 3.12)
- **Chrome/Chromium** — cho browser automation
- **RAM**: tối thiểu 4GB (ChromaDB + embedding model ~500MB–1GB)
- **Mạng**: cần kết nối để gọi API; lần đầu tải embedding model từ HuggingFace (~90MB)

---

## Cài đặt

**1. Clone và tạo môi trường:**

```bash
git clone <repo-url>
cd Oculo/ai-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Cài Playwright browsers:**

```bash
venv/bin/playwright install chromium
```

**3. Tạo file `.env`:**

```env
# Bắt buộc
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_BASE_URL=https://llm.chiasegpu.vn   # hoặc bỏ để dùng Anthropic trực tiếp

# Model
MODEL=claude-sonnet-4.6
HAIKU_MODEL=claude-haiku-4.5
AGENT_SMART_MODEL_ROUTING=true

# OpenAI-compat (tùy chọn — Gemini, GLM...)
GEMINI_API_KEY=sk-...
GEMINI_BASE_URL=https://llm.chiasegpu.vn/v1
GEMINI_EXTRA_MODELS=gemini-3-flash,gemini-3.1-pro-preview
```

**4. Chạy setup script (tùy chọn):**

```bash
bash setup.sh
```

---

## Biến môi trường

Đặt trong `ai-agent/.env`. Chỉ `ANTHROPIC_API_KEY` là bắt buộc.

### Anthropic API

| Biến | Mô tả | Mặc định |
|---|---|---|
| `ANTHROPIC_API_KEY` | API key chính | **bắt buộc** |
| `ANTHROPIC_API_KEY_2` ... `_5` | Key phụ để xoay vòng | tùy chọn |
| `ANTHROPIC_BASE_URL` | Base URL tùy chỉnh (proxy) | Anthropic default |
| `MODEL` | Model chính | `claude-sonnet-4.6` |
| `HAIKU_MODEL` | Model nhẹ cho task đơn giản | `claude-haiku-4.5` |
| `MODELS_EXCLUDE` | Model ẩn khỏi UI (phân cách bởi `,`) | trống |

### OpenAI-compatible (Gemini, proxy...)

| Biến | Mô tả |
|---|---|
| `GEMINI_API_KEY` | API key |
| `GEMINI_BASE_URL` | Base URL endpoint `/v1` |
| `GEMINI_MODEL` | Model ID mặc định |
| `GEMINI_EXTRA_MODELS` | Thêm model vào danh sách (phân cách bởi `,`) |

### Hành vi agent

| Biến | Mô tả | Mặc định |
|---|---|---|
| `AGENT_SMART_MODEL_ROUTING` | Bật định tuyến model thông minh | `false` |
| `AGENT_SKIP_DECOMPOSE` | Tắt phân rã task | `false` |
| `AGENT_TOOL_MAX_TOKENS` | Max tokens khi có tool | `8192` |
| `AGENT_CHAT_MAX_TOKENS` | Max tokens chat thuần | `4096` |
| `SCREENSHOT_COOLDOWN_SEC` | Giãn cách tối thiểu giữa screenshot | `5` |
| `TOOL_RESULT_TRIM_CHARS` | Trim tool results trong history | `600` |
| `IMAGE_MAX_PX` | Resize ảnh đính kèm (px) | `1024` |

### Chrome & Browser

| Biến | Mô tả | Mặc định |
|---|---|---|
| `CHROME_SHARE_SYSTEM_PROFILE` | Dùng chung profile Chrome hàng ngày | `0` |
| `CHROME_PROFILE_DIRECTORY` | Tên profile (chỉ khi SHARE=1) | `Default` |
| `CHROME_USER_DATA_DIR` | Đường dẫn User Data tùy chỉnh | tự động |
| `CHROME_CDP_URL` | CDP endpoint | `http://localhost:9222` |
| `BROWSER_HEADLESS` | Chạy headless | `false` |

### Server

| Biến | Mô tả | Mặc định |
|---|---|---|
| `RATE_LIMIT_MAX` | Số request tối đa mỗi window | `60` |
| `RATE_LIMIT_WINDOW` | Window tính rate limit (giây) | `60` |

---

## Chạy server

```bash
cd ai-agent
source venv/bin/activate
python server.py
```

Server khởi động tại **`http://localhost:8080`** (lắng nghe `0.0.0.0:8080` — truy cập được từ LAN).

**Kiểm tra:**

```bash
curl http://localhost:8080/health
```

---

## Đóng gói macOS (.app + .dmg) và Update nhanh

### Build `.app`

```bash
cd ai-agent
bash build/macos/build_app.sh
```

Output: `ai-agent/dist/Oculo.app`

### Tạo `.dmg` (kéo thả vào Applications)

```bash
cd ai-agent
bash build/macos/make_dmg.sh
```

Output: `ai-agent/dist/Oculo.dmg`

### Sau khi cài từ `.dmg` — app không mở?

Bản build không có chữ ký Apple Developer, nên macOS Gatekeeper có thể chặn:

1. **Cho phép lần đầu:** Chuột phải `Oculo.app` trong `Applications` → **Open** → **Open** lại trong hộp thoại cảnh báo. Sau đó mở bằng double-click bình thường.
2. **Nếu vẫn bị chặn** ("app is damaged"): mở Terminal và gỡ quarantine:
   ```bash
   xattr -dr com.apple.quarantine /Applications/Oculo.app
   ```
3. **Dữ liệu & cấu hình** ghi vào thư mục user (không ghi vào bundle read-only):
   - `~/Library/Application Support/Oculo/chroma_db/` — bộ nhớ dài hạn
   - `~/Library/Application Support/Oculo/data/task_progress.db` — checkpoint task
   - `~/Library/Application Support/Oculo/browser_data/session.json` — session trình duyệt
   - `~/Library/Application Support/Oculo/launch.log` — log khởi động (mở file này nếu app im lặng crash)
4. **Đặt API key** sau khi cài: tạo file `~/Library/Application Support/Oculo/.env`:
   ```env
   ANTHROPIC_API_KEY=sk-ant-...
   ANTHROPIC_BASE_URL=https://llm.chiasegpu.vn
   MODEL=claude-sonnet-4.6
   ```
   Nếu chưa có key, app vẫn mở được và hiện trang chat; chỉ gọi model mới báo lỗi.

### Update nhanh (in-app notification)

App có thể hiện thông báo “có bản mới” và mở trang tải.

- Set env trên máy người dùng (ví dụ trong `.env`):
  - `OCULO_DOWNLOADS_URL`: trang tải bản mới (GitHub Releases / website)
  - `OCULO_UPDATE_FEED_URL` (tùy chọn): URL JSON trả về `{ "version": "x.y.z" }`

Ví dụ:

```env
OCULO_DOWNLOADS_URL=https://github.com/<owner>/<repo>/releases/latest
OCULO_UPDATE_FEED_URL=https://raw.githubusercontent.com/<owner>/<repo>/main/oculo-update.json
```


**Lỗi thường gặp:**

| Lỗi | Nguyên nhân | Cách xử lý |
|---|---|---|
| `Address already in use` | Cổng 8080 bị chiếm | `lsof -ti:8080 \| xargs kill -9` |
| `zsh: command not found: python` | Chưa activate venv | `source venv/bin/activate` |
| Chậm lần đầu | Tải embedding model (~90MB) | Đợi, hoặc set `HF_TOKEN` |
| `playwright._impl._errors.Error` | Chưa cài browser | `playwright install chromium` |
| Chrome tự tắt ngay | `SingletonLock` còn sót | Server tự xóa lock khi khởi động |
| CDP port 9222 không kết nối được | Chrome không có remote debugging | Đặt `CHROME_SHARE_SYSTEM_PROFILE=0` |

---

## API Reference

### Chat

**`POST /chat`** — Gửi message, nhận SSE stream.

```json
{
  "message": "Liệt kê file trong Desktop",
  "history": [],
  "model": "claude-sonnet-4.6",
  "temperature": 1.0,
  "stream_id": "uuid-v4",
  "system_prompt": "",
  "files": []
}
```

`files`: array `{name, type, data}` với `data` là base64. Hỗ trợ ảnh (tự resize) và file text.

**`POST /abort/<stream_id>`** — Hủy stream đang chạy.

### Bộ nhớ

| Endpoint | Method | Body / Params |
|---|---|---|
| `/memory` | GET | `?limit=50` |
| `/memory` | POST | `{content, metadata}` |
| `/memory/search` | POST | `{query, n_results}` |
| `/memory/<doc_id>` | DELETE | — |
| `/memory/clear` | POST | — |
| `/memory/consolidate` | POST | — |

### Model & Config

| Endpoint | Method | Mô tả |
|---|---|---|
| `/models` | GET | Danh sách model (Anthropic + OpenAI-compat) |
| `/client-config` | GET | Config cho frontend |

### Checkpoint & Schedule

| Endpoint | Method | Mô tả |
|---|---|---|
| `/checkpoints` | GET | Danh sách checkpoint |
| `/checkpoints/<id>/restore` | POST | Khôi phục checkpoint |
| `/schedules` | GET | Danh sách scheduled jobs |
| `/schedules/<job_id>` | DELETE | Xóa job |

### Monitor

| Endpoint | Method | Mô tả |
|---|---|---|
| `/monitors` | GET | Danh sách monitors đang chạy |
| `/monitors/file` | POST | Theo dõi thay đổi file |
| `/monitors/calendar` | POST | Theo dõi calendar |
| `/monitors/system` | POST | Theo dõi system metrics |
| `/monitors/<id>` | DELETE | Dừng monitor |
| `/monitors/events` | GET | Lấy events gần nhất |

### File & Tiện ích

| Endpoint | Method | Mô tả |
|---|---|---|
| `/list-files` | GET | `?q=query` — liệt kê files Desktop/Downloads (cho @mention) |
| `/read-file-b64` | POST | `{path}` — đọc file trả về base64 |
| `/generate-title` | POST | Sinh tiêu đề hội thoại |
| `/suggest-followups` | POST | `{question, answer, tool_names}` — gợi ý tiếp theo |
| `/pipeline` | POST | `{task}` — chạy pipeline đa-agent |
| `/computer-use` | POST | `{task}` — Computer Use (SSE stream) |
| `/health` | GET | Trạng thái ChromaDB, scheduler, active streams |

---

## Công cụ (Tools)

Schema đầy đủ trong biến `TOOLS` trong `server.py`.

### Shell & Desktop

| Tool | Input | Mô tả |
|---|---|---|
| `run_shell` | `cmd` | Chạy lệnh bash, output streaming |
| `open_app` | `app_name` | Mở ứng dụng macOS |
| `run_applescript` | `script` | Chạy AppleScript |
| `read_file` | `path` | Đọc file (tối đa 8000 ký tự) |
| `write_file` | `path, content` | Ghi file (server gửi `before_content` để diff) |
| `notify` | `title, message` | Thông báo macOS |
| `schedule_task` | `task, delay_seconds` | Lên lịch task chạy sau N giây |
| `screenshot_and_analyze` | `question` | Chụp màn hình desktop + phân tích vision |

### Browser (Playwright)

| Tool | Input | Mô tả |
|---|---|---|
| `browser_navigate` | `url` | Mở URL trong Chrome |
| `browser_evaluate` | `js` | Chạy JavaScript trên trang |
| `browser_fill` | `selector, value, sensitive?` | Điền input |
| `browser_click` | `selector?, text?` | Click theo selector hoặc text |
| `browser_scroll` | `direction, amount?, selector?` | Cuộn trang |
| `browser_wait_for_human` | `condition, timeout_ms?` | Đợi selector/navigation/network_idle |
| `browser_new_tab` | `url?` | Mở tab mới |
| `browser_switch_tab` | `tab_id` | Chuyển tab |
| `browser_list_tabs` | — | Liệt kê tabs |
| `browser_close_tab` | `tab_id` | Đóng tab |
| `browser_analyze_page` | `focus?` | Vision phân tích layout trang (SLOW — chỉ khi DOM tools fail) |
| `browser_vision_click` | `target, verify?, selector?` | Click theo mô tả ngôn ngữ tự nhiên |
| `browser_vision_type` | `target, text` | Gõ vào field theo mô tả |

### Bộ nhớ & Dữ liệu

| Tool | Input | Mô tả |
|---|---|---|
| `remember` | `content, category?` | Lưu vào ChromaDB |
| `recall` | `query` | Tìm kiếm semantic trong memory |
| `extract_data` | `schema, source` | Trích xuất dữ liệu theo JSON schema |

> **Chiến lược browser:** Luôn ưu tiên DOM tools (`browser_evaluate`, `browser_click`, `browser_fill`) trước. Chỉ dùng vision tools khi DOM tools thất bại hoặc trang có CAPTCHA/canvas UI.

---

## Error Recovery

Khi tool thất bại, Oculo không crash toàn bộ task.

### Phân loại lỗi (`utils/error_classifier.py`)

| Tầng | Ví dụ | Hành vi |
|---|---|---|
| **Transient** | Rate limit 429, timeout, DB lock | Retry với backoff |
| **Recoverable** | Element not found, navigation failed | Retry ít lần → fallback |
| **Fatal** | Permission denied, invalid API key, captcha | Abort ngay, báo user |

### Retry config

```
Rate limit  → 4 attempts, base 30s, max 120s, jitter
DB lock     → 5 attempts, base 0.5s, max 10s, jitter
Network     → 3 attempts, base 2s, max 30s, jitter
Vision tools → 1 attempt (không retry — chuyển ngay sang DOM tools)
Fatal       → 1 attempt
```

### Fallback registry (`utils/fallback_registry.py`)

| Tool gốc | Fallback |
|---|---|
| `browser_click` | JS click → text search click |
| `browser_navigate` | Retry với domcontentloaded → curl |
| `browser_fill` | JS fill via evaluate |
| `screenshot_and_analyze` | DOM text extraction |
| `run_shell` | AppleScript do shell script |

---

## Bộ nhớ dài hạn

ChromaDB với embedding model `all-MiniLM-L6-v2` chạy local — không gửi data ra ngoài.

**Cách hoạt động:**
1. Agent gọi `remember` → lưu vào ChromaDB với metadata
2. Mỗi turn, server tự động search memory theo query → inject vào system prompt (chỉ khi similarity ≥ 72%)
3. APScheduler gom/củng cố bộ nhớ cũ mỗi 30 phút

**Quản lý qua UI:** Menu `⋯` → Bộ nhớ

**Quản lý qua API:**
```bash
# Tìm kiếm
curl -X POST http://localhost:8080/memory/search \
  -H "Content-Type: application/json" \
  -d '{"query": "mật khẩu wifi", "n_results": 5}'

# Xóa tất cả
curl -X POST http://localhost:8080/memory/clear
```

---

## Giao diện

### Layout
- **Sidebar trái** — danh sách hội thoại, tìm kiếm, tạo mới
- **Header** — model switcher (badge màu theo tier), chế độ Chat/Điều khiển, menu `⋯`
- **Status bar** — trạng thái agent, model badge, activity toggle
- **Vùng chat** — messages, tool timeline, event pills, diff view
- **Input area** — textarea, @mention files, mic, nút gửi/hủy
- **Tab Điều khiển** — live screen (16:9), input, activity log với timeline

### Tính năng UI
- Markdown + syntax highlight (highlight.js)
- Tool timeline — mỗi tool call là một node với icon màu theo loại
- Live browser panel — floating panel hiện screenshot realtime khi agent dùng browser
- Ambient status orb — logo mắt đổi màu: xanh (idle) → tím (thinking) → vàng (tool running) → đỏ (error)
- Diff view — hiện before/after khi agent ghi file
- Proactive suggestions — gợi ý contextual dựa trên tools vừa chạy
- @mention files — gõ `@` để attach file từ Desktop/Downloads
- ↑ Arrow — chỉnh sửa message cuối khi input rỗng
- Automation Panel — drawer chứa kỹ năng, checkpoint, pipeline, giám sát, xuất dữ liệu
- Lazy load lịch sử (20 tin nhắn cuối)
- Phím tắt: `Enter` gửi, `Shift+Enter` xuống dòng, `⌥M` model picker, `⌘N` hội thoại mới

### Design system
- `tokens.css` — primitive tokens (màu, spacing, z-index, typography)
- Semantic tokens theo theme: `--bg-*`, `--border-*`, `--text-*`, `--interactive-*`, `--status-*`
- `data-theme="light"` / `"dark"` trên `<html>`
- Font weights: `--weight-normal` (400), `--weight-medium` (500), `--weight-semibold` (600), `--weight-bold` (700)

---

## Phát triển

**Chạy test:**

```bash
cd ai-agent
source venv/bin/activate
pytest
pytest tests/test_human_behavior.py -v
```

**Thêm tool mới:**

1. Implement function trong `tools/desktop.py` hoặc `tools/browser.py`
2. Thêm entry vào `TOOLS` list trong `server.py`
3. Thêm case trong `run_tool()` trong `server.py`
4. (Tùy chọn) Thêm fallback strategy trong `utils/fallback_registry.py`

**Thêm fallback strategy:**

```python
# utils/fallback_registry.py
FALLBACK_REGISTRY["tên_tool"] = [
    FallbackStrategy(
        name="tool_fallback",
        description="Mô tả ngắn",
        transform_input=lambda inp: {"key": inp.get("key")},
    ),
]
```

---

## Bảo mật

Oculo có thể **chạy lệnh shell tùy ý, sửa file, điều khiển trình duyệt** trên máy chạy server.

- Chỉ chạy trên máy và mạng bạn tin tưởng
- Server lắng nghe `0.0.0.0` — dùng firewall nếu cần giới hạn truy cập LAN
- Không commit `.env` lên Git
- Rate limiting: 60 request/60 giây mỗi IP (cấu hình qua `RATE_LIMIT_*`)
- Dữ liệu nhạy cảm trong tool output được mask trước khi gửi về client
- Embedding model chạy hoàn toàn local — không gửi nội dung bộ nhớ ra ngoài

---

*Oculo — Nhìn thấu · Hiểu sâu · Làm được mọi việc bạn cần.*
