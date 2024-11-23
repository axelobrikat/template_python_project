import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock
from pathlib import Path
import shutil

from src.log.log import logging
from src.log import log


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



@pytest.mark.parametrize(
    "test_case, log_level_str, expected_log_level",
    [
        ("test case 1:", "CRITICAL", logging.CRITICAL),
        ("test case 2:", "FATAL", logging.FATAL),
        ("test case 3:", "ERROR", logging.ERROR),
        ("test case 4:", "WARNING", logging.WARNING),
        ("test case 5:", "WARN", logging.WARN),
        ("test case 6:", "INFO", logging.INFO),
        ("test case 7:", "DEBUG", logging.DEBUG),
        ("test case 8:", "NOTSET", logging.NOTSET),
    ]
)
def test__get_log_level_success(
        tmp_path: Path, test_case: str, log_level_str: str, expected_log_level: int
    ) -> None:
    """
    Test _get_log_level function for expected log level values when valid log levels are provided.

    Args:
        tmp_path (Path): Temporary directory provided by pytest to create a mock log.conf file.
        test_case (str): test case name of the parametrized test func
        log_level_str (str): Log level name to write to the mock log.conf file (e.g., "WARNING").
        expected_log_level (int): Expected integer value for the log level based on Python's logging library.
  """

    # Create a temporary log.conf file with the log_level we want to test
    log_conf_path = tmp_path / "log.conf"
    log_conf_path.write_text(f"log_level: {log_level_str}")

    # Run the function and check that it returns the expected log level
    log_level = log._get_log_level(log_conf_path)
    assert log_level == expected_log_level, \
        f"{test_case}, failed. Expected {expected_log_level}, but got {log_level}"
    


def test__get_log_level_FileNotFoundError(tmp_path: Path):
    """test _get_log_level function for FileNotFoundError

    Args:
        tmp_path (Path): Temporary directory provided by pytest to create a mock log.conf file.
    """
    not_existing_path: Path = tmp_path / "not" / "existing" / "path"
    exp_exc_msg: str = fr"File '{not_existing_path}' does not exist."
    
    with pytest.raises(FileNotFoundError, match=exp_exc_msg):
        log._get_log_level(not_existing_path)



@pytest.mark.parametrize(
    "file_content, exp_err_msg",
    [
        ("log_level: INVALID_LEVEL", "Cannot configure logging. Invalid log level: 'INVALID_LEVEL'."),  # Case 1
        ("some_other_config: INFO", "Cannot configure logging. Log level cannot be determined from log.conf file.")  # Case 2
    ]
)
def test__get_log_level_ValueError(tmp_path: Path, file_content: str, exp_err_msg: str) -> None:
    """Test _get_log_level function raises ValueError for invalid or missing log levels.

    Args:
        tmp_path (Path): Temporary directory provided by pytest to create a mock log.conf file.
        file_content (str): Content to write in the mock log.conf file for testing error conditions.
        exp_err_msg (str): Expected error message substring for ValueError.
    """
    # Create a temporary log.conf file with the specified content
    log_conf_path = tmp_path / "log.conf"
    log_conf_path.write_text(file_content)

    # Check that ValueError is raised with the expected error message
    with pytest.raises(ValueError, match=exp_err_msg):
        log._get_log_level(log_conf_path)



@pytest.mark.parametrize(
    "test_case, log_level_str, expected_log_level",
    [
        ("test case 1:", "CRITICAL", logging.CRITICAL),
        ("test case 3:", "ERROR", logging.ERROR),
        ("test case 4:", "WARNING", logging.WARNING),
        ("test case 6:", "INFO", logging.INFO),
        ("test case 7:", "DEBUG", logging.DEBUG),
        ("test case 8:", "NOTSET", logging.NOTSET),
    ]
)
def test_write_log_level_success(
        tmp_path: Path,
        mocker: MockerFixture,
        test_case: str,
        log_level_str: str,
        expected_log_level: int,
    ) -> None:
    """
    Test write_log_level function for expected log level values when valid log levels are provided.

    Args:
        tmp_path (Path): Temporary directory provided by pytest to create a mock log.conf file.
        mocker (MockerFixture): pytest MockerFixture
        test_case (str): Test case name of the parametrized test function.
        log_level_str (str): Log level name to write to the mock log.conf file (e.g., "WARNING").
        expected_log_level (int): Expected integer value for the log level based on Python's logging library.
    """
    # Create a temporary log.conf file with the same content as project's log.conf file #
    log_conf_path = tmp_path / "src" / "log" / "log.conf"
    log_conf_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(Path(log.ROOT / "src" / "log" / "log.conf"), log_conf_path)

    # patch ROOT var #
    mocker.patch.object(
        log,
        "ROOT",
        tmp_path
    )

    # Run the function to update the log level
    log.write_log_level(expected_log_level)

    # Check if the file content has the expected log level
    updated_content = log_conf_path.read_text()
    assert f"log_level: {log_level_str}" in updated_content, \
        f"{test_case} failed. Expected 'log_level: {log_level_str}', but got {updated_content}"



