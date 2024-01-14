import logging
import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock
from py import path

from src.utils.intl_logger import IntlLogger
from src.utils import cli_input_args
from src.utils.cli_input_args import CliInputArgs


@pytest.fixture
def intl_logger():
    """return instance of default internal logger with name test-logger

    Returns:
        IntlLogger: default internal logger with name test-logger
    """
    return IntlLogger(logger_name="test-logger")

@pytest.fixture
def mock_CliInputArgs(mocker: MockerFixture) -> MagicMock:
    """mocks logging.CliInputArgs

    Args:
        mocker (MockerFixture): pytest MockerFixture

    Returns:
        MagicMock: mocked CliInputArgs class
    """
    return mocker.patch.object(
        cli_input_args,
        "CliInputArgs",
    )

@pytest.fixture
def mock_configure_and_add_handler(mocker: MockerFixture) -> MagicMock:
    """mocks IntlLogger.configure_and_add_handler

    Args:
        mocker (MockerFixture): pytest MockerFixture

    Returns:
        MagicMock: mocked method
    """
    return mocker.patch.object(
        IntlLogger,
        "configure_and_add_handler",
    )

@pytest.fixture
def mock_stream_handler(mocker: MockerFixture) -> MagicMock:
    """mocks logging.StreamHandler

    Args:
        mocker (MockerFixture): pytest MockerFixture

    Returns:
        MagicMock: mocked StreamHandler class
    """
    return mocker.patch.object(
        logging,
        "StreamHandler",
    )



def _reset_CliInputArgs():
    """reset CliInputArgs class variables to default values
    """
    CliInputArgs.verbose = False
    CliInputArgs.quiet = False
    CliInputArgs.hello = False



def test__str__(intl_logger: IntlLogger):
    """test __str__ method

    Args:
        intl_logger (IntlLogger): internal logger
    """
    assert f"This is the internal IntlLogger: 'test-logger'." in intl_logger.__str__()



def test_add_stream_handler(mock_configure_and_add_handler: MagicMock, mock_stream_handler: MagicMock):
    """test adding a stream handler

    Args:
        mock_configure_and_add_handler (MagicMock): mocked method
        mock_stream_handler (MagicMock): mocked class
    """
    # Arrange
    intl_logger = IntlLogger()

    # Act
    intl_logger.add_stream_handler()

    # Assert
    mock_configure_and_add_handler.assert_called_once_with(mock_stream_handler())


def test_add_file_handler(mock_configure_and_add_handler: MagicMock, tmpdir: path.LocalPath):
    """test adding a file handler

    Args:
        mock_configure_and_add_handler (MagicMock): mocked method
        tmpdir (path.LocalPath): pytest fixture tmpdir
    """
    # Arrange
    intl_logger = IntlLogger()
    log_dir = tmpdir.mkdir("log")
    test_path = log_dir.join("test.log")

    # Act
    intl_logger.add_file_handler(file=test_path)

    # Assert
    mock_configure_and_add_handler.assert_called_once()
    assert test_path.exists()


def test_set_verbosity_verbose():
    """Test setting verbosity to verbose.
    """
    # Arrange
    CliInputArgs.verbose = True
    handler = logging.StreamHandler()
    intl_logger = IntlLogger()

    # Act
    intl_logger.set_verbosity(handler)

    # Assert
    assert handler.level == logging.DEBUG

    # TearDown #
    _reset_CliInputArgs()

def test_set_verbosity_quiet():
    """Test setting verbosity to quiet.
    """
    # Arrange
    CliInputArgs.quiet = True
    handler = logging.StreamHandler()
    intl_logger = IntlLogger()

    # Act
    intl_logger.set_verbosity(handler)

    # Assert
    assert handler.level == logging.ERROR

    # TearDown #
    _reset_CliInputArgs()

def test_set_verbosity_default():
    """Test setting verbosity to default.
    """
    # Arrange
    handler = logging.StreamHandler()
    intl_logger = IntlLogger()

    # Act
    intl_logger.set_verbosity(handler)

    # Assert
    assert handler.level == logging.WARNING


def test_configure_and_add_handler(mocker: MockerFixture):
    """Test configure_and_add_handler with verbosity set to verbose.

    Args:
        mocker (MockerFixture): pytest MockerFixture
    """
    # Arrange
    mock_handler = MagicMock()
    mock_set_verbosity: MagicMock = mocker.patch.object(
        IntlLogger,
        "set_verbosity",
    )
    mock_formatter: MagicMock = mocker.patch.object(
        logging,
        "Formatter",
    )
    intl_logger = IntlLogger()
    intl_logger.logger = MagicMock()

    # Act
    intl_logger.configure_and_add_handler(mock_handler)

    # Assert
    mock_set_verbosity.assert_called_once_with(mock_handler)
    mock_handler.setFormatter.assert_called_once_with(mock_formatter(intl_logger.format))
    intl_logger.logger.addHandler.assert_called_once_with(mock_handler)
