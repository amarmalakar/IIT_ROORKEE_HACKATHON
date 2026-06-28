"""FAISS vector retrieval for context enrichment."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from backend.config.settings import get_settings

logger = logging.getLogger("codeforge.retriever")

DEFAULT_EXAMPLES: list[dict[str, str]] = [
    {
        "id": "two_sum_hashmap",
        "language": "python",
        "content": (
            "def two_sum(nums: list[int], target: int) -> list[int]:\n"
            "    seen = {}\n"
            "    for i, num in enumerate(nums):\n"
            "        complement = target - num\n"
            "        if complement in seen:\n"
            "            return [seen[complement], i]\n"
            "        seen[num] = i\n"
            "    return []"
        ),
        "tags": "hashmap two-pointer array",
    },
    {
        "id": "binary_search",
        "language": "python",
        "content": (
            "def binary_search(arr: list[int], target: int) -> int:\n"
            "    lo, hi = 0, len(arr) - 1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if arr[mid] == target:\n"
            "            return mid\n"
            "        elif arr[mid] < target:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "    return -1"
        ),
        "tags": "binary-search sorted-array",
    },
    {
        "id": "sql_window_dedup",
        "language": "sql",
        "content": (
            "SELECT user_id, event_type, event_time\n"
            "FROM (\n"
            "  SELECT *, ROW_NUMBER() OVER (\n"
            "    PARTITION BY user_id ORDER BY event_time DESC\n"
            "  ) AS rn\n"
            "  FROM events\n"
            ") t WHERE rn = 1"
        ),
        "tags": "window-function dedup sql",
    },
]


class ContextRetriever:
    """FAISS + HuggingFace embeddings retriever with graceful fallback."""

    def __init__(self, index_path: str | None = None) -> None:
        settings = get_settings()
        self.index_path = Path(index_path or settings.faiss_index_path)
        self._index = None
        self._embeddings = None
        self._documents: list[dict[str, str]] = list(DEFAULT_EXAMPLES)
        self._initialized = False

    def _try_init(self) -> bool:
        if self._initialized:
            return self._index is not None
        self._initialized = True
        if not get_settings().enable_semantic_search:
            return False
        try:
            import faiss  # noqa: F401
            from sentence_transformers import SentenceTransformer

            self._embeddings = SentenceTransformer(get_settings().embedding_model)
            if self.index_path.exists():
                import faiss as faiss_lib
                import numpy as np
                import pickle

                index_file = self.index_path / "index.faiss"
                docs_file = self.index_path / "docs.pkl"
                if index_file.exists() and docs_file.exists():
                    self._index = faiss_lib.read_index(str(index_file))
                    with open(docs_file, "rb") as f:
                        self._documents = pickle.load(f)
                    return True

            self._build_index()
            return True
        except Exception as exc:
            logger.warning("FAISS init failed, using keyword fallback: %s", exc)
            return False

    def _build_index(self) -> None:
        import faiss
        import numpy as np

        texts = [f"{d['tags']} {d['content']}" for d in self._documents]
        vectors = self._embeddings.encode(texts, show_progress_bar=False)
        vectors = np.array(vectors).astype("float32")
        dim = vectors.shape[1]
        self._index = faiss.IndexFlatIP(dim)
        faiss.normalize_L2(vectors)
        self._index.add(vectors)

    def retrieve(self, query: str, language: str = "", top_k: int = 3) -> list[dict[str, Any]]:
        """Retrieve top-k relevant code snippets."""
        if self._try_init() and self._index is not None and self._embeddings is not None:
            return self._semantic_search(query, language, top_k)
        return self._keyword_search(query, language, top_k)

    def _semantic_search(self, query: str, language: str, top_k: int) -> list[dict[str, Any]]:
        import faiss
        import numpy as np

        vector = self._embeddings.encode([query])
        vector = np.array(vector).astype("float32")
        faiss.normalize_L2(vector)
        scores, indices = self._index.search(vector, min(top_k * 2, len(self._documents)))

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            doc = self._documents[idx]
            if language and doc.get("language") != language:
                continue
            if float(score) < 0.3:
                continue
            results.append({
                "source": doc.get("id", f"doc_{idx}"),
                "language": doc.get("language", ""),
                "relevance_score": round(float(score), 2),
                "snippet": doc.get("content", ""),
                "usage_note": f"Reference pattern from {doc.get('id', 'knowledge base')}",
            })
            if len(results) >= top_k:
                break
        return results

    def _keyword_search(self, query: str, language: str, top_k: int) -> list[dict[str, Any]]:
        query_lower = query.lower()
        scored = []
        for doc in self._documents:
            if language and doc.get("language") != language:
                continue
            text = f"{doc.get('tags', '')} {doc.get('content', '')}".lower()
            words = query_lower.split()
            score = sum(1 for w in words if w in text) / max(len(words), 1)
            if score > 0:
                scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "source": doc.get("id", "example"),
                "language": doc.get("language", ""),
                "relevance_score": round(score, 2),
                "snippet": doc.get("content", ""),
                "usage_note": "Keyword-matched reference pattern",
            }
            for score, doc in scored[:top_k]
        ]


_retriever: ContextRetriever | None = None


def get_retriever() -> ContextRetriever:
    global _retriever
    if _retriever is None:
        _retriever = ContextRetriever()
    return _retriever
