####################################################
#                                                  #
#          src/snippets/logging/logging.py
#                                                  #
####################################################
# Created by: Chad Lowe                            #
# Created on: 2022-10-31T08:12:18-07:00            #
# Last Modified: 2022-12-04T01:11:10.071840+00:00  #
# Source: https://github.com/DonalChilde/snippets  #
####################################################
"""
Convenience functions for logging.

"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

DEFAULT_FORMAT = (
    "%(asctime)s %(levelname)s:%(funcName)s: %(message)s [in %(pathname)s:%(lineno)d]"
)


def rotating_file_handler(
    log_dir: Path,
    file_name: str,
    log_level: int,
    formater: logging.Formatter | None = None,
) -> RotatingFileHandler:
    """
    Convenience function to init a rotating file handler.

    Ensures log directory exists, and enforces .log file suffix.
    If no format string is provided, uses a default format.

    Args:
        log_dir: The log directory.
        file_name: The name of the log file, without suffix.
        log_level: The log level
        format_string: The format string for the log message. Defaults to None.

    Returns:
        RotatingFileHandler: The confgured RotatingFileHandler.
    """

    log_dir.mkdir(parents=True, exist_ok=True)
    if file_name.endswith(".log"):
        log_file = log_dir / Path(file_name)
    else:
        log_file = log_dir / Path(f"{file_name}.log")
    handler = RotatingFileHandler(log_file, maxBytes=102400, backupCount=10)
    if formater is None:
        formater = logging.Formatter(fmt=DEFAULT_FORMAT)
    handler.setFormatter(fmt=formater)
    handler.setLevel(log_level)
    return handler


def rotating_file_logger(
    logger_name: str,
    log_dir: Path,
    log_level: int,
    logfile_name: str | None = None,
    formater: logging.Formatter | None = None,
):
    """
    Configures a logger with a rotating file handler.

    Convenience method with useful defaults.

    Args:
        log_dir: The log directory.
        log_name: The name of the logger.
        log_level: The log level.

    Returns:
        The logger.
    """
    logger_ = logging.getLogger(logger_name)
    if logfile_name is None:
        logfile_name = logger_name
    handler = rotating_file_handler(
        log_dir=log_dir, file_name=logfile_name, log_level=log_level, formater=formater
    )
    logger_.addHandler(handler)
    logger_.setLevel(log_level)
    logger_.info("Rotating file logger initialized with %r", handler)
    return logger_


def add_handlers_to_target_logger_by_name(
    source_logger: logging.Logger, target_logger_name: str
):
    """Add the handlers of one logger to another logger, by logger name.

    Do this to enable logging for libraries, presumed to have a nullhandler.
    target_object.__module__.__name__
    """
    target_logger = logging.getLogger(target_logger_name)
    for handler in source_logger.handlers:
        source_logger.info(
            "Attempting to add %s from %s to %s", handler, source_logger, target_logger
        )
        target_logger.addHandler(handler)
    target_logger.info("Added handlers from %s to %s", source_logger, target_logger)


def add_handlers_to_target_logger(
    source_logger: logging.Logger, target_logger: logging.Logger
):
    """Add the handlers of one logger to another logger.

    Do this to enable logging for libraries, presumed to have a nullhandler.
    target_object.__module__.__name__
    """
    for handler in source_logger.handlers:
        source_logger.info(
            "Attempting to add %s from %s to %s", handler, source_logger, target_logger
        )
        target_logger.addHandler(handler)
    target_logger.info("Added handlers from %s to %s", source_logger, target_logger)
