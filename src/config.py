"""Configuration loader for the pipeline."""

import os
import re
from pathlib import Path

import yaml
from dotenv import load_dotenv


def _expand_env_vars(obj):
    """Recursively expand ${VAR} references in strings."""
    if isinstance(obj, str):
        def replacer(match):
            var_name = match.group(1)
            return os.getenv(var_name, "")
        return re.sub(r"\$\{(\w+)\}", replacer, obj)
    elif isinstance(obj, dict):
        return {k: _expand_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_expand_env_vars(item) for item in obj]
    return obj


class Config:
    """Pipeline configuration loaded from .env and sources.yaml."""

    def __init__(self, config_path: str = "config/sources.yaml"):
        load_dotenv()

        self.data_dir = Path(os.getenv("DATA_DIR", "./data"))
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        self.request_delay = float(os.getenv("REQUEST_DELAY", "1.0"))
        self.git_auto_push = os.getenv("GIT_AUTO_PUSH", "false").lower() == "true"

        with open(config_path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        raw = _expand_env_vars(raw)

        self.sources = [s for s in raw.get("sources", []) if s.get("enabled", True)]
        self.taxonomy = raw.get("taxonomy", {})
