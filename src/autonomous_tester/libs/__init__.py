"""Initialization for libs module."""


from .common.logger import logger
from .common.decorators import singleton
from .common.config import Settings


@singleton
def get_settings() -> Settings:
    """Get settings for the autonomous tester."""
    return Settings()

settings = get_settings()


__all__ = [
    "logger",
    "settings",
]
