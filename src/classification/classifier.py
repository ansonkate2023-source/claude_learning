"""Keyword-weighted topic classifier."""

from src.collectors.base import Item
from src.utils.logger import setup_logger

logger = setup_logger("classifier")

DEFAULT_CATEGORY = "General"


class Classifier:
    """Classifies items into categories using weighted keyword matching."""

    def __init__(self, taxonomy: dict[str, dict[str, int]]):
        # Pre-process: lowercase all keywords
        self.taxonomy = {
            category: {kw.lower(): weight for kw, weight in keywords.items()}
            for category, keywords in taxonomy.items()
        }

    def classify(self, item: Item) -> str:
        """Return the best-matching category for an item."""
        text = f"{item.title} {item.content}".lower()
        scores: dict[str, float] = {}

        for category, keywords in self.taxonomy.items():
            score = 0.0
            for keyword, weight in keywords.items():
                if keyword in text:
                    score += weight
                    # Bonus if keyword appears in title
                    if keyword in item.title.lower():
                        score += weight * 0.5
            scores[category] = score

        if not scores or max(scores.values()) == 0:
            return DEFAULT_CATEGORY

        return max(scores, key=scores.get)

    def classify_items(self, items: list[Item]) -> list[Item]:
        """Classify all items and set their category field."""
        category_counts: dict[str, int] = {}
        for item in items:
            item.category = self.classify(item)
            category_counts[item.category] = category_counts.get(item.category, 0) + 1

        for cat, count in sorted(category_counts.items()):
            logger.info(f"  {cat}: {count} items")

        return items
