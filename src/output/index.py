"""Generate a daily index.md overview file."""

from datetime import datetime
from pathlib import Path

from src.collectors.base import Item
from src.utils.logger import setup_logger

logger = setup_logger("index")


def write_index(items: list[Item], category_counts: dict[str, int], data_dir: Path):
    """Create an index.md with a table of all categories and top stories."""
    today = datetime.now().strftime("%Y-%m-%d")
    day_dir = data_dir / today
    day_dir.mkdir(parents=True, exist_ok=True)

    # Find top story per category (first item, usually most relevant)
    top_stories: dict[str, str] = {}
    for item in items:
        cat = item.category or "General"
        if cat not in top_stories:
            top_stories[cat] = item.title

    index_path = day_dir / "index.md"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(f"# Daily Digest - {today}\n\n")
        f.write("| Category | Items | Top Story |\n")
        f.write("|----------|-------|-----------|\n")

        for category in sorted(category_counts.keys()):
            count = category_counts[category]
            top = top_stories.get(category, "—")
            # Truncate long titles
            if len(top) > 50:
                top = top[:47] + "..."
            f.write(f"| [{category}](./{category}/summary.md) | {count} | {top} |\n")

        total = sum(category_counts.values())
        sources = len(set(item.source_name for item in items))
        f.write(f"\n**Total:** {total} items from {sources} sources\n")

    logger.info(f"Index written to {index_path}")