def test_write_log_level_ValueError(tmp_path: Path, mocker: MockerFixture) -> None:
    """Test write_log_level function raises ValueError for invalid log level.

    Args:
        tmp_path (Path): Temporary directory provided by pytest to create a mock log.conf file.
        mocker (MockerFixture): pytest MockerFixture
    """
    invalid_log_level = 999
    exp_exc_msg = "Cannot configure logging. Invalid log level: 999 of type"
    mocker.patch.object(
        log,
        "ROOT",
        tmp_path
    )
    
    with pytest.raises(ValueError, match=exp_exc_msg):
        log.write_log_level(invalid_log_level)



def test_write_log_level_FileNotFoundError(tmp_path: Path, mocker: MockerFixture) -> None:
    """Test write_log_level function raises FileNotFoundError when log.conf is missing.

    Args:
        tmp_path (Path): Temporary directory provided by pytest to create a mock log.conf file.
        mocker (MockerFixture): pytest MockerFixture
    """
    not_existing_path = tmp_path / "nonexistent"
    mocker.patch.object(
        log,
        "ROOT",
        not_existing_path
    )
    not_existing_log_conf_path: Path = not_existing_path / "src" / "log" / "log.conf"
    exp_exc_msg = f"File '{not_existing_log_conf_path}' does not exist."
    
    with pytest.raises(FileNotFoundError, match=exp_exc_msg):
        log.write_log_level(logging.NOTSET)



def test_rotate_logs_of_all_rotating_file_handlers(
        logger: logging.Logger,
        tmp_path: Path,
        mocker: MockerFixture,
    ):
    """test function rotate_logs_of_all_rotating_file_handlers
    - check that only RotatingFileHanlders do the rollover

    Args:
        logger (logging.Logger): Logger object
        tmp_path (Path): pytest tmp path fixture
        mocker (MockerFixture): pytest mocker fixture
    """
    mock_doRollover: MagicMock = mocker.patch.object(
        logging.handlers.RotatingFileHandler,
        "doRollover",
    )
    tmp_log_file: Path = tmp_path / "test.log"
    tmp_log_file.touch()

    inital_num_handlers: int = len(logger.handlers)

    # add RotatingFileHandlers #
    num_rfh: int = 3
    for _ in range(num_rfh):
        logger.addHandler(
            logging.handlers.RotatingFileHandler(tmp_log_file)
        )

    # add FileHandlers #
    num_fh: int = 4
    for _ in range(num_fh):
        logger.addHandler(
            logging.FileHandler(tmp_log_file)
        )

    # add StreamHandlers #
    num_sh: int = 2
    for _ in range(num_sh):
        logger.addHandler(
            logging.StreamHandler()
        )

    num_added_handlers: int = num_rfh + num_fh + num_sh

    # act #
    log.rotate_logs_of_all_rotating_file_handlers(logger)

    # assert #
    ## ensure that loggers got added correctly #
    assert len(logger.handlers) == inital_num_handlers + num_added_handlers
    ## assert number of calls for mocked function doRollover ##
    assert mock_doRollover.call_count == num_rfh


def test_configure_logger_defaults(logger: logging.Logger):
    """test configure_logger func when default parameters are used
    - this includes ./log/log.conf to be configured with `log_level: WARNING`

    Args:
        logger (logging.Logger): Logger object
    """
    logger = log.configure_logger(logger=logger)

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
            assert handler.formatter._fmt == log._get_basic_format()

    # assert RotatingFileHandler properties #
    has_RotatingFileHandler: bool = any(
        type(handler) == logging.handlers.RotatingFileHandler
        for handler in logger.handlers
    )
    assert has_RotatingFileHandler
    for handler in logger.handlers:
        if type(handler) == logging.handlers.RotatingFileHandler:
            assert handler.level == logging.WARNING
            assert handler.formatter._fmt == log._get_basic_format()
            assert handler.baseFilename == str(log.ROOT / "log" / "app.log")



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
    logger = log.configure_logger(
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
