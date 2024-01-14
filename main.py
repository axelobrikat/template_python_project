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
    --hello         [TEST CASE], log "Hello World!"
"""
from docopt import docopt

from src.utils.cli_input_args import CliInputArgs
from src.utils.intl_logger import IntlLogger
from src.utils import exception_handling as exc


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
    
    # start program #
    from src.hello_world import hello
    hello()

    # on exit, log catched exceptions as roundup #
    exc.program_end()


if __name__=="__main__":
    main() # pragma: no cover
