import logging
from pathlib import Path

from src.utils.cli_input_args import CliInputArgs
from src.vars.paths import ROOT


class Logger():
    """internal class for configuring logging
    """
    def __init__(
            self,
            logger_name: str = "",
            format: str = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        ) -> None:
        self.name: str = logger_name
        self.logger: logging.Logger = logging.getLogger(self.name)
        self.verbose: bool = False
        self.quiet: bool = False
        self.format: str =  format

    def __str__(self) -> str:
        return f"This is the internal logger: '{self.name}'."
    
    def set_verbosity(self, handler: logging.Handler):
        """set verbosity of handler dependant on cli input args -v and -q
        - if both -v and -q are false, then default level is WARNING
        """
        if CliInputArgs.verbose:
            handler.setLevel(logging.DEBUG)
        elif CliInputArgs.quiet:
            handler.setLevel(logging.ERROR)

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
