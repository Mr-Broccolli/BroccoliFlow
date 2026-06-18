import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "broccoliflow.log"

def setup_logger(debug=False):
    LOG_DIR.mkdir(exist_ok=True)
    
    logger = logging.getLogger("BroccoliFlow")
    
    # Set level based on debug toggle
    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)
    
    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

logger = setup_logger(debug=False)
# Add this function to logger.py
def set_debug_level(debug):
    logger.setLevel(logging.DEBUG if debug else logging.INFO)