"""Utility for extracting structured GDPR articles from the source PDF."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

from pdfminer.high_level import extract_text

DATA_DIR = Path(__file__).parent
PDF_PATH = DATA_DIR / "GDPR.pdf"
ARTICLES_PATH = DATA_DIR / "gdpr_articles.json"
CHUNKS_PATH = DATA_DIR / "gdpr_chunks.jsonl"

ARTICLE_HEADER_PATTERN = re.compile(r"^Article\s+\d+[A-Za-z]?\s*$", re.IGNORECASE)
CHAPTER_PATTERN = re.compile(r"^Chapter\s+[IVXLC]+\s*$", re.IGNORECASE)
SECTION_PATTERN = re.compile(r"^Section\s+[IVXLC\d]+\s*$", re.IGNORECASE)


@dataclass
class Article:
    """Representation of a GDPR article."""

    article: str
    title: str
    chapter: Optional[str]
    section: Optional[str]
    text: str


@dataclass
class Chunk:
    """Smaller retrieval-friendly unit derived from an article."""

    article: str
    title: str
    chapter: Optional[str]
    section: Optional[str]
    chunk_id: str
    text: str


def _normalize(line: str) -> str:
    """Collapse repeated whitespace within a line while keeping spacing between words."""
    return " ".join(line.strip().split())


def parse_articles(raw_text: str) -> List[Article]:
    """Parse raw GDPR text into structured articles."""
    lines = raw_text.replace("\r\n", "\n").split("\n")

    articles: List[Article] = []
    current_chapter: Optional[str] = None
    current_section: Optional[str] = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if CHAPTER_PATTERN.match(line):
            chapter_number = _normalize(line).upper()
            j = i + 1
            chapter_title = ""
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                next_line = lines[j].strip()
                if next_line and not _is_heading(next_line):
                    chapter_title = _normalize(next_line)
                    i = j
            current_chapter = chapter_number + (" - " + chapter_title if chapter_title else "")
            current_section = None
            i += 1
            continue

        if SECTION_PATTERN.match(line):
            section_number = _normalize(line).upper()
            j = i + 1
            section_title = ""
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                next_line = lines[j].strip()
                if next_line and not _is_heading(next_line):
                    section_title = _normalize(next_line)
                    i = j
            current_section = section_number + (" - " + section_title if section_title else "")
            i += 1
            continue

        if ARTICLE_HEADER_PATTERN.match(line):
            article_label = "Article " + line.split()[1].upper()
            j = i + 1
            title = ""
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                next_line = lines[j].strip()
                if next_line and not _is_heading(next_line):
                    title = _normalize(next_line)
                    j += 1
            body_lines: List[str] = []
            while j < len(lines):
                peek = lines[j].strip()
                if not peek:
                    j += 1
                    continue
                if _is_heading(peek):
                    break
                body_lines.append(_normalize(lines[j]))
                j += 1

            articles.append(
                Article(
                    article=article_label,
                    title=title,
                    chapter=current_chapter,
                    section=current_section,
                    text="\n".join(body_lines),
                )
            )
            i = j
            continue

        i += 1

    return articles


def _is_heading(line: str) -> bool:
    line = line.strip()
    return bool(
        ARTICLE_HEADER_PATTERN.match(line)
        or CHAPTER_PATTERN.match(line)
        or SECTION_PATTERN.match(line)
    )


def iter_paragraph_chunks(article: Article) -> Iterable[Chunk]:
    """Split article text into numbered or paragraph-level chunks."""
    if not article.text:
        return []

    # Split at paragraph numbers (e.g., "1."), keeping the delimiter with the chunk.
    parts = re.split(r"\n(?=\d+\.)", article.text)
    if len(parts) == 1:
        parts = [article.text]

    for idx, part in enumerate(parts, start=1):
        value = part.strip()
        if not value:
            continue
        chunk_id = f"{article.article.replace(' ', '_').lower()}_p{idx}"
        yield Chunk(
            article=article.article,
            title=article.title,
            chapter=article.chapter,
            section=article.section,
            chunk_id=chunk_id,
            text=value,
        )


def write_articles(articles: List[Article]) -> None:
    data = [article.__dict__ for article in articles]
    ARTICLES_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_chunks(chunks: Iterable[Chunk]) -> None:
    with CHUNKS_PATH.open("w", encoding="utf-8") as stream:
        for chunk in chunks:
            stream.write(json.dumps(chunk.__dict__, ensure_ascii=False) + "\n")


def main() -> None:
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"GDPR source PDF not found at {PDF_PATH}")

    print("Extracting text from GDPR.pdf ...")
    raw_text = extract_text(str(PDF_PATH))
    print("Parsing articles ...")
    articles = parse_articles(raw_text)
    print(f"Parsed {len(articles)} articles")
    write_articles(articles)

    print("Creating retrieval chunks ...")
    chunk_iterables = []
    for article in articles:
        chunk_iterables.extend(iter_paragraph_chunks(article))
    print(f"Generated {len(chunk_iterables)} chunks")
    write_chunks(chunk_iterables)
    print(f"Saved articles to {ARTICLES_PATH.relative_to(DATA_DIR)}")
    print(f"Saved chunks to {CHUNKS_PATH.relative_to(DATA_DIR)}")


if __name__ == "__main__":
    main()
