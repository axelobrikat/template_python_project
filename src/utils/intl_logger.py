"""
TODO:
- impemented way of logging is too complicated
- just follow the cook book on https://docs.python.org/3/howto/logging.html
- use Logger class and getLogger func for different loggers
- use --log cli option for passing loglevel
- start every module with
  ```
  import logging
  logger = logging.getLogger() # OR logging.getLogger(__name__)
  ```
- include the test in each module to check if the correct logger is used
  - if this does not contradict with pytest's internal logging
"""
import logging
import logging.handlers
from pathlib import Path

from src.utils.cli_input_args import CliInputArgs
from src.vars.paths import ROOT
from src.utils import exception_handling as exc


class IntlLogger():
    """internal class for configuring logging
    """
    logger_names = []
    """Saves unique names of already configured internal logger instances."""

    log_file_path: Path = ROOT / "log" / "app.log"
    """Path to logging file"""

    rotating_file_handler: logging.handlers.RotatingFileHandler = logging.handlers.RotatingFileHandler(
            log_file_path,
            mode="a",
            maxBytes=100*1024*1024,
            backupCount=5,
    )
    """RotatingFileHanlder that handles all logs to file"""

    def __new__(
            cls,
            logger_name: str = "root",
            format: str = '',
        ):
        """check that created IntlLogger instances have unique names
        - exit program, if InstLogger instance with same name already exists

        Args:
            logger_name (str, optional): logger name. Defaults to "root".
            format (str, optional): logging format (not used in this method). Defaults to ''.

        Returns:
            Self: instance of class, if no exception to exit program occured
        """
        if logger_name in cls.logger_names:
            exc.raise_exception(
                f"{cls.__name__} '{logger_name}' has already been instantiated and configured before."
                f" {cls.__name__} instances must have unique names."
                f" Access the existing logger of {cls.__name__} via `logging.getLogger(\"{logger_name}\")`."
            )
        return super().__new__(cls)


    def __init__(
            self,
            logger_name: str = "root",
            format: str = '%(asctime)s [%(levelname)-8s] %(name)s: %(message)s',
        ) -> None:
        """init

        Args:
            logger_name (str, optional): name of logger. Defaults to "root".
            format (str, optional): logging format. Defaults to '%(asctime)s [%(levelname)-8s] %(name)s: %(message)s'.
        """
        self.name: str = logger_name
        IntlLogger.logger_names.append(self.name)
        self.logger: logging.Logger = logging.getLogger(self.name)
        self.format: str =  format


    def __str__(self) -> str:
        return f"This is the internal IntlLogger: '{self.name}'."
    

    def set_verbosity(self, manager: logging.Handler | logging.Logger):
        """set verbosity of handler
        - for 'root' logger, it is dependant on cli input args -v (DEBUG) and -q (ERROR)
        - default level is WARNING for all loggers
        - at the moment, other loggers than "root" are not configurable
        TODO: 
          - must be more general
          - only use CliInputArgs when "root" logger is meant
          - otherwise, provide func params
        """
        if self.name == "root":
            if CliInputArgs.verbose:
                manager.setLevel(logging.DEBUG)
                return
            elif CliInputArgs.quiet:
                manager.setLevel(logging.ERROR)
                return

        # set default level -> WARNING #
        # at the moment, other loggers than "root" are not configurable #
        manager.setLevel(logging.WARNING)


    def _configure_and_add_handler(self, handler: logging.Handler):
        """configure and add a new handler to self.logger

        Args:
            handler (logging.Handler): handler
        """
        # Ensure the logger does not propagate messages to the root logger
        self.logger.propagate = False

        # set verbosity level #
        self.set_verbosity(handler)

        # set format of handler #
        handler.setFormatter(logging.Formatter(self.format))

        # add handler to logger #
        self.logger.addHandler(handler)


    def add_stream_handler(self):
        """add a StreamHandler for logging to console
        """ 
        self._configure_and_add_handler(logging.StreamHandler())


    def add_file_handler(self):
        """add a log-rotating FileHandler for logging to a file
        """
        self._configure_and_add_handler(IntlLogger.rotating_file_handler)
