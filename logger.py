import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "broccoliflow.log"

def setup_logger(debug=False):
    """Initializes and configures the global logger."""
    LOG_DIR.mkdir(exist_ok=True)
    
    app_logger = logging.getLogger("BroccoliFlow")
    
    #set level based on debug toggle
    level = logging.DEBUG if debug else logging.INFO
    app_logger.setLevel(level)
    
    #prevent duplicate handlers
    if not app_logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        app_logger.addHandler(file_handler)
        
    return app_logger

#initialize global instance
logger = setup_logger(debug=False)

def set_debug_level(debug):
    """Dynamically changes the logging level at runtime."""
    logger.setLevel(logging.DEBUG if debug else logging.INFO)