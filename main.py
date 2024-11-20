"""
Purpose:
    - Python Project Template which includes
      - project structure
      - test stucture using pytest and coverage
      - configured logging (logrotate), cli input args parsing and exception handling
      - .gitignore
      - LICENSE
      - README.md
      - requirements.txt

Usage:
    main.py [ -V | -v | -q | -Q ] [--hello]

Options:
    -v              verbose, increase verbosity to log on INFO level (default is WARNING)
    -V              more verbose, increase verbosity to log on DEBUG level (default is WARNING)
    -q              quiet, decrease verbosity to log on ERROR level (default is WARNING)
    -Q              more quiet, decrease verbosity to log on EXCEPTION level (default is WARNING)
    --hello         [TEST CASE OF THE TEMPLATE], log "Hello World!"
"""
from docopt import docopt
import logging
import logging.handlers

from src.utils.cli_input_args import CLI
from src.log import log
from src.utils import exception_handling as exc
from src.vars.pretty_print import SEPARATOR


def evaluate_cli_input_args():
    """evalute cli input args via docopt
    - save input to class CLI
    """
    docopt_args: dict = docopt(__doc__)
    CLI.set_cli_input_args(
        v=docopt_args["-v"],
        V=docopt_args["-V"],
        q=docopt_args["-q"],
        Q=docopt_args["-Q"],
        hello=docopt_args["--hello"],
    )


def main():
    """
    - get and process CLI input args
    - configure logging
    - start program
    - on program exit, log possible exceptions
    """
    # process CLI input args #
    evaluate_cli_input_args()

    # write log level to log.conf file #
    log.write_log_level(CLI.get_wanted_log_level())

    # configure logger #
    logger: logging.Logger = logging.getLogger(__name__)
    logger = log.configure_logger(logger)
    log.rotate_logs_of_all_rotating_file_handlers(logger)

    # log debug msg for program start #
    logger.debug((
        f"Program execution starts.\n"
        f"Logging and Input Arguments configured successfully.\n"
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
