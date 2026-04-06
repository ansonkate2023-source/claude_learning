"""Main pipeline orchestrator.

Pipeline flow:
  1. Load config
  2. Collect from all sources
  3. Deduplicate
  4. Normalize
  5. Filter
  6. Summarize
  7. Classify
  8. Write output (raw.json + summary.md per category)
  9. Write index
  10. Git sync
"""

from src.collectors.base import Item
from src.collectors.rss import RSSCollector
from src.collectors.api import APICollector
from src.collectors.web import WebCollector
from src.classification.classifier import Classifier
from src.config import Config
from src.output.index import write_index
from src.output.writer import write_output
from src.processing.filter import filter_items
from src.processing.normalizer import normalize_items
from src.processing.summarizer import summarize_items
from src.sync.git_sync import git_sync
from src.utils.dedup import DedupStore
from src.utils.logger import setup_logger

logger = setup_logger("pipeline")

COLLECTOR_MAP = {
    "rss": RSSCollector,
    "api": APICollector,
    "web": WebCollector,
}


def run_pipeline(config: Config) -> None:
    """Execute the full data pipeline."""
    logger.info("=" * 50)
    logger.info("Pipeline started")

    # Step 1: Collect
    all_items: list[Item] = []
    for source in config.sources:
        collector_cls = COLLECTOR_MAP.get(source["type"])
        if not collector_cls:
            logger.warning(f"Unknown source type: {source['type']}")
            continue
        collector = collector_cls(source, config.max_retries, config.request_delay)
        items = collector.safe_collect()
        all_items.extend(items)

    logger.info(f"Total collected: {len(all_items)} items")
    if not all_items:
        logger.info("No items collected, exiting")
        return

    # Step 2: Deduplicate
    dedup = DedupStore(str(config.data_dir / ".dedup.db"))
    unique_items = []
    for item in all_items:
        if not dedup.is_seen(item.url, item.content):
            dedup.mark_seen(item.url, item.content)
            unique_items.append(item)
    dedup.close()
    logger.info(f"After dedup: {len(unique_items)} items ({len(all_items) - len(unique_items)} duplicates)")

    if not unique_items:
        logger.info("All items are duplicates, exiting")
        return

    # Step 3: Normalize
    unique_items = normalize_items(unique_items)

    # Step 4: Filter
    unique_items = filter_items(unique_items)
    logger.info(f"After filtering: {len(unique_items)} items")

    # Step 5: Summarize
    unique_items = summarize_items(unique_items)

    # Step 6: Classify
    classifier = Classifier(config.taxonomy)
    unique_items = classifier.classify_items(unique_items)

    # Step 7: Write output
    category_counts = write_output(unique_items, config.data_dir)

    # Step 8: Write index
    write_index(unique_items, category_counts, config.data_dir)

    # Step 9: Git sync
    total = sum(category_counts.values())
    git_sync(category_counts, total, config.git_auto_push)

    logger.info(f"Pipeline complete: {total} items in {len(category_counts)} categories")
    logger.info("=" * 50)


def main():
    config = Config()
    run_pipeline(config)


if __name__ == "__main__":
    main()
