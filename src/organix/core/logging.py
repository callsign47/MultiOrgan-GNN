"""
ORGANIX Structured Logging Setup.
"""

import logging
import sys
from typing import Optional


def get_logger(name: str = "organix", level: int = logging.INFO) -> logging.Logger:
    """Returns a pre-configured structured logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
