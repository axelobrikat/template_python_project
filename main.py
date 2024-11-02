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
    main.py [-v | -q ] [--hello]

Options:
    -v              verbose, increase verbosity to log on DEBUG level (default is WARNING)
    -q              quiet, decrease verbosity to log on ERROR level (default is WARNING)
    --hello         [TEST CASE OF THE TEMPLATE], log "Hello World!"
"""
from docopt import docopt

from src.utils.cli_input_args import CLI
from src.utils.intl_logger import IntlLogger
from src.utils import exception_handling as exc
from src.vars.pretty_print import log_exec_start_msg


def evaluate_cli_input_args():
    """evalute cli input args via docopt
    - save input to class CLI
    """
    docopt_args: dict = docopt(__doc__)
    CLI.set_cli_input_args(
        verbose=docopt_args["-v"],
        quiet=docopt_args["-q"],
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

    # configure logging #
    root_logger = IntlLogger()
    root_logger.set_verbosity(root_logger.logger)
    root_logger.add_stream_handler()
    root_logger.add_file_handler()

    # rotate logs from previous program execution #
    root_logger.rotating_file_handler.doRollover()
    log_exec_start_msg(root_logger.log_file_path)
    
    # start program #
    from src.hello_world import hello
    hello()

    # on exit, log catched exceptions as roundup #
    exc.program_end()


if __name__=="__main__":
    main() # pragma: no cover
