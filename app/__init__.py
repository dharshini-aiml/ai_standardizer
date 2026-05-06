"""Data Standardization API - Initialize application package."""
__version__ = "1.0.0"
__author__ = "Data Standardization Team"
__description__ = "Data Standardization and Schema Mapping Agent"

from app.config import settings
from app.utils.logger import logger

logger.info(f"Initializing {__description__} v{__version__}")
