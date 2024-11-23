import logging

from src.utils.cli_input_args import CLI
from src.log.log import configure_logger


logger = logging.getLogger(__name__)
logger = configure_logger(logger)


def hello(): # pragma: no cover
    """log test messages
    """
    if CLI.hello:
        logger.debug("Hello World!")
        logger.info("Hello World!")
        logger.warning("Hello World!")
        logger.error("Hello World!")
        logger.critical("Hello World!")
    else:
        logger.warning("This is a Python project template. Use me as a project starter.")
