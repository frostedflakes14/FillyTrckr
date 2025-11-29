"""Common logging configuration for FillyTrckr application.

Provides a configured logger object that writes to console and log file with proper formatting.
"""

import logging
import sys
from pathlib import Path


# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE = LOGS_DIR / "fillytrckr.log"


def get_logger(name: str = "FillyTrckr", level: int = logging.INFO) -> logging.Logger:
    """Get or create a configured logger instance.

    Args:
        name: Name of the logger (typically __name__ of the calling module)
        level: Logging level (default: INFO)

    Returns:
        Configured logger object
    """
    logger = logging.getLogger(name)

    # Only configure if not already configured (avoid duplicate handlers)
    if not logger.handlers:
        logger.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)

        # Create file handler
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


# Default logger instance
logger = get_logger()