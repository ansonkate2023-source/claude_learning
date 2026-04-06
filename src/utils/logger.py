"""Structured logging setup for the pipeline."""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(name: str = "pipeline") -> logging.Logger:
    """Configure and return a logger that writes to both console and file."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    file_handler = logging.FileHandler(log_dir / f"{today}.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
