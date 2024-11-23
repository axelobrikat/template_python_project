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

logging.basicConfig(level=logging.NOTSET)
"""
This sets the root logger to write to stdout (your console).
Your script/app needs to call this somewhere at least once.
By default the root logger is set to WARNING and all loggers you define
inherit that value. Here we set the root logger to NOTSET. This logging
level is automatically inherited by all existing and new sub-loggers
that do not set a less verbose level.
"""

# only import modules that do not include custom logging, #
# as custom logging has not been configured yet #
from src.utils.cli_input_args import CLI
from src.log import log


def _evaluate_cli_input_args():
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


if __name__=="__main__":
    """setup program
    """
    # process CLI input args #
    _evaluate_cli_input_args()

    # write log level to log.conf file #
    log.write_log_level(CLI.get_wanted_log_level())


# configure logger #
logger: logging.Logger = logging.getLogger(__name__)
logger = log.configure_logger(logger)


from src.vars.pretty_print import SEPARATOR
from src.utils import exception_handling as exc
from src.hello_world import hello


def main():
    """
    - rotate logs
    - start program
    - on program exit, log possible exceptions
    """
    # rotate logs #
    # TODO: fix: logs are not saved in app.log but already in app.log.1 #
    log.rotate_logs_of_all_rotating_file_handlers(logger)

    # log debug msg for program start #
    logger.debug((
        f"Program execution starts.\n"
        f"Logging and Input Arguments configured successfully.\n"
        f"{SEPARATOR}\n"
        f"{SEPARATOR}\n\n"
    ))

    # start program #
    hello()

    # on exit, log catched exceptions as roundup #
    exc.program_end()


if __name__=="__main__":
    """call main
    """
    main() # pragma: no cover
