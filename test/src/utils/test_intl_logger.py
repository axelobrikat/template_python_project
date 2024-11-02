"""
NOTE,
- to capture output of logging, use pytest fixture caplog
  - ...as implemented in this test script
- to capture stdout and stderr, use pytest fixture capsys
  - see https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html
  - typehint with CaptureFixture (from _pytest.capture import CaptureFixture)
  - assert stdout, stderr using
    ```
    cap = capsys.readouterr()
    assert cap.err == "your stderr text"
    assert cap.out == "your stdout text"
    ```
"""

import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock

from src.utils.intl_logger import logging
from src.utils.intl_logger import IntlLogger
from src.utils.cli_input_args import CLI


@pytest.fixture
def intl_logger():
    """return instance of default internal logger with name 'test-logger'
    NOTE, it is important to not use default 'root' logger, as this contradicts
        .. with pytest logging

    Returns:
        IntlLogger: default internal logger with name 'test-logger'
    """
    return IntlLogger(logger_name="test-logger")


@pytest.fixture(autouse=True)
def tearDown():
    """yield test and tearDown
    - clear handlers from all created loggers
    - clear list of IntlLogger instances to prevent exception to be thrown
    - reset CLI to defaults
    """
    yield

    # clear handlers from all created loggers #
    for name in IntlLogger.logger_names:
        logging.getLogger(name).handlers.clear()

    # clear logger_names #
    IntlLogger.logger_names = []

    # reset CLI to defaults #
    CLI.set_cli_input_args()


@pytest.fixture
def mock_stream_handler(mocker: MockerFixture) -> MagicMock:
    """mocks logging.StreamHandler to return a Callable
    - Callable returns instance of logging.Handler with default verbosity WARNING
      - this ensures that the same object can be compared for test assertion

    Args:
        mocker (MockerFixture): pytest MockerFixture

    Returns:
        MagicMock: mocked StreamHandler class
    """
    dummy_handler = logging.Handler(logging.WARNING)

    def __callable__():
        return dummy_handler

    return mocker.patch.object(
        logging,
        "StreamHandler",
        new_callable=lambda: __callable__
    )



def test___new__exception(intl_logger: IntlLogger, caplog: pytest.LogCaptureFixture):
    """test __new__ method
    - IntlLogger with duplicate name gets instantiated and exception occurs

    Args:
        intl_logger (IntlLogger): internal logger
        caplog (pytest.LogCaptureFixture): pytest fixture to capture logging
    """
    # act # 
    # instanciate logger with same name #
    with pytest.raises(Exception):
        _ = IntlLogger(intl_logger.name)

    # assert # 
    assert "'test-logger' has already been instantiated and configured" in caplog.text
    assert "instances must have unique names" in caplog.text
    assert "Access the existing logger of" in caplog.text


def test__str__(intl_logger: IntlLogger):
    """test __str__ method

    Args:
        intl_logger (IntlLogger): internal logger instance 'test-logger'
    """
    assert f"This is the internal IntlLogger: 'test-logger'." == intl_logger.__str__()


def test_add_stream_handler(intl_logger: IntlLogger, mock_stream_handler: MagicMock):
    """test adding a stream handler

    Args:
        intl_logger (IntlLogger): internal logger instance 'test-logger'
        mock_stream_handler (MagicMock): mocked class
    """
    # Act #
    intl_logger.add_stream_handler()

    # Assert #
    assert len(intl_logger.logger.handlers) == 1, \
        f"Expected exactly 1 handler to be added, but got {len(intl_logger.logger.handlers)}."
    assert intl_logger.logger.handlers[0] == mock_stream_handler(), \
        f"Not the expected hanlder object has been added."
    assert intl_logger.logger.handlers[0].formatter._fmt == intl_logger.format, \
        f"Expected format '{intl_logger.format}', but got '{intl_logger.logger.handlers[0].formatter._fmt}'."


def test_add_file_handler(intl_logger: IntlLogger):
    """test adding a file handler

    Args:
        intl_logger (IntlLogger): internal logger instance 'test-logger'
    """
    # Act #
    intl_logger.add_file_handler()

    # Assert #
    assert len(intl_logger.logger.handlers) == 1, \
        f"Expected exactly 1 handler to be added, but got {len(intl_logger.logger.handlers)}."
    assert intl_logger.logger.handlers[0] == IntlLogger.rotating_file_handler, \
        f"Not the expected hanlder object has been added."
    assert intl_logger.logger.handlers[0].formatter._fmt == intl_logger.format, \
        f"Expected format '{intl_logger.format}', but got '{intl_logger.logger.handlers[0].formatter._fmt}'."
    assert intl_logger.logger.handlers[0].baseFilename == str(IntlLogger.log_file_path), \
        f"Expected filepath of log file '{str(IntlLogger.log_file_path)}', but got '{intl_logger.logger.handlers[0].baseFilename}'."


@pytest.mark.parametrize(
    "test_case,verbosity,log_level", [
        ("Test Case: verbose - root logger","verbose", logging.DEBUG),
        ("Test Case: quiet - root logger","quiet", logging.ERROR),
        ("Test Case: default - root logger","default", logging.WARNING),
    ]
)
def test_set_verbosity_root(test_case: str, verbosity: str, log_level: int):
    """Test function set_verbosity with "root" logger

    Args:
        test_case (str): test case name
        verbosity (str): parameterized test input
        log_level (int): parameterized expected result
    """
    # Arrange
    if verbosity=="verbose":
        CLI.verbose = True
    elif verbosity=="quiet":
        CLI.quiet = True
    elif verbosity=="default":
        pass # auto-tearDown sets class args back to default vals
    else:
        assert False, f"Test input of Test Case '{test_case}' invalid. Verbosity level '{verbosity}' not defined."

    handler = logging.StreamHandler()
    intl_logger = IntlLogger()

    # Act
    intl_logger.set_verbosity(handler)

    # Assert
    assert handler.level == log_level, \
        f"Test Case {test_case} failed. Expected log level '{log_level}, but got {handler.level}"


def test_set_verbosity_not_root(intl_logger: IntlLogger):
    """Test function set_verbosity with a logger that is not "root"

    Args:
        intl_logger (IntlLogger): internal logger instance 'test-logger'
    """
    # Arrange
    handler = logging.StreamHandler()

    # Act
    intl_logger.set_verbosity(handler)

    # Assert
    assert handler.level == logging.WARNING
