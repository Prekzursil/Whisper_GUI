import logging
from typing import Optional


def get_logger(name: Optional[str] = None):
    if name is None:
        name = "Whisper-WebUI"
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        # handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger