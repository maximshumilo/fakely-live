import logging
import time
from typing import Callable


_LOG_FORMAT: str = "%(asctime)s %(name)-15s %(levelname)-8s %(message)s"


def get_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """Get logger and set a specific formatter."""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter(_LOG_FORMAT)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
