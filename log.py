import sys
import logging

from loguru import logger

import config


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def format_record(record: dict) -> str:
    format_string = (
        "<green>[{time:YYYY-MM-DD HH:mm:ss.SSS}]</green> "
        + "<level>[{level: <8}]</level> "
        + "<cyan>[{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}]</cyan> "
    )

    if record["extra"].get("info") is not None:
        for key, value in record["extra"]["info"].items():
            if value:
                format_string += f"<yellow>[{key}:{{extra[info][{key}]}}]</yellow> "

    format_string += "- <white><level>{message}</level></white>"
    format_string += "{exception}\n"

    return format_string


def setup_logging():
    intercept_handler = InterceptHandler()

    # Intercept Root Logger
    logging.basicConfig(handlers=[intercept_handler])
    logging.getLogger().handlers = [intercept_handler]

    logger.configure(
        handlers=[
            {
                "sink": sys.stderr if config.DEBUG else sys.stdout,
                "level": config.LOGGING_LEVEL,
                "format": format_record,
                "colorize": True if config.DEBUG else False,
                "diagnose": True if config.DEBUG else False,
            }
        ]
    )
    logger.info("Successfully set-up logging.")
