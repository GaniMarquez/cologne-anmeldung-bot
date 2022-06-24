from distutils.util import strtobool

import os
import logging

from dotenv import load_dotenv


load_dotenv(".env")

# General Configs
DEBUG: bool = bool(strtobool(os.getenv("DEBUG", "False")))
TELEGRAM_API_TOKEN: str = os.getenv("TELEGRAM_API_TOKEN")
SCRAPER_BASE_URL: str = os.getenv("SCRAPER_BASE_URL")
SCRAPER_UID: str = os.getenv("SCRAPER_UID")
SCRAPER_SEARCH_MODE = os.getenv("SCRAPER_SEARCH_MODE", "earliest")

# Logging Specific Configs
_logging_levels = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}
LOGGING_LEVEL = _logging_levels.get(
    os.getenv("LOGGING_LEVEL", "INFO").upper(),
    logging.INFO,
)