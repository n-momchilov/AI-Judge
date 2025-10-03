"""Build a lightweight TF-IDF vector store over GDPR retrieval chunks."""
from __future__ import annotations

import json
from pathlib import Path
from typing import List

import joblib
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_DIR = Path(__file__).parent
CHUNKS_PATH = DATA_DIR / "gdpr_chunks.jsonl"
MATRIX_PATH = DATA_DIR / "gdpr_tfidf.npz"
VECTORIZER_PATH = DATA_DIR / "gdpr_vectorizer.joblib"
INDEX_PATH = DATA_DIR / "gdpr_chunks_index.json"


def load_chunks() -> List[dict]:
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            "Chunk file not found. Run build_gdpr_corpus.py first to generate gdpr_chunks.jsonl"
        )

    chunks: List[dict] = []
    with CHUNKS_PATH.open("r", encoding="utf-8") as src:
        for line in src:
            line = line.strip()
            if not line:
                continue
            chunks.append(json.loads(line))
    return chunks


def build_vector_store(chunks: List[dict]) -> None:
    texts = [chunk["text"] for chunk in chunks]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95,
        lowercase=True,
    )

    matrix = vectorizer.fit_transform(texts)

    INDEX_PATH.write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    sparse.save_npz(MATRIX_PATH, matrix)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print(f"Stored TF-IDF matrix at {MATRIX_PATH.relative_to(DATA_DIR)}")
    print(f"Stored vectorizer at {VECTORIZER_PATH.relative_to(DATA_DIR)}")
    print(f"Stored chunk index at {INDEX_PATH.relative_to(DATA_DIR)}")


def main() -> None:
    print("Loading GDPR chunks ...")
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks")
    print("Building TF-IDF vector store ...")
    build_vector_store(chunks)


if __name__ == "__main__":
    main()
