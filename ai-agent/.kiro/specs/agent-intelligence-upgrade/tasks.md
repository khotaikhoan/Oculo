# Kế hoạch triển khai: Agent Intelligence Upgrade

## Tổng quan

Triển khai 12 tính năng nâng cấp AI Agent theo 3 nhóm: Accuracy, Intelligence, Performance. Mỗi tính năng được implement như một module độc lập, sau đó tích hợp vào `server.py`.

## Tasks

- [x] 1. Thiết lập cấu trúc thư mục và testing framework
  - Tạo thư mục `ai-agent/utils/` và `ai-agent/tests/`
  - Tạo `ai-agent/utils/__init__.py` và `ai-agent/tests/__init__.py`
  - Cài đặt dependencies: `hypothesis` cho property testing
  - _Requirements: tất cả_

- [x] 2. Implement Tool Cache (Performance - Yêu cầu 10)
  - [x] 2.1 Tạo `ai-agent/utils/tool_cache.py`
    - Implement `CacheEntry` dataclass với `is_valid()` dựa trên TTL 60s
    - Implement `is_cacheable(cmd)`: kiểm tra READ_ONLY_COMMANDS và UNSAFE_PATTERNS
    - Implement `get_cached(cmd)` và `set_cache(cmd, result)`
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_
  - [ ]* 2.2 Viết property test cho Tool Cache
    - **Property 9: Cache read-only commands**
    - **Validates: Requirements 10.1, 10.2, 10.6**

- [x] 3. Implement Model Router (Performance - Yêu cầu 11)
  - [x] 3.1 Tạo `ai-agent/utils/model_router.py`
    - Implement `ModelRoutingDecision` dataclass
    - Implement `route_model(message, has_tool_history, user_specified_model)` với logic phân loại simple/complex
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_
  - [ ]* 3.2 Viết property test cho Model Router
    - **Property 10: Model routing correctness**
    - **Validates: Requirements 11.1, 11.2, 11.3, 11.6**

- [x] 4. Implement Prompt Compressor (Performance - Yêu cầu 12)
  - [x] 4.1 Tạo `ai-agent/utils/prompt_compressor.py`
    - Implement `compress_history(messages, anthropic_client)` với threshold 20 messages, giữ 4 gần nhất
    - Gọi Haiku để tóm tắt messages cũ, xử lý API failure gracefully
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6_
  - [ ]* 4.2 Viết property test cho Prompt Compressor
    - **Property 11: Prompt compression reduces history length**
    - **Validates: Requirements 12.1, 12.2, 12.3**

- [x] 5. Implement Retry Logic (Accuracy - Yêu cầu 2)
  - [x] 5.1 Tạo `ai-agent/utils/retry.py`
    - Implement `run_tool_with_retry(name, inputs, yield_fn, max_retries=3)` với exponential backoff 1s/2s/4s
    - Yield `tool_retry` event với tên tool, số lần thử, lý do thất bại
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_
  - [ ]* 5.2 Viết property test cho Retry Logic
    - **Property 2: Retry count và backoff**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.5**

- [x] 6. Implement Context Injector (Accuracy - Yêu cầu 3)
  - [x] 6.1 Tạo `ai-agent/utils/context_injector.py`
    - Implement `get_environment_context()`: thu thập pwd, thời gian, apps đang mở, màn hình resolution
    - Mỗi source được wrap trong try/except riêng, failure không ảnh hưởng sources khác
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_
  - [ ]* 6.2 Viết property test cho Context Injector
    - **Property 3: Context injection completeness**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6**

- [x] 7. Checkpoint — Đảm bảo tất cả tests pass
  - Chạy `pytest ai-agent/tests/ -v` và đảm bảo tất cả tests pass
  - Kiểm tra imports và dependencies hoạt động đúng

- [x] 8. Implement Streaming Tool Results (Accuracy - Yêu cầu 1)
  - [x] 8.1 Thêm `run_shell_streaming(cmd, timeout=60)` vào `ai-agent/tools/desktop.py`
    - Dùng `subprocess.Popen` với `stdout=PIPE`, yield từng dòng output
    - Xử lý timeout bằng cách yield `__TIMEOUT__` sentinel
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_
  - [ ]* 8.2 Viết property test cho Streaming
    - **Property 1: Streaming output completeness**
    - **Validates: Requirements 1.1, 1.3**

- [x] 9. Implement Structured Output — extract_data tool (Accuracy - Yêu cầu 4)
  - [x] 9.1 Thêm tool `extract_data` vào `TOOLS` list trong `server.py`
    - Định nghĩa input_schema với `schema` (object) và `source` (string)
    - _Requirements: 4.1_
  - [x] 9.2 Implement handler `extract_data` trong `run_tool()` tại `server.py`
    - Gọi Anthropic API với `tool_choice={"type":"tool","name":"extracted"}` để force structured output
    - Validate inputs, trả về error message nếu schema rỗng hoặc source rỗng
    - _Requirements: 4.2, 4.3, 4.4, 4.5_
  - [ ]* 9.3 Viết unit test cho extract_data
    - Test với schema hợp lệ, schema không hợp lệ, source rỗng
    - **Property 4: Extract data schema conformance**
    - **Validates: Requirements 4.2, 4.4**

- [x] 10. Implement Memory Consolidation (Intelligence - Yêu cầu 5)
  - [x] 10.1 Thêm `consolidate_old_memories(anthropic_client)` vào `ai-agent/memory/store.py`
    - Lấy session memories cũ hơn 30 phút, gọi Haiku để tóm tắt thành ≤3 facts
    - Lưu facts mới với category `consolidated_fact`, xóa memories gốc
    - Xử lý API failure: giữ nguyên memories gốc nếu Haiku fail
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
  - [x] 10.2 Đăng ký APScheduler job trong `server.py` và thêm endpoint `/memory/consolidate`
    - `scheduler.add_job(lambda: memory_store.consolidate_old_memories(client), 'interval', minutes=30)`
    - _Requirements: 5.1, 5.6_
  - [ ]* 10.3 Viết property test cho Memory Consolidation
    - **Property 5: Memory consolidation reduces count**
    - **Validates: Requirements 5.2, 5.3, 5.4**

