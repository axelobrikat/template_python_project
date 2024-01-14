import pytest
import logging

from src.utils.cli_input_args import CliInputArgs as Args

def hello(): # pragma: no cover
    """log test messages
    """
    if Args.hello:
        logging.debug("Hello World!")
        logging.info("Hello World!")
        logging.warning("Hello World!")
        logging.error("Hello World!")
        logging.critical("Hello World!")
    else:
        logging.warning("This is a Python project template. Use me as a project starter.")
