"""RSS/Atom feed collector."""

import feedparser

from src.collectors.base import BaseCollector, Item
from src.utils.logger import setup_logger

logger = setup_logger("collector.rss")


class RSSCollector(BaseCollector):
    """Collects items from RSS/Atom feeds."""

    def collect(self) -> list[Item]:
        response = self.fetch_url(self.url)
        feed = feedparser.parse(response.text)

        items = []
        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            if not title or not link:
                continue

            # Get content from various feed formats
            content = ""
            if "content" in entry and entry.content:
                content = entry.content[0].get("value", "")
            elif "summary" in entry:
                content = entry.get("summary", "")
            elif "description" in entry:
                content = entry.get("description", "")

            # Strip HTML tags for plain text
            content = self._strip_html(content)

            extra = {
                "published": entry.get("published", ""),
                "author": entry.get("author", ""),
            }

            items.append(self._make_item(title, link, content, extra))

        return items

    @staticmethod
    def _strip_html(text: str) -> str:
        """Remove HTML tags from text."""
        import re
        clean = re.sub(r"<[^>]+>", "", text)
        clean = re.sub(r"\s+", " ", clean).strip()
        return clean
