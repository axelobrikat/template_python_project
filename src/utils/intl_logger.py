import logging
from pathlib import Path

from src.utils.cli_input_args import CliInputArgs
from src.vars.paths import ROOT
from src.utils import exception_handling as exc


class IntlLogger():
    """internal class for configuring logging
    """
    logger_names = []
    """Saves unique names of already configured internal logger instances."""

    def __new__(
            cls,
            logger_name: str = "root",
            format: str = '',
        ):
        """check that created InstLogger instances have unique names
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
        self.name: str = logger_name
        IntlLogger.logger_names.append(self.name)
        self.logger: logging.Logger = logging.getLogger(self.name)
        self.verbose: bool = False
        self.quiet: bool = False
        self.format: str =  format

    def __str__(self) -> str:
        return f"This is the internal IntlLogger: '{self.name}'."
    
    def set_verbosity(self, manager: logging.Handler | logging.Logger):
        """set verbosity of handler dependant on cli input args -v and -q
        - if both -v and -q are false, then default level is WARNING
        """
        if CliInputArgs.verbose:
            manager.setLevel(logging.DEBUG)
        elif CliInputArgs.quiet:
            manager.setLevel(logging.ERROR)
        else:
            manager.setLevel(logging.WARNING)

    def configure_and_add_handler(self, handler: logging.Handler):
        """configure and add a new handler to self.logger

        Args:
            handler (logging.Handler): handler
        """
        # set verbosity level #
        self.set_verbosity(handler)

        # set format of handler #
        handler.setFormatter(logging.Formatter(self.format))

        # add handler to logger #
        self.logger.addHandler(handler)

    def add_stream_handler(self):
        """add a StreamHandler for logging to console
        """ 
        self.configure_and_add_handler(logging.StreamHandler())

    def add_file_handler(self, file: Path = ROOT / "log" / "app.log"):
        """add a FileHandler for logging to a file
        - NOTE, when app is executed, old logs get deleted

        Args:
            file (Path, optional): path to log file. Defaults to ROOT/"log"/"app.log".
        """
        self.configure_and_add_handler(logging.FileHandler(str(file), mode="w"))
