# Tài liệu Yêu cầu: Nâng cấp AI Agent Intelligence

## Giới thiệu

Tính năng này nâng cấp toàn diện backend AI Agent (Python/Flask) hiện tại theo ba nhóm chính: **Accuracy** (độ chính xác), **Intelligence** (trí tuệ), và **Performance** (hiệu năng). Mục tiêu là cải thiện trải nghiệm người dùng thông qua phản hồi nhanh hơn, thông minh hơn và đáng tin cậy hơn.

## Bảng chú giải

- **Agent**: Hệ thống AI Agent Flask backend tại `server.py`
- **Tool**: Hàm thực thi lệnh hệ thống (run_shell, browser_*, v.v.)
- **Memory_Store**: Module ChromaDB tại `memory/store.py`
- **Orchestrator**: Pipeline đa agent tại `agents/orchestrator.py`
- **Stream**: Luồng SSE (Server-Sent Events) trả về client
- **Haiku**: Model `claude-haiku-4-5` dùng cho tác vụ nhẹ
- **Sonnet**: Model `claude-sonnet-4-5` dùng cho tác vụ phức tạp
- **Context_Injector**: Module mới inject thông tin môi trường vào system prompt
- **Task_Decomposer**: Module mới phân tách task phức tạp thành subtasks
- **Self_Corrector**: Module mới tự kiểm tra kết quả sau khi thực thi tool
- **Preference_Tracker**: Module mới theo dõi sở thích người dùng
- **Tool_Cache**: Module mới cache kết quả tool read-only
- **Model_Router**: Module mới phân loại và định tuyến model phù hợp
- **Prompt_Compressor**: Module mới nén lịch sử hội thoại dài

---

## Nhóm 1: Accuracy (Độ chính xác)

### Yêu cầu 1: Streaming Tool Results

**User Story:** Là người dùng, tôi muốn thấy output từng phần của các lệnh chạy lâu, để tôi không phải chờ đợi mà không biết tiến trình.

#### Tiêu chí chấp nhận

1. WHEN `run_shell` được gọi với lệnh có thời gian chạy dự kiến trên 2 giây, THE Agent SHALL stream từng dòng output về client qua SSE thay vì chờ lệnh hoàn thành.
2. WHEN một dòng output mới xuất hiện từ subprocess, THE Agent SHALL yield event `tool_stream` chứa nội dung dòng đó trong vòng 500ms.
3. WHEN lệnh shell kết thúc, THE Agent SHALL yield event `tool_result` chứa toàn bộ output tổng hợp.
4. IF subprocess bị timeout sau 60 giây, THEN THE Agent SHALL yield event `tool_error` với thông báo timeout và dừng stream.
5. WHILE lệnh shell đang chạy, THE Agent SHALL cho phép abort_event ngắt quá trình và dừng stream ngay lập tức.

---

### Yêu cầu 2: Tool Retry Logic

**User Story:** Là người dùng, tôi muốn agent tự động thử lại khi tool thất bại, để tôi không cần phải gửi lại yêu cầu thủ công.

#### Tiêu chí chấp nhận

1. WHEN `run_shell` hoặc `browser_navigate`, `browser_evaluate`, `browser_fill`, `browser_click` trả về lỗi, THE Agent SHALL tự động thử lại tối đa 3 lần.
2. WHEN thực hiện retry, THE Agent SHALL áp dụng exponential backoff với thời gian chờ lần lượt là 1s, 2s, 4s giữa các lần thử.
3. WHEN retry thành công trước lần thứ 3, THE Agent SHALL trả về kết quả thành công và dừng retry.
4. IF tất cả 3 lần retry đều thất bại, THEN THE Agent SHALL trả về thông báo lỗi cuối cùng kèm số lần đã thử.
5. WHEN retry đang diễn ra, THE Agent SHALL yield event `tool_retry` chứa tên tool, số lần thử hiện tại và lý do thất bại.

---

### Yêu cầu 3: Context Injection

**User Story:** Là người dùng, tôi muốn agent biết ngữ cảnh môi trường hiện tại (thư mục, app đang mở, thời gian, màn hình), để agent đưa ra hành động phù hợp hơn.

#### Tiêu chí chấp nhận

1. WHEN một request chat mới được nhận, THE Context_Injector SHALL thu thập thư mục làm việc hiện tại bằng lệnh `pwd`.
2. WHEN một request chat mới được nhận, THE Context_Injector SHALL thu thập danh sách ứng dụng đang mở bằng `osascript`.
3. WHEN một request chat mới được nhận, THE Context_Injector SHALL thu thập thời gian hiện tại theo định dạng ISO 8601.
4. WHEN một request chat mới được nhận, THE Context_Injector SHALL thu thập độ phân giải màn hình hiện tại.
5. THE Context_Injector SHALL inject tất cả thông tin môi trường vào system prompt trước khi gửi đến model, theo định dạng có cấu trúc rõ ràng.
6. IF việc thu thập bất kỳ thông tin môi trường nào thất bại, THEN THE Context_Injector SHALL bỏ qua thông tin đó và tiếp tục với các thông tin còn lại.

---

### Yêu cầu 4: Structured Output

**User Story:** Là người dùng, tôi muốn agent trích xuất dữ liệu có cấu trúc theo JSON schema, để tôi có thể xử lý dữ liệu một cách nhất quán.

#### Tiêu chí chấp nhận

1. THE Agent SHALL cung cấp tool `extract_data` với tham số `schema` (JSON schema object) và `source` (văn bản nguồn).
2. WHEN `extract_data` được gọi với schema hợp lệ và source text, THE Agent SHALL trả về JSON object tuân theo schema đã cung cấp.
3. WHEN `extract_data` được gọi, THE Agent SHALL sử dụng Anthropic API với `tool_choice` forced để đảm bảo output đúng schema.
4. IF schema không hợp lệ hoặc source text rỗng, THEN THE Agent SHALL trả về thông báo lỗi mô tả rõ vấn đề.
5. WHEN task của người dùng liên quan đến việc lấy dữ liệu có cấu trúc, THE Agent SHALL ưu tiên sử dụng `extract_data` thay vì parse thủ công.

---

## Nhóm 2: Intelligence (Trí tuệ)

### Yêu cầu 5: Memory Consolidation

**User Story:** Là người dùng, tôi muốn agent tự động tóm tắt và hợp nhất các memory cũ, để memory không bị phình to và vẫn giữ được thông tin quan trọng.

#### Tiêu chí chấp nhận

1. THE Memory_Store SHALL chạy background job tự động mỗi 30 phút để consolidate session memories cũ.
2. WHEN background job chạy, THE Memory_Store SHALL lấy tất cả memories có category `session` được tạo trước 30 phút.
3. WHEN có từ 5 session memories trở lên cần consolidate, THE Memory_Store SHALL gọi Haiku để tóm tắt thành tối đa 3 facts ngắn gọn (mỗi fact dưới 100 từ).
4. WHEN consolidation hoàn thành, THE Memory_Store SHALL lưu các facts mới với category `consolidated_fact` và xóa các session memories gốc.
5. IF Haiku API call thất bại trong quá trình consolidation, THEN THE Memory_Store SHALL giữ nguyên session memories gốc và log lỗi.
6. THE Memory_Store SHALL expose endpoint `/memory/consolidate` để trigger consolidation thủ công.

---

### Yêu cầu 6: Task Decomposition

**User Story:** Là người dùng, tôi muốn agent tự chia nhỏ task phức tạp thành các bước rõ ràng, để tôi theo dõi được tiến trình và agent thực hiện chính xác hơn.

#### Tiêu chí chấp nhận

