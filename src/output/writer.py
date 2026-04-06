"""Write classified items to the data directory structure."""

import json
from datetime import datetime
from pathlib import Path

from src.collectors.base import Item
from src.utils.logger import setup_logger

logger = setup_logger("writer")


def write_output(items: list[Item], data_dir: Path) -> dict[str, int]:
    """Write items to /data/YYYY-MM-DD/{category}/ structure.

    Returns a dict of category -> item count.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    day_dir = data_dir / today

    # Group items by category
    by_category: dict[str, list[Item]] = {}
    for item in items:
        cat = item.category or "General"
        by_category.setdefault(cat, []).append(item)

    category_counts = {}
    for category, cat_items in by_category.items():
        cat_dir = day_dir / category
        cat_dir.mkdir(parents=True, exist_ok=True)

        # Write raw.json
        raw_path = cat_dir / "raw.json"
        raw_data = [_item_to_dict(item) for item in cat_items]
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=2)

        # Write summary.md
        summary_path = cat_dir / "summary.md"
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(f"# {category} - {today}\n\n")
            for item in cat_items:
                f.write(f"## {item.title}\n")
                f.write(f"**Source:** {item.source_name}")
                if item.tags:
                    f.write(f" | **Tags:** {', '.join(item.tags)}")
                f.write("\n\n")
                if item.summary:
                    f.write(f"> {item.summary}\n\n")
                f.write(f"[Read more]({item.url})\n\n---\n\n")

        category_counts[category] = len(cat_items)
        logger.info(f"Wrote {len(cat_items)} items to {cat_dir}")

    return category_counts


def _item_to_dict(item: Item) -> dict:
    """Convert an Item to a serializable dict."""
    return {
        "id": item.id,
        "title": item.title,
        "url": item.url,
        "content": item.content,
        "summary": item.summary,
        "source_name": item.source_name,
        "collected_at": item.collected_at,
        "tags": item.tags,
        "category": item.category,
        "extra": item.extra,
    }
