import logging

from app.core.config import settings

def setup_logging():
    log_level = settings.LOG_LEVEL.upper()
    # Map TRACE to DEBUG as python logging doesn't have TRACE by default
    if log_level == "TRACE":
        level = logging.DEBUG
    else:
        level = getattr(logging, log_level, logging.INFO)

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # You can add more advanced logging setup here (e.g., file handlers, JSON formatting)
