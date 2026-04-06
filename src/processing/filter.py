"""Filter out low-quality or noise items."""

from src.collectors.base import Item
from src.utils.logger import setup_logger

logger = setup_logger("filter")

# Minimum content length to be considered valid
MIN_CONTENT_LENGTH = 30

# Title blocklist patterns (ads, spam, etc.)
BLOCKLIST = [
    "sponsored",
    "advertisement",
    "click here",
    "subscribe now",
    "buy now",
]


def filter_items(items: list[Item]) -> list[Item]:
    """Remove low-quality items from the list."""
    filtered = []
    for item in items:
        if not item.title:
            continue
        if len(item.content) < MIN_CONTENT_LENGTH and not item.url:
            logger.debug(f"Filtered (too short): {item.title}")
            continue
        if _is_blocklisted(item.title):
            logger.debug(f"Filtered (blocklist): {item.title}")
            continue
        filtered.append(item)

    removed = len(items) - len(filtered)
    if removed > 0:
        logger.info(f"Filtered out {removed} low-quality items")
    return filtered


def _is_blocklisted(title: str) -> bool:
    """Check if a title matches blocklist patterns."""
    title_lower = title.lower()
    return any(term in title_lower for term in BLOCKLIST)
