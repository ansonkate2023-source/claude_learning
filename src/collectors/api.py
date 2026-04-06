"""Generic REST API collector."""

from src.collectors.base import BaseCollector, Item
from src.utils.logger import setup_logger

logger = setup_logger("collector.api")


class APICollector(BaseCollector):
    """Collects items from REST APIs that return JSON."""

    def collect(self) -> list[Item]:
        response = self.fetch_url(self.url)
        data = response.json()

        # Handle GitHub-style API responses (items in an "items" key)
        if isinstance(data, dict) and "items" in data:
            entries = data["items"]
        elif isinstance(data, list):
            entries = data
        else:
            entries = [data]

        items = []
        for entry in entries:
            title = self._extract_field(entry, ["name", "title", "full_name"])
            url = self._extract_field(entry, ["html_url", "url", "link"])
            content = self._extract_field(entry, ["description", "body", "content", "summary"])

            if not title or not url:
                continue

            extra = {}
            for key in ["stargazers_count", "language", "created_at", "updated_at"]:
                if key in entry:
                    extra[key] = entry[key]

            items.append(self._make_item(title, url, content or "", extra))

        return items

    @staticmethod
    def _extract_field(data: dict, keys: list[str]) -> str:
        """Try multiple keys to extract a field value."""
        for key in keys:
            val = data.get(key)
            if val:
                return str(val).strip()
        return ""
