import logging


_LOG_FORMAT: str = "%(asctime)s %(name)-15s %(levelname)-8s %(message)s"


def get_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """Get logger and set a specific formatter.

    Args:
        name: The name of the logger.
        level: The logging level (default: DEBUG).

    Returns
    -------
        A configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter(_LOG_FORMAT)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