1. WHEN task của người dùng có độ dài trên 50 từ, THE Task_Decomposer SHALL phân tích và chia thành danh sách subtasks trước khi thực thi.
2. WHEN phân tách task, THE Task_Decomposer SHALL yield event `decomposition` chứa danh sách subtasks với thứ tự thực hiện.
3. WHEN bắt đầu thực thi mỗi subtask, THE Agent SHALL yield event `subtask_start` chứa index và mô tả subtask.
4. WHEN hoàn thành mỗi subtask, THE Agent SHALL yield event `subtask_done` chứa index, mô tả và kết quả tóm tắt.
5. IF task có dưới 50 từ, THEN THE Task_Decomposer SHALL bỏ qua bước phân tách và thực thi trực tiếp.
6. THE Task_Decomposer SHALL sử dụng Haiku để phân tách task nhằm tiết kiệm chi phí.

---

### Yêu cầu 7: Self-Correction

**User Story:** Là người dùng, tôi muốn agent tự kiểm tra kết quả sau khi thực thi, để đảm bảo hành động đã được thực hiện đúng.

#### Tiêu chí chấp nhận

1. WHEN `write_file` được thực thi thành công, THE Self_Corrector SHALL tự động gọi `read_file` trên cùng path để xác minh nội dung đã được ghi đúng.
2. WHEN `browser_navigate` được thực thi thành công, THE Self_Corrector SHALL tự động chạy `browser_evaluate` để lấy `document.title` và xác minh đã navigate đúng URL.
3. WHEN verification thành công, THE Agent SHALL yield event `verification_passed` chứa tên tool và kết quả xác minh.
4. IF verification thất bại, THEN THE Agent SHALL yield event `verification_failed` chứa tên tool, kết quả mong đợi và kết quả thực tế, sau đó thử lại tool gốc một lần.
5. THE Self_Corrector SHALL chỉ áp dụng cho `write_file` và `browser_navigate` trong phiên bản đầu tiên.

---

### Yêu cầu 8: User Preference Learning

**User Story:** Là người dùng, tôi muốn agent học và ghi nhớ sở thích của tôi, để agent phản hồi theo cách tôi thích mà không cần nhắc lại.

#### Tiêu chí chấp nhận

1. THE Preference_Tracker SHALL phát hiện ngôn ngữ chính người dùng sử dụng trong mỗi message (tiếng Việt, tiếng Anh, v.v.) và lưu vào memory.
2. THE Preference_Tracker SHALL theo dõi độ dài response người dùng thích dựa trên phản hồi tích cực/tiêu cực (ngắn gọn vs chi tiết).
3. THE Preference_Tracker SHALL phát hiện format người dùng thích (markdown với headers/bullets vs plain text) dựa trên lịch sử tương tác.
4. WHEN preferences được cập nhật, THE Preference_Tracker SHALL lưu vào Memory_Store với category `user_preference` và overwrite giá trị cũ.
5. WHEN system prompt được tạo, THE Agent SHALL inject preferences hiện tại của người dùng vào system prompt để điều chỉnh hành vi.
6. IF chưa có đủ dữ liệu để xác định preference (dưới 3 interactions), THEN THE Preference_Tracker SHALL sử dụng giá trị mặc định (tiếng Việt, độ dài trung bình, markdown).

---

## Nhóm 3: Performance (Hiệu năng)

### Yêu cầu 9: Tool Parallelism

**User Story:** Là người dùng, tôi muốn các tool độc lập được chạy song song, để giảm thời gian chờ đợi khi agent thực hiện nhiều tác vụ cùng lúc.

#### Tiêu chí chấp nhận

1. WHEN model trả về nhiều tool_use blocks trong cùng một response, THE Agent SHALL phân tích dependency giữa các tool calls.
2. WHEN các tool calls không có dependency với nhau (output của tool này không là input của tool kia), THE Agent SHALL thực thi chúng song song bằng `ThreadPoolExecutor`.
3. WHEN các tool calls có dependency, THE Agent SHALL thực thi tuần tự theo thứ tự dependency.
4. WHEN tất cả parallel tool calls hoàn thành, THE Agent SHALL tổng hợp kết quả và tiếp tục vòng lặp agent.
5. THE Agent SHALL giới hạn tối đa 5 tool calls chạy song song cùng lúc để tránh quá tải hệ thống.
6. IF một tool call trong nhóm parallel thất bại, THEN THE Agent SHALL tiếp tục các tool calls còn lại và báo cáo lỗi riêng cho tool thất bại.

---

### Yêu cầu 10: Response Caching

**User Story:** Là người dùng, tôi muốn các lệnh read-only được cache kết quả, để agent phản hồi nhanh hơn khi hỏi thông tin hệ thống lặp lại.

#### Tiêu chí chấp nhận

1. THE Tool_Cache SHALL cache kết quả của `run_shell` cho các lệnh read-only: `ps`, `df`, `uname`, `date`, `whoami`, `hostname`, `uptime`, `sw_vers`.
2. WHEN một lệnh read-only được gọi và có cache hợp lệ (TTL chưa hết), THE Tool_Cache SHALL trả về kết quả từ cache thay vì thực thi lại.
3. THE Tool_Cache SHALL áp dụng TTL 60 giây cho tất cả cached results.
4. WHEN cache entry hết TTL, THE Tool_Cache SHALL tự động xóa entry đó và thực thi lại lệnh khi được gọi tiếp theo.
5. THE Tool_Cache SHALL sử dụng in-memory dictionary với key là chuỗi lệnh shell đầy đủ.
6. IF lệnh shell chứa pipe (`|`), redirect (`>`), hoặc biến (`$`), THEN THE Tool_Cache SHALL không cache kết quả của lệnh đó.

---

### Yêu cầu 11: Model Routing

**User Story:** Là người dùng, tôi muốn agent tự chọn model phù hợp với độ phức tạp của task, để tiết kiệm chi phí cho task đơn giản mà vẫn đảm bảo chất lượng cho task phức tạp.

#### Tiêu chí chấp nhận

1. THE Model_Router SHALL phân loại task thành hai loại: `simple` và `complex` trước khi gửi đến model.
2. WHEN task thuộc loại `simple` (chào hỏi, format văn bản, tóm tắt ngắn, câu hỏi thông tin đơn giản), THE Model_Router SHALL sử dụng Haiku.
3. WHEN task thuộc loại `complex` (yêu cầu dùng tool, lập trình, phân tích dữ liệu, task đa bước), THE Model_Router SHALL sử dụng Sonnet.
4. THE Model_Router SHALL phân loại dựa trên: độ dài message (>30 từ → complex), sự hiện diện của từ khóa tool-related, và lịch sử tool usage trong session.
5. WHEN model được chọn, THE Agent SHALL yield event `model_selected` chứa tên model và lý do phân loại.
6. WHERE người dùng đã chỉ định model cụ thể trong request, THE Model_Router SHALL tôn trọng lựa chọn đó và bỏ qua auto-routing.

---

### Yêu cầu 12: Prompt Compression

**User Story:** Là người dùng, tôi muốn agent xử lý được hội thoại dài mà không bị mất ngữ cảnh quan trọng, để tôi có thể làm việc trong các session kéo dài.

#### Tiêu chí chấp nhận

1. WHEN lịch sử hội thoại vượt quá 20 messages, THE Prompt_Compressor SHALL kích hoạt quá trình nén.
2. WHEN nén được kích hoạt, THE Prompt_Compressor SHALL giữ nguyên 4 messages gần nhất và tóm tắt tất cả messages cũ hơn.
3. WHEN tóm tắt messages cũ, THE Prompt_Compressor SHALL sử dụng Haiku để tạo summary ngắn gọn (tối đa 500 từ) chứa các điểm quan trọng.
4. THE Prompt_Compressor SHALL thay thế các messages cũ bằng một message duy nhất có role `user` với nội dung là summary.
5. IF Haiku API call thất bại trong quá trình nén, THEN THE Prompt_Compressor SHALL giữ nguyên lịch sử gốc và log cảnh báo.
6. WHEN compression xảy ra, THE Agent SHALL yield event `history_compressed` chứa số messages đã nén và độ dài summary.
