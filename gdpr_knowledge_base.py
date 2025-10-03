"""Lightweight retrieval helper built on the GDPR corpus."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import joblib
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

DATA_DIR = Path(__file__).parent / "data"


@dataclass
class RetrievalResult:
    chunk_id: str
    article: str
    title: str
    chapter: Optional[str]
    section: Optional[str]
    text: str
    score: float


class GDPRKnowledgeBase:
    """Expose TF-IDF based retrieval over GDPR text."""

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        self.data_dir = data_dir or DATA_DIR
        self.vectorizer_path = self.data_dir / "gdpr_vectorizer.joblib"
        self.matrix_path = self.data_dir / "gdpr_tfidf.npz"
        self.index_path = self.data_dir / "gdpr_chunks_index.json"

        if not self.vectorizer_path.exists() or not self.matrix_path.exists() or not self.index_path.exists():
            raise FileNotFoundError(
                "Missing GDPR knowledge assets. Run data/build_gdpr_corpus.py and data/build_gdpr_vector_store.py first."
            )

        self.vectorizer = joblib.load(self.vectorizer_path)
        self.matrix = sparse.load_npz(self.matrix_path)
        self.chunks: List[Dict] = json.loads(self.index_path.read_text(encoding="utf-8"))

    def retrieve(self, query: str, top_k: int = 5, min_score: float = 0.05) -> List[RetrievalResult]:
        if not query.strip():
            return []

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(self.matrix, query_vec).ravel()

        ranked_indices = similarities.argsort()[::-1]
        results: List[RetrievalResult] = []

        for idx in ranked_indices[: top_k * 2]:  # fetch extras before filtering on score
            score = float(similarities[idx])
            if score < min_score:
                continue
            chunk = self.chunks[idx]
            results.append(
                RetrievalResult(
                    chunk_id=chunk["chunk_id"],
                    article=chunk["article"],
                    title=chunk["title"],
                    chapter=chunk.get("chapter"),
                    section=chunk.get("section"),
                    text=chunk["text"],
                    score=score,
                )
            )
            if len(results) >= top_k:
                break

        return results


__all__ = ["GDPRKnowledgeBase", "RetrievalResult"]
