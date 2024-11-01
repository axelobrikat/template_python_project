import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock
from pathlib import Path

from src.log.log import logging
from src.log.log import configure_logger, _get_basic_format, ROOT


@pytest.fixture
def logger():
    """return instance of default internal logger with name 'test-logger'
    NOTE, it is important to not use default 'root' logger, as this contradicts
        .. with pytest logging

    Returns:
        IntlLogger: default internal logger with name 'test-logger'
    """
    return logging.getLogger("test-logger")


def _remove_loggers(logger_names: set):
    """remove loggers by name

    Args:
        logger_names (set): names of loggers to be removed
    """
    for name in logger_names:
        del logging.root.manager.loggerDict[name]


@pytest.fixture(autouse=True)
def tearDown():
    """yield test and tearDown
    - remove all created loggers from testing
    """
    logger_names_inital: set = set(logging.root.manager.loggerDict.keys())

    yield
    
    test_logger_names: set = set(logging.root.manager.loggerDict.keys()) - logger_names_inital
    # same cmd as `diff = set(logging.root.manager.loggerDict.keys()).difference(logger_names_initial)`
    _remove_loggers(test_logger_names)


@pytest.fixture
def mock_stream_handler(mocker: MockerFixture) -> MagicMock:
    """mocks logging.StreamHandler to return a Callable
    - Callable returns instance of logging.StreamHandler with default verbosity WARNING
      - this ensures that the same object can be compared for test assertion

    Args:
        mocker (MockerFixture): pytest MockerFixture

    Returns:
        MagicMock: mocked StreamHandler class
    """
    dummy_handler = logging.StreamHandler(logging.WARNING)

    def __callable__():
        return dummy_handler

    return mocker.patch.object(
        logging,
        "StreamHandler",
        new_callable=lambda: __callable__
    )


def test_configure_logger_defaults(logger: logging.Logger):
    """test configure_logger func when default parameters are used

    Args:
        logger (logging.Logger): Logger object
    """
    logger = configure_logger(logger=logger)

    # assert logger properties #
    assert logger == logging.root.manager.loggerDict["test-logger"]
    assert logger.propagate == False
    assert len(logger.handlers) == 2

    # assert StreamHandler properties #
    has_StreamHandler: bool = any(
        type(handler) == logging.StreamHandler for handler in logger.handlers
    )
    assert has_StreamHandler
    for handler in logger.handlers:
        if type(handler) == logging.StreamHandler:
            assert handler.level == logging.WARNING
            assert handler.formatter._fmt == _get_basic_format()

    # assert RotatingFileHandler properties #
    has_RotatingFileHandler: bool = any(
        type(handler) == logging.handlers.RotatingFileHandler
        for handler in logger.handlers
    )
    assert has_RotatingFileHandler
    for handler in logger.handlers:
        if type(handler) == logging.handlers.RotatingFileHandler:
            assert handler.level == logging.WARNING
            assert handler.formatter._fmt == _get_basic_format()
            assert handler.baseFilename == str(ROOT / "log" / "app.log")


@pytest.mark.parametrize(
    "test_case, ch_level, fh_level, ch_format, fh_format, log_filename, propagate",
    [
        # Test case 1: Different levels, custom filename
        (
            "test case 1",
            logging.INFO,
            logging.ERROR,
            "%(levelname)s - %(message)s",
            "%(name)s - %(message)s",
            "custom_app.log",
            True,
        ),
        # Test case 2: Debug level for both handlers, same format, another filename
        (
            "test case 2",
            logging.DEBUG,
            logging.DEBUG,
            "%(message)s",
            "%(message)s",
            "debug_app.log",
            False,
        ),
        # Test case 3: Info level for console, warning for file, custom format and filename
        (
            "test case 3",
            logging.INFO,
            logging.WARNING,
            "%(asctime)s - %(message)s",
            "%(asctime)s - %(levelname)s - %(message)s",
            "info_warning_app.log",
            True,
        ),
        # Test case 4: Warning level for console, error for file, different format and filename
        (
            "test case 4",
            logging.WARNING,
            logging.ERROR,
            "%(levelname)s: %(message)s",
            "%(asctime)s - %(levelname)s: %(message)s",
            "error_log.log",
            False,
        ),
    ],
)
def test_configure_logger_non_defaults(
    logger: logging.Logger,
    tmp_path: Path,
    test_case: str,
    ch_level: int,
    fh_level: int,
    ch_format: str,
    fh_format: str,
    log_filename: str,
    propagate: bool
):
    """
    Test configure_logger function with non-default parameters and a parameterized log file name.

    Args:
        logger (logging.Logger): Logger object to configure.
        tmp_path (Path): Temporary directory path provided by pytest fixture.
        test_case (str): Identifier for the test case being run.
        ch_level (int): Log level for the console handler (StreamHandler).
        fh_level (int): Log level for the file handler (RotatingFileHandler).
        ch_format (str): Format string for the console handler.
        fh_format (str): Format string for the file handler.
        log_filename (str): Name of the log file for the file handler.
        propagate (bool): Boolean to indicate if logs should propagate to the root logger.
    """
    # Create formatters with the provided format strings
    ch_formatter = logging.Formatter(ch_format)
    fh_formatter = logging.Formatter(fh_format)

    # Use tmp_path and log_filename to create a temporary log file path
    fh_file_path = tmp_path / log_filename

    # Configure logger with non-default parameters
    logger = configure_logger(
        logger=logger,
        ch_level=ch_level,
        ch_formatter=ch_formatter,
        fh_level=fh_level,
        fh_formatter=fh_formatter,
        fh_file_path=fh_file_path,
        propagate=propagate,
    )

    # Assert logger properties
    assert logger.propagate == propagate, \
        f"{test_case}: Expected logger propagate to be {propagate}, but got {logger.propagate}"

    assert len(logger.handlers) == 2, \
        f"{test_case}: Expected 2 handlers, but got {len(logger.handlers)}"

    # Assert StreamHandler properties
    has_StreamHandler = any(
        type(handler) == logging.StreamHandler for handler in logger.handlers
    )
    assert has_StreamHandler, \
        f"{test_case}: Expected StreamHandler not found in logger handlers"

    for handler in logger.handlers:
        if type(handler) == logging.StreamHandler:
            assert handler.level == ch_level, \
                f"{test_case}: Expected StreamHandler level {ch_level}, but got {handler.level}"

            assert handler.formatter._fmt == ch_format, \
                f"{test_case}: Expected StreamHandler format '{ch_format}', but got '{handler.formatter._fmt}'"

    # Assert RotatingFileHandler properties
    has_RotatingFileHandler = any(
        type(handler) == logging.handlers.RotatingFileHandler
        for handler in logger.handlers
    )
    assert has_RotatingFileHandler, \
        f"{test_case}: Expected RotatingFileHandler not found in logger handlers"

    for handler in logger.handlers:
        if type(handler) == logging.handlers.RotatingFileHandler:
            assert handler.level == fh_level, \
                f"{test_case}: Expected RotatingFileHandler level {fh_level}, but got {handler.level}"

            assert handler.formatter._fmt == fh_format, \
                f"{test_case}: Expected RotatingFileHandler format '{fh_format}', but got '{handler.formatter._fmt}'"

            assert handler.baseFilename == str(fh_file_path), \
                f"{test_case}: Expected RotatingFileHandler file path '{fh_file_path}', but got '{handler.baseFilename}'"
