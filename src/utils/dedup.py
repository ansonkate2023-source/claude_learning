"""SQLite-backed deduplication store."""

import hashlib
import sqlite3
from pathlib import Path


class DedupStore:
    """Tracks seen URLs and content hashes to avoid duplicate items."""

    def __init__(self, db_path: str = "data/.dedup.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._init_db()

    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS seen (
                hash TEXT PRIMARY KEY,
                url TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    @staticmethod
    def _hash(text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()

    def is_seen(self, url: str, content: str = "") -> bool:
        """Check if a URL or content hash has been seen before."""
        url_hash = self._hash(url)
        content_hash = self._hash(content) if content else None

        cursor = self.conn.execute("SELECT 1 FROM seen WHERE hash = ?", (url_hash,))
        if cursor.fetchone():
            return True

        if content_hash:
            cursor = self.conn.execute("SELECT 1 FROM seen WHERE hash = ?", (content_hash,))
            if cursor.fetchone():
                return True

        return False

    def mark_seen(self, url: str, content: str = ""):
        """Mark a URL and its content hash as seen."""
        url_hash = self._hash(url)
        self.conn.execute(
            "INSERT OR IGNORE INTO seen (hash, url) VALUES (?, ?)",
            (url_hash, url),
        )
        if content:
            content_hash = self._hash(content)
            self.conn.execute(
                "INSERT OR IGNORE INTO seen (hash, url) VALUES (?, ?)",
                (content_hash, url),
            )
        self.conn.commit()

    def close(self):
        self.conn.close()
