"""Normalize raw items into a consistent format."""

import re

from src.collectors.base import Item


def normalize_items(items: list[Item]) -> list[Item]:
    """Clean and normalize all items."""
    for item in items:
        item.title = _clean_text(item.title)
        item.content = _clean_text(item.content)
        # Ensure URL is clean
        item.url = item.url.strip()
    return items


def _clean_text(text: str) -> str:
    """Remove excess whitespace, control characters, and normalize text."""
    if not text:
        return ""
    # Remove control characters
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # Decode common HTML entities
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'")
    return text
