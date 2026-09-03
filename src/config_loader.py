from pathlib import Path
from typing import Any, Dict
import yaml

_CONFIG_CACHE: Dict[str, Any] | None = None


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    global _CONFIG_CACHE
    if _CONFIG_CACHE is not None:
        return _CONFIG_CACHE

    path = Path(config_path)
    if not path.is_file():
        return {
            "level": "INFO",
            "console": {
                "enabled": True,
                "level": "INFO",
                "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            },
            "file": {"enabled": False},
        }

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    _CONFIG_CACHE = data
    return _CONFIG_CACHE