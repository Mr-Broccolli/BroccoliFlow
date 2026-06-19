import logging
import logging.handlers
from pathlib import Path
from typing import Union

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "broccoliflow.log"

def setup_logger(debug: bool = False):
    """Initializes and configures the global logger with rotation and optional console output."""
    app_logger = logging.getLogger("BroccoliFlow")

    #set level based on debug toggle
    level = logging.DEBUG if debug else logging.INFO
    app_logger.setLevel(level)

    #prevent duplicate handlers
    if not app_logger.handlers:
        # File handler with rotation (5 MB per file, keep 5 backups)
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE, maxBytes=5*1024*1024, backupCount=5, encoding='utf-8'
        )
        file_formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(module)s:%(lineno)d | %(funcName)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        app_logger.addHandler(file_handler)

        # Console handler for debug mode (prints to stderr)
        if debug:
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                fmt="%(levelname)s: %(message)s"
            )
            console_handler.setFormatter(console_formatter)
            app_logger.addHandler(console_handler)

    return app_logger

#initialize global instance
logger = setup_logger(debug=False)

def set_debug_level(debug: bool) -> None:
    """Dynamically changes the logging level at runtime."""
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    # Update handlers levels and ensure console handler present/absent as needed
    # Remove any existing console handlers (StreamHandler writing to stderr) if debug=False
    if not debug:
        # Remove console handlers
        for handler in list(logger.handlers):
            if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                logger.removeHandler(handler)
    else:
        # Add console handler if not already present
        has_console = any(isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler) for h in logger.handlers)
        if not has_console:
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                fmt="%(levelname)s: %(message)s"
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
    # Update levels of all handlers to match logger level
    for handler in logger.handlers:
        handler.setLevel(logger.level)