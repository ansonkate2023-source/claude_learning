"""Extractive summarizer - picks the most relevant sentences from content."""

import re

from src.collectors.base import Item


def summarize_items(items: list[Item]) -> list[Item]:
    """Generate summaries for all items."""
    for item in items:
        if not item.summary and item.content:
            item.summary = _extractive_summary(item.content, item.title, max_sentences=3)
        elif not item.summary:
            item.summary = item.title
    return items


def _extractive_summary(content: str, title: str, max_sentences: int = 3) -> str:
    """Extract the most relevant sentences based on position and keyword overlap."""
    sentences = _split_sentences(content)
    if not sentences:
        return content[:200] if content else ""

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    # Score sentences
    title_words = set(title.lower().split())
    scored = []
    for i, sent in enumerate(sentences):
        score = 0.0
        # Position bonus: first and last sentences
        if i == 0:
            score += 2.0
        elif i == len(sentences) - 1:
            score += 1.0

        # Keyword overlap with title
        sent_words = set(sent.lower().split())
        overlap = len(title_words & sent_words)
        score += overlap * 0.5

        # Length preference: not too short, not too long
        word_count = len(sent.split())
        if 10 <= word_count <= 40:
            score += 1.0

        scored.append((score, i, sent))

    # Pick top sentences, preserve original order
    scored.sort(key=lambda x: x[0], reverse=True)
    top = sorted(scored[:max_sentences], key=lambda x: x[1])
    return " ".join(s[2] for s in top)


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 10]
