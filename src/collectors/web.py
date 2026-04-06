"""Web scraping collector using selectolax."""

from selectolax.parser import HTMLParser

from src.collectors.base import BaseCollector, Item
from src.utils.logger import setup_logger

logger = setup_logger("collector.web")


class WebCollector(BaseCollector):
    """Collects items by scraping web pages."""

    def collect(self) -> list[Item]:
        response = self.fetch_url(self.url)
        tree = HTMLParser(response.text)

        # Extract article-like elements
        selectors = self.config.get("selectors", {})
        item_selector = selectors.get("item", "article")
        title_selector = selectors.get("title", "h2 a, h3 a, .title a")
        content_selector = selectors.get("content", "p, .summary, .description")

        items = []
        for node in tree.css(item_selector):
            title_node = node.css_first(title_selector)
            if not title_node:
                continue

            title = title_node.text(strip=True)
            link = title_node.attributes.get("href", "")

            if not title or not link:
                continue

            # Make relative URLs absolute
            if link.startswith("/"):
                from urllib.parse import urlparse
                parsed = urlparse(self.url)
                link = f"{parsed.scheme}://{parsed.netloc}{link}"

            content_parts = []
            for p in node.css(content_selector):
                text = p.text(strip=True)
                if text:
                    content_parts.append(text)
            content = " ".join(content_parts)

            items.append(self._make_item(title, link, content))

        return items
