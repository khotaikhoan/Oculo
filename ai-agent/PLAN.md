# Oculo — Kế hoạch cải tiến UI/UX (audit)

Theo dõi triển khai; đánh dấu `[x]` khi xong.

## Tầng 1

- [x] Token `--z-*` trong `:root`, thay literal trong `style.css`
- [x] Gỡ Lucide CDN (không dùng)
- [x] `cu-dock` input: class `.cu-input-row` / `.cu-input-hint`
- [x] `#ctx-meter`: bỏ `!important`, layout khi hiển thị
- [x] Lỗi schedule / memory: class thay inline style trong `app.js`
- [x] Phím tắt: ghi chú Win/Linux (Ctrl/Alt)
- [x] `#ctx-tokens`: class thay inline opacity

## Tầng 2

- [x] Menu `…`: `role="region"` + nhóm `role="group"` + `aria-labelledby`
- [x] Gom shell `.hbtn` + `.hmore-btn` (30×30)
- [x] Memory: skeleton khi mở modal
- [x] Token `--accent-border-soft`, `--overlay-strong`

## Tầng 3

- [x] **IA header** — Ba cụm: `.header-cluster--brand` / `--model` / `--tools` (`role="group"` + `aria-label`)
- [x] **Gỡ inline handler trên `index.html`** — `data-oculo` + delegate trong `app.js` (`oculoUiActions`); `oninput` → delegate theo `#conv-search` / `#mem-search` / `#model-picker-search`
- [x] **Chia CSS** — `static/tokens.css` (tokens + theme), `style.css` `@import url("tokens.css")`
- [x] **JS sinh HTML** — template trong `app.js` dùng `data-oculo` / `data-conv-id` / delegate; khối `pre` (Chạy / Sao chép) dùng `runCmdFromPre` + `copyCodeBlock` qua `data-oculo`

**File chính:** `static/tokens.css`, `static/style.css`, `static/index.html`, `static/app.js`
