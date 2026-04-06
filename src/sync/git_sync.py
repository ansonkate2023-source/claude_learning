"""Auto git sync: add, commit, push with change detection."""

import subprocess
from datetime import datetime

from src.utils.logger import setup_logger

logger = setup_logger("git_sync")


def git_sync(category_counts: dict[str, int], total_items: int, auto_push: bool = False) -> bool:
    """Stage data/ changes, commit with summary, and optionally push.

    Returns True if a commit was made, False if no changes.
    """
    # Check for changes
    result = subprocess.run(
        ["git", "status", "--porcelain", "data/"],
        capture_output=True, text=True, timeout=30,
    )
    if not result.stdout.strip():
        logger.info("No changes to commit")
        return False

    # Stage data directory
    subprocess.run(["git", "add", "data/"], check=True, timeout=30)

    # Build commit message
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    categories = ", ".join(f"{cat}({cnt})" for cat, cnt in sorted(category_counts.items()))
    message = f"[auto] {today}: collected {total_items} items — {categories}"

    # Commit
    result = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        logger.error(f"Commit failed: {result.stderr}")
        return False

    logger.info(f"Committed: {message}")

    # Push if enabled
    if auto_push:
        _push_with_retry()

    return True


def _push_with_retry(max_retries: int = 3):
    """Push to remote with retry logic."""
    for attempt in range(1, max_retries + 1):
        # Pull first to avoid conflicts
        subprocess.run(
            ["git", "pull", "--rebase"],
            capture_output=True, text=True, timeout=60,
        )

        result = subprocess.run(
            ["git", "push"],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode == 0:
            logger.info("Pushed to remote successfully")
            return

        logger.warning(f"Push attempt {attempt}/{max_retries} failed: {result.stderr}")

    logger.error("Push failed after all retries")
