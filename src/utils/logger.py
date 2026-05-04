
import logging
import logging.handlers
from pathlib import Path
from src.config.config import settings


def setup_logger(name: str) -> logging.Logger:
    
    # Create logs directory if it doesn't exist
    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / settings.LOG_FILE
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # File handler - Rotating to prevent huge log files
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file,
        maxBytes=10_000_000,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))
    
    # Formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
