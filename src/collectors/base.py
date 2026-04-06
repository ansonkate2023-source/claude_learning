"""Base collector with retry logic and rate limiting."""

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from src.utils.logger import setup_logger

logger = setup_logger("collector")


@dataclass
class Item:
    """Unified data item produced by all collectors."""
    id: str = ""
    title: str = ""
    url: str = ""
    content: str = ""
    summary: str = ""
    source_name: str = ""
    collected_at: str = ""
    tags: list[str] = field(default_factory=list)
    category: str = ""
    extra: dict = field(default_factory=dict)


class BaseCollector(ABC):
    """Abstract base for all data source collectors."""

    def __init__(self, source_config: dict, max_retries: int = 3, request_delay: float = 1.0):
        self.config = source_config
        self.name = source_config.get("name", "unknown")
        self.url = source_config.get("url", "")
        self.tags = source_config.get("tags", [])
        self.max_retries = max_retries
        self.request_delay = request_delay

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=2, max=30),
        retry=retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException)),
    )
    def fetch_url(self, url: str, **kwargs) -> httpx.Response:
        """Fetch a URL with retry and exponential backoff."""
        headers = self.config.get("headers", {})
        params = self.config.get("params", {})
        with httpx.Client(timeout=30, follow_redirects=True) as client:
            response = client.get(url, headers=headers, params=params, **kwargs)
            response.raise_for_status()
            return response

    @abstractmethod
    def collect(self) -> list[Item]:
        """Collect items from the source. Must be implemented by subclasses."""
        ...

    def _make_item(self, title: str, url: str, content: str, extra: dict | None = None) -> Item:
        """Helper to create an Item with common fields filled in."""
        import hashlib
        return Item(
            id=hashlib.sha256(url.encode()).hexdigest()[:16],
            title=title,
            url=url,
            content=content,
            source_name=self.name,
            collected_at=datetime.now(timezone.utc).isoformat(),
            tags=list(self.tags),
            extra=extra or {},
        )

    def safe_collect(self) -> list[Item]:
        """Collect with error handling - returns empty list on failure."""
        try:
            time.sleep(self.request_delay)
            items = self.collect()
            logger.info(f"[{self.name}] Collected {len(items)} items")
            return items
        except Exception as e:
            logger.error(f"[{self.name}] Collection failed: {e}")
            return []
