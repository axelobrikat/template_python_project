"""
module to handle logging
- this is also used for configuring the main logger of the app
  - therefore, this module cannot log 'normally', but must raise issues instantly
  - TODO: rework this structure - app should not break if any logger cannot find log.conf etc.
    - logging should be usable, but not custom logger
    - NOTE, this module should not include custom logging (for info, see main.py).
"""
import logging
import logging.handlers
from pathlib import Path
import re

from src.vars.paths import ROOT


def _check_path_existence(path: Path):
    """check if path exists
    - if it does not, then raise FileNotFoundError

    Args:
        path (Path): file or dir path

    Raises:
        FileNotFoundError: if path does not exist, raise
    """
    if not path.exists():
        raise FileNotFoundError(f"File '{path}' does not exist.")


def _get_log_level(log_conf_path: Path = ROOT / "src" / "log" / "log.conf") -> int:
    r"""return log level that is stored in file
    - pattern: "^log_level:\s*(\w+)$", e.g. "log_level: WARNING"

    Args:
        log_conf_path (Path, optional): Path to log.conf file. Defaults to ROOT/"src"/"log"/"log.conf".

    Raises:
        ValueError: raise if logging cannot be configured
        FileNotFoundError: raise if log.conf file cannot be found

    Returns:
        int: log level
    """
    _check_path_existence(log_conf_path)
    with open(log_conf_path) as f:
        content: str = f.read()

    # Use regex to find the log level from the file content
    pattern: str = r'^log_level:\s*(\w+)'
    m: re.Match = re.search(pattern, content)

    if m:
        # Extract the log level string from the match
        log_level_str: str = m.group(1)
        # Convert the log level string to the corresponding logging level integer
        log_level = getattr(logging, log_level_str.upper(), None)

        if isinstance(log_level, int):
            return log_level
        else:
            raise ValueError(
                f"Cannot configure logging. Invalid log level: '{log_level_str}'. "
                f"Only levels from Python's 'logging' library are valid."
            )

    raise ValueError(
        "Cannot configure logging. Log level cannot be determined from log.conf file."
    )


def write_log_level(log_level: int) -> None:
    """Update the log level in log.conf to the provided log level.
    - do this by overwriting the whole file with the updated content
    - TODO:
      - log.conf should not be overwritten
      - instead check if cli logging option is passed
        - if yes, then create a tmp log.conf file in tmp folder
        - if not, then use the default log.conf file
      - in both cases, log if the log level was taken from log.conf or cli

    Args:
        log_level (int): New log level as an integer (e.g., logging.WARNING, logging.INFO).

    Raises:
        FileNotFoundError: If the log.conf file does not exist.
    """
    # Validate that the provided log_level is a valid logging level name
    log_level_name = logging.getLevelName(log_level)
    if not isinstance(log_level_name, str) or log_level_name == f"Level {log_level}":
        raise ValueError(
            f"Cannot configure logging. Invalid log level: {log_level} of type {log_level}."
        )

    # Define the path to log.conf
    log_conf_path = ROOT / "src" / "log" / "log.conf"
    _check_path_existence(log_conf_path)

    # Read, modify, and overwrite the file content
    with open(log_conf_path, mode='r+') as f:
        # read content #
        content = f.read()
        # set pointer to file start #
        f.seek(0)
        # substitute log level #
        f.write(re.sub(
            r"^log_level:\s*\w+",
            f"log_level: {log_level_name}",
            content,
            flags=re.MULTILINE,
        ))
        # truncate at the end #
        f.truncate()


def rotate_logs_of_all_rotating_file_handlers(logger: logging.Logger) -> None:
    """
    rotate log files of all RotatingFileHandlers of passed logger instance
    - only if the file is not empty

    Args:
        logger (logging.Logger): logger instance
    """
    for h in logger.handlers:
        if type(h) == logging.handlers.RotatingFileHandler \
        and Path(h.baseFilename).stat().st_size != 0:
            h.doRollover()


def _get_basic_format() -> str:
    """return basic logging format of program

    Returns:
        str: basic logging format
    """
    return '%(asctime)s [%(levelname)-8s] %(name)s: %(message)s'


def _get_configured_handler(
        handler: logging.Handler, level: int, formatter: logging.Formatter
    ) -> logging.Handler:
    """create and return a configured handler

    Args:
        handler (logging.Handler): handler
        level (int): log level
        formatter (logging.Formatter): Formatter object
    """
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


def configure_logger(
        logger: logging.Logger,
        ch_level: int = -1,
        ch_formatter: logging.Formatter = logging.Formatter(_get_basic_format()),
        fh_level: int = -1,
        fh_formatter: logging.Formatter = logging.Formatter(_get_basic_format()),
        fh_file_path: Path = ROOT / "log" / "app.log",
        propagate: bool = False,
    ) -> logging.Logger:
    """configure logger object

    Args:
        logger (logging.Logger): logger
        ch_level (int): log level for console handler (ch). Defaults to -1
            ...indicating that default value from log.conf should be used.
        ch_formatter (logging.Formatter): formatter for console handler (ch). Defaults to 
            ...logging.Formaterr using interal default format
        fh_level (int): log level for file handler (fh). Defaults to -1
            ...indicating that default value from log.conf should be used.
        fh_formatter (logging.Formatter): formatter for file handler (fh). Defaults to 
            ...logging.Formaterr using interal default format
        fh_file_path (Path): path to log file. Defaults to project's log.conf file path.
        propagate (bool): decides if logs should be propoagated to root logger. Defaults to False.

    Returns:
        logging.Logger: configured logger object
    """
    # Check if default log level should be used #
    if ch_level == -1:
        ch_level = _get_log_level()
    if fh_level == -1:
        fh_level = _get_log_level()

    # Ensure the logger does not propagate messages to the root logger
    logger.propagate = propagate

    # add console handler #
    logger.addHandler(_get_configured_handler(logging.StreamHandler(), ch_level, ch_formatter))

    # add rotating file handler #
    rotating_fh: logging.handlers.RotatingFileHandler = logging.handlers.RotatingFileHandler(
            fh_file_path,
            mode="a",
            maxBytes=100*1024*1024,
            backupCount=10,
    )
    logger.addHandler(_get_configured_handler(rotating_fh, fh_level, fh_formatter))

    # return configured logger #
    return logger
