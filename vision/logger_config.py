import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name="PlanExecutor", log_file="logs/executor.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.hasHandlers():
        handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s", "%H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
