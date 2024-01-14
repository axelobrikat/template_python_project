"""
Purpose:
    - Python Project Template which includes
      - project structure
      - test stucture using pytest and coverage
      - configured logging, arg parsing and exception handling
      - .gitignore
      - LICENSE
      - README.md
      - requirements.txt

Usage:
    main.py [-v | -q ] [--hello]

Options:
    -v              verbose, increase verbosity to log on DEBUG level (default is WARNING)
    -q              quiet, decrease verbosity to log on ERROR level (default is WARNING)
    --hello         log "Hello World!" (test case)
"""
from docopt import docopt

from src.utils.cli_input_args import CliInputArgs
from src.utils.intl_logger import IntlLogger


def main():
    """
    - get and process CLI input args
    - configure logging
    - start program
    - on program exit, log possible exceptions
    """
    # process CLI input args #
    CliInputArgs.set_cli_input_args(docopt(__doc__))

    # configure logging #
    root_logger = IntlLogger()
    root_logger.set_verbosity(root_logger.logger)
    root_logger.add_stream_handler()
    root_logger.add_file_handler()
    
    # enter program #
    import logging
    logging.debug("Hello World!")
    logging.info("Hello World!")
    logging.warning("Hello World!")
    logging.error("Hello World!")
    logging.critical("Hello World!")

    # on exit, log exceptions #


if __name__=="__main__":
    main() # pragma: no cover
