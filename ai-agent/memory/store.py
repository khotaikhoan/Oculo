"""
Long-term memory using ChromaDB + sentence-transformers embeddings.
Stores facts, summaries, and past interactions across sessions.
"""
import os
import sys
import json
import chromadb
from datetime import datetime
from chromadb.utils import embedding_functions

# Ghi ChromaDB ra thư mục user-writable khi app chạy từ .app bundle (read-only).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.app_paths import data_dir  # noqa: E402

DB_PATH = str(data_dir("chroma_db"))

# Use local sentence-transformers (no API key needed)
_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

_client = chromadb.PersistentClient(path=DB_PATH)

# Collections
_memories  = _client.get_or_create_collection("memories",  embedding_function=_ef)
_summaries = _client.get_or_create_collection("summaries", embedding_function=_ef)


def save_memory(content: str, metadata: dict = None):
    """Save a fact or piece of information to long-term memory."""
    doc_id = f"mem_{datetime.now().timestamp()}"
    meta = {"timestamp": datetime.now().isoformat(), "type": "memory"}
    if metadata:
        meta.update(metadata)
    _memories.add(documents=[content], ids=[doc_id], metadatas=[meta])
    return doc_id


def save_session_summary(session_id: str, summary: str, key_facts: list[str]):
    """Save a summary of a chat session."""
    doc_id = f"sess_{session_id}"
    _summaries.add(
        documents=[summary],
        ids=[doc_id],
        metadatas=[{
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "key_facts": json.dumps(key_facts)
        }]
    )


def search_memory(query: str, n_results: int = 5) -> list[dict]:
    """Search long-term memory for relevant information."""
    results = []
    for collection in [_memories, _summaries]:
        try:
            count = collection.count()
            if count == 0:
                continue
            r = collection.query(query_texts=[query], n_results=min(n_results, count))
            distances = r.get("distances") or [[]]
            for i, doc in enumerate(r["documents"][0]):
                dist = distances[0][i] if distances and distances[0] and i < len(distances[0]) else 1.0
                if not isinstance(dist, (int, float)):
                    dist = 1.0
                results.append({
                    "id": r["ids"][0][i],
                    "content": doc,
                    "metadata": r["metadatas"][0][i],
                    "distance": dist,
                })
        except Exception:
            pass
    # Sort by relevance (lower distance = more relevant)
    results.sort(key=lambda x: x.get("distance", 1.0))
    return results[:n_results]


def get_memory_context(query: str) -> str:
    """Get formatted memory context — legacy, returns all results."""
    memories = search_memory(query, n_results=4)
    if not memories:
        return ""
    lines = ["[Relevant memories from past sessions:]"]
    for m in memories:
        ts = m["metadata"].get("timestamp", "")[:10]
        lines.append(f"- [{ts}] {m['content']}")
    return "\n".join(lines)


def search_memory_with_scores(query: str, n_results: int = 6) -> list[dict]:
    """Search memory and return results with distance scores for threshold filtering."""
    return search_memory(query, n_results=n_results)


def list_memories(limit: int = 20) -> list[dict]:
    """List recent memories, sorted by timestamp descending."""
    try:
        r = _memories.get(include=["documents", "metadatas", "ids"])
        items = [
            {"id": r["ids"][i], "content": r["documents"][i], "metadata": r["metadatas"][i]}
            for i in range(len(r["documents"]))
        ]
        # Sort by timestamp descending (newest first)
        items.sort(
            key=lambda x: x["metadata"].get("timestamp", ""),
            reverse=True,
        )
        return items[:limit]
    except Exception:
        return []


def delete_memory(doc_id: str):
    """Delete a specific memory (memories hoặc summaries — tìm đúng collection)."""
    for coll in (_memories, _summaries):
        try:
            coll.delete(ids=[doc_id])
        except Exception:
            pass


def clear_all_memories():
    """Clear all memories (use with caution)."""
    _client.delete_collection("memories")
    _client.delete_collection("summaries")
    global _memories, _summaries
    _memories  = _client.get_or_create_collection("memories",  embedding_function=_ef)
    _summaries = _client.get_or_create_collection("summaries", embedding_function=_ef)


def consolidate_old_memories(anthropic_client) -> dict:
    """
    Tóm tắt session memories cũ hơn 30 phút thành facts ngắn gọn bằng Haiku.
    Requirements: 5.1 - 5.6
    """
    import time
    from datetime import datetime, timedelta

    cutoff = (datetime.now() - timedelta(minutes=30)).isoformat()

    try:
        all_mems = _memories.get(include=["documents", "metadatas", "ids"])
    except Exception as e:
        return {"consolidated": 0, "reason": f"fetch failed: {e}"}

    old_ids, old_docs = [], []
    for i, meta in enumerate(all_mems.get("metadatas", [])):
        if (meta.get("category") in ("session", "general") and
                meta.get("timestamp", "9999") < cutoff):
            old_ids.append(all_mems["ids"][i])
            old_docs.append(all_mems["documents"][i])

    if len(old_docs) < 5:
        return {"consolidated": 0, "reason": "not enough old session memories"}

    combined = "\n".join(old_docs[:20])  # Giới hạn để tránh token quá lớn
    try:
        user_msg = (
            f"Tóm tắt các memories sau thành tối đa 3 facts ngắn gọn "
            f"(mỗi fact 1 dòng, dưới 100 từ):\n\n{combined}"
        )
        model_h = os.getenv("HAIKU_MODEL") or os.getenv("MODEL", "claude-sonnet-4.6")
        r = anthropic_client.messages.create(
            model=model_h,
            max_tokens=512,
            messages=[{"role": "user", "content": user_msg}],
        )
        facts_text = next((b.text for b in r.content if hasattr(b, "type") and b.type == "text"), "")
        if not facts_text:
            return {"consolidated": 0, "reason": "no text in api response"}
        facts = [f.strip() for f in facts_text.split("\n") if f.strip()][:3]
    except Exception as e:
        return {"consolidated": 0, "reason": f"haiku api failed: {e}"}

    # Lưu facts mới
    for fact in facts:
        save_memory(fact, {"category": "consolidated_fact"})

    # Xóa memories cũ
    try:
        _memories.delete(ids=old_ids)
    except Exception:
        pass

    return {"consolidated": len(old_ids), "facts_created": len(facts)}
