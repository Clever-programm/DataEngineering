import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from src.config_loader import load_config

def get_logger(name: str, file_path: Optional[str], config_path: str = "config.yaml") -> logging.Logger:
    """
    Возвращает настроенный экземпляр логгера по переданному имени.
    
    :param name: Имя логгера (рекомендуется передавать __name__)
    :param file_path: Путь к файлу логов
    :param config_path: Путь к общему файлу конфигурации YAML
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    cfg = load_config(config_path).get("logging", {})

    # Общий уровень логгера
    root_level = getattr(logging, cfg.get("level", "INFO").upper(), logging.INFO)
    logger.setLevel(root_level)
    logger.propagate = False

    # 1. Настройка вывода в консоль
    console_cfg = cfg.get("console", {})
    if console_cfg.get("enabled", True):
        c_level = getattr(logging, console_cfg.get("level", "INFO").upper(), logging.INFO)
        c_format = console_cfg.get(
            "format", "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )
        c_handler = logging.StreamHandler(sys.stdout)
        c_handler.setLevel(c_level)
        c_handler.setFormatter(logging.Formatter(c_format))
        logger.addHandler(c_handler)

    # 2. Настройка вывода в файл
    file_cfg = cfg.get("file", {})
    if file_cfg.get("enabled", False):
        if file_path:
            log_path = Path(file_path)
        else:
            log_path = Path(file_cfg.get("path", "logs/app.log"))
        log_path.parent.mkdir(parents=True, exist_ok=True)

        f_level = getattr(logging, file_cfg.get("level", "DEBUG").upper(), logging.DEBUG)
        f_format = file_cfg.get(
            "format",
            "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
        )
        max_bytes = file_cfg.get("max_bytes", 10 * 1024 * 1024)

        f_handler = RotatingFileHandler(
            filename=log_path,
            maxBytes=max_bytes,
            encoding="utf-8",
        )
        f_handler.setLevel(f_level)
        f_handler.setFormatter(logging.Formatter(f_format))
        logger.addHandler(f_handler)

    return logger