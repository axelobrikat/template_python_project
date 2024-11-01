"""
module to handle logging
"""
import logging
import logging.handlers
from pathlib import Path

from src.vars.paths import ROOT


def _get_basic_format() -> str:
    """return basic logging format of program

    Returns:
        str: basic logging format
    """
    return '%(asctime)s [%(levelname)-8s] %(name)s: %(message)s'


def _get_configured_handler(handler: logging.Handler, level: int, formatter: logging.Formatter):
    """create and return a configured handler

    Args:
        handler (logging.Handler): handler
    """
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler



def configure_logger(
    logger: logging.Logger,
    ch_level: int = logging.WARNING,
    ch_formatter: logging.Formatter = logging.Formatter(_get_basic_format()),
    fh_level: int = logging.WARNING,
    fh_formatter: logging.Formatter = logging.Formatter(_get_basic_format()),
    fh_file_path: Path = ROOT / "log" / "app.log",
    propagate: bool = False,
) -> logging.Logger:
    """configure logger object

    Args:
        logger (logging.Logger): logger
        ch_level (int): log level for console handler (ch)
        ch_formatter (logging.Formatter): formatter for console handler (ch)
        fh_level (int): log level for file handler (fh)
        fh_formatter (logging.Formatter): formatter for file handler (fh)
        fh_file_path (Path): path to log file
        propagate (bool): decides if logs should be propoagated to root logger

    Returns:
        logging.Logger: configured logger object
    """
    # Ensure the logger does not propagate messages to the root logger
    logger.propagate = propagate

    # add console handler #
    logger.addHandler(_get_configured_handler(logging.StreamHandler(), ch_level, ch_formatter))

    # add rotating file handler #
    rotating_fh: logging.handlers.RotatingFileHandler = logging.handlers.RotatingFileHandler(
            fh_file_path,
            mode="a",
            maxBytes=100*1024*1024,
            backupCount=10,
    )
    logger.addHandler(_get_configured_handler(rotating_fh, fh_level, fh_formatter))

    # return configured logger #
    return logger
