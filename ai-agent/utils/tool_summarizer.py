"""
Tool Summarizer — cắt gọn tool output dài mà không gọi API.
Giữ phần đầu (context) + phần cuối (kết quả) để Claude vẫn hiểu output.
Trước: gọi Haiku API → +1-2s mỗi tool result dài.
Sau: smart truncation trong microseconds.
"""

HEAD_CHARS = 1400   # phần đầu: header, metadata
TAIL_CHARS = 500    # phần cuối: kết quả cuối
MAX_TOTAL  = HEAD_CHARS + TAIL_CHARS  # 1900 chars trước khi truncate


def maybe_summarize(tool_name: str, result, anthropic_client=None) -> str:
    """
    Smart truncate nếu result vượt ngưỡng.
    Không gọi API — instant, zero latency.
    """
    if not isinstance(result, str):
        result = str(result) if result is not None else ""
    if len(result) <= MAX_TOTAL:
        return result

    head = result[:HEAD_CHARS]
    tail = result[-TAIL_CHARS:]
    skipped = len(result) - HEAD_CHARS - TAIL_CHARS

    return (
        f"{head}\n"
        f"... [{skipped:,} ký tự đã lược bỏ] ...\n"
        f"{tail}"
    )
