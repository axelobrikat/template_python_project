"""
Purpose:
    - Python Project Template which includes
      - project structure
      - test stucture using pytest and coverage
      - configured logging, cli input args parsing and exception handling
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
import logging

from src.utils.cli_input_args import CliInputArgs
from src.utils.intl_logger import IntlLogger
from src.utils import exception_handling as exc
from src.vars.pretty_print import SEPARATOR


def main():
    """
    - get and process CLI input args
    - configure logging
    - start program
    - on program exit, log possible exceptions
    """
    # process CLI input args #
    docopt_args: dict = docopt(__doc__)
    CliInputArgs.set_cli_input_args(
        verbose=docopt_args["-v"],
        quiet=docopt_args["-q"],
        hello=docopt_args["--hello"],
    )

    # configure logging #
    root_logger = IntlLogger()
    root_logger.set_verbosity(root_logger.logger)
    root_logger.add_stream_handler()
    root_logger.add_file_handler()

    # rotate logs from previous program execution #
    root_logger.rotating_file_handler.doRollover()
    logging.debug((
        f"Program execution starts.\n"
        f"Logging and Input Arguments configured successfully.\n"
        f"Log rotation of log files '{root_logger.log_file_path}.<x>' performed succesfully.\n"
        f"{SEPARATOR}\n"
        f"{SEPARATOR}\n\n"
    ))
    
    # start program #
    from src.hello_world import hello
    hello()

    # on exit, log catched exceptions as roundup #
    exc.program_end()


if __name__=="__main__":
    main() # pragma: no cover
