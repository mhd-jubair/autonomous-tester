"""Logger module for the autonomous tester."""

import logging
import sys

logger = logging.getLogger("my_app_logger")
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("app.log")

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