- [x] 11. Implement Task Decomposer (Intelligence - Yêu cầu 6)
  - [x] 11.1 Tạo `ai-agent/utils/task_decomposer.py`
    - Implement `decompose_task(task, anthropic_client)`: trả về list rỗng nếu ≤50 từ
    - Gọi Haiku để phân tách, parse output thành list subtasks (tối đa 6)
    - _Requirements: 6.1, 6.2, 6.5, 6.6_
  - [ ]* 11.2 Viết property test cho Task Decomposer
    - **Property 6: Task decomposition threshold**
    - **Validates: Requirements 6.1, 6.5**

- [x] 12. Implement Self-Corrector (Intelligence - Yêu cầu 7)
  - [x] 12.1 Tạo `ai-agent/utils/self_corrector.py`
    - Implement `verify_write_file(path, expected_content, run_tool_fn)`: read_file và so sánh
    - Implement `verify_browser_navigate(url, run_tool_fn)`: evaluate document.title + location.href
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_
  - [ ]* 12.2 Viết property test cho Self-Corrector
    - **Property 7: Write-then-read round trip**
    - **Validates: Requirements 7.1**

- [x] 13. Implement Preference Tracker (Intelligence - Yêu cầu 8)
  - [x] 13.1 Tạo `ai-agent/utils/preference_tracker.py`
    - Implement `detect_preferences(message, response_length)`: detect ngôn ngữ, phân loại độ dài
    - Implement `load_preferences(memory_store)` và `save_preferences(prefs, memory_store)`
    - Sử dụng `langdetect` library cho language detection
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.6_
  - [ ]* 13.2 Viết property test cho Preference Tracker
    - **Property 8: Preference save-load round trip**
    - **Validates: Requirements 8.1, 8.4**

- [x] 14. Implement Tool Parallelism (Performance - Yêu cầu 9)
  - [x] 14.1 Tạo `ai-agent/utils/tool_parallel.py`
    - Implement `can_run_parallel(tool_blocks)`: kiểm tra tất cả tools có trong INDEPENDENT_TOOLS
    - Implement `run_tools_parallel(tool_blocks, run_tool_fn, max_workers=5)` với ThreadPoolExecutor
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6_
  - [ ]* 14.2 Viết unit test cho Tool Parallelism
    - Test với 2 independent tools, test với dependent tools, test với >5 tools
    - _Requirements: 9.2, 9.5_

- [x] 15. Tích hợp tất cả modules vào server.py
  - [x] 15.1 Tích hợp Model Router vào đầu `stream_agent()`
    - Import và gọi `route_model()` để chọn model, yield `model_selected` event
    - Tôn trọng `user_specified_model` từ request
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_
  - [x] 15.2 Tích hợp Context Injector vào `stream_agent()`
    - Gọi `get_environment_context()` và append vào system_prompt
    - _Requirements: 3.5_
  - [x] 15.3 Tích hợp Prompt Compressor vào `stream_agent()`
    - Gọi `compress_history(messages, client)` trước vòng lặp chính, yield `history_compressed` event
    - _Requirements: 12.1, 12.6_
  - [x] 15.4 Tích hợp Task Decomposer vào `stream_agent()`
    - Gọi `decompose_task()` với query, yield `decomposition` và `subtask_start`/`subtask_done` events
    - _Requirements: 6.2, 6.3, 6.4_
  - [x] 15.5 Tích hợp Tool Cache, Retry Logic, Streaming vào `run_tool()` và vòng lặp tool execution
    - Wrap `run_shell` với cache check trước, streaming cho long-running commands
    - Wrap RETRYABLE_TOOLS với `run_tool_with_retry()`
    - _Requirements: 1.1, 1.3, 2.1, 10.1, 10.2_
  - [x] 15.6 Tích hợp Tool Parallelism vào vòng lặp tool execution trong `stream_agent()`
    - Kiểm tra `can_run_parallel()`, nếu true dùng `run_tools_parallel()`, ngược lại chạy tuần tự
    - _Requirements: 9.1, 9.2, 9.3, 9.4_
  - [x] 15.7 Tích hợp Self-Corrector sau tool execution trong `stream_agent()`
    - Sau `write_file` và `browser_navigate`, gọi verify tương ứng, yield verification events
    - _Requirements: 7.1, 7.2, 7.3, 7.4_
  - [x] 15.8 Tích hợp Preference Tracker vào `stream_agent()`
    - Load preferences đầu session, inject vào system prompt
    - Sau khi agent trả lời, detect và save preferences mới
    - _Requirements: 8.5, 8.6_

- [x] 16. Checkpoint cuối — Đảm bảo tất cả tests pass
  - Chạy `pytest ai-agent/tests/ -v --tb=short` và đảm bảo tất cả tests pass
  - Kiểm tra server khởi động không có lỗi import
  - Đảm bảo tất cả 12 tính năng hoạt động end-to-end

## Ghi chú

- Tasks đánh dấu `*` là optional (tests), có thể bỏ qua để tập trung vào MVP
- Mỗi task tham chiếu requirements cụ thể để đảm bảo traceability
- Checkpoints tại task 7 và 16 để validate tiến trình
- Property tests dùng Hypothesis với tối thiểu 100 iterations mỗi property
- Unit tests dùng pytest với unittest.mock để mock Anthropic API và subprocess
