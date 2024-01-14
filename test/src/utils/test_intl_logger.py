import logging
import os
from pathlib import Path
import pytest
from pytest import LogCaptureFixture

from src.utils.intl_logger import IntlLogger
from src.utils.cli_input_args import CliInputArgs


@pytest.fixture
def intl_logger():
    """return instance of default internal logger with name test-logger

    Returns:
        IntlLogger: default internal logger with name test-logger
    """
    return IntlLogger(logger_name="test-logger")


@pytest.fixture
def CliInputArgs():
    """return class CliInputArgs

    Returns:
        CliInputArgs: class
    """
    return CliInputArgs


def test__str__(intl_logger: IntlLogger):
    """test __str__ method

    Args:
        intl_logger (IntlLogger): internal logger
    """
    assert f"This is the internal logger: 'test-logger'." in intl_logger.__str__()

import logging
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from src.utils.cli_input_args import CliInputArgs
from src.vars.paths import ROOT
from src.utils.intl_logger import IntlLogger
from py import path



@patch.object(IntlLogger, 'configure_and_add_handler')
@patch.object(logging, 'StreamHandler')
def test_add_stream_handler(mock_stream_handler, mock_configure_handler, caplog):
    """Test adding a StreamHandler.

    Args:
        mock_stream_handler (MagicMock): Mock for the StreamHandler class.
        mock_configure_handler (MagicMock): Mock for the configure_and_add_handler method.
        caplog (pytest.fixture): Fixture to capture log messages during the test.
    """
    # Arrange
    logger = IntlLogger()
    mock_configure_and_add_handler: MagicMock = patch.object(IntlLogger, )

    # Act
    logger.add_stream_handler()

    # Assert
    mock_configure_handler.assert_called_once_with(mock_stream_handler())

@patch.object(IntlLogger, 'configure_and_add_handler')
# @patch.object(logging, 'FileHandler')
def test_add_file_handler(mock_configure_handler, caplog, tmpdir: path.LocalPath):
    """Test adding a FileHandler.

    Args:
        mock_file_handler (MagicMock): Mock for the FileHandler class.
        mock_configure_handler (MagicMock): Mock for the configure_and_add_handler method.
        caplog (pytest.fixture): Fixture to capture log messages during the test.
        tmpdir (pytest.fixture): Fixture providing a temporary directory.
    """
    # Arrange
    logger = IntlLogger()
    print()
    print()
    print()
    print(tmpdir)
    print(type(tmpdir))
    print()
    print()
    print()

    log_dir = tmpdir.mkdir("log")
    log_file_path = log_dir.join("app.log")
    print(log_file_path)

    # Act
    logger.add_file_handler(file=log_file_path)
    print(log_file_path.exists())

    # Assert
    # mock_configure_handler.assert_called_once_with(mock_file_handler(str(log_file_path)))
    assert log_file_path.exists()

@patch.object(logging, 'StreamHandler')
def test_set_verbosity_verbose(mock_stream_handler):
    """Test setting verbosity to verbose.

    Args:
        mock_stream_handler (MagicMock): Mock for the StreamHandler class.
    """
    # Arrange
    handler = mock_stream_handler()
    CliInputArgs.verbose = True
    logger = IntlLogger()

    # Act
    logger.set_verbosity(handler)

    # Assert
    assert handler.level == logging.DEBUG

@patch.object(logging, 'StreamHandler')
def test_set_verbosity_quiet(mock_stream_handler):
    """Test setting verbosity to quiet.

    Args:
        mock_stream_handler (MagicMock): Mock for the StreamHandler class.
    """
    # Arrange
    handler = mock_stream_handler()
    CliInputArgs.quiet = True
    logger = IntlLogger()

    # Act
    logger.set_verbosity(handler)

    # Assert
    assert handler.level == logging.ERROR

@patch.object(logging, 'StreamHandler')
def test_set_verbosity_default(mock_stream_handler):
    """Test setting verbosity to default.

    Args:
        mock_stream_handler (MagicMock): Mock for the StreamHandler class.
    """
    # Arrange
    handler = mock_stream_handler()
    CliInputArgs.verbose = False
    CliInputArgs.quiet = False
    logger = IntlLogger()

    # Act
    logger.set_verbosity(handler)

    # Assert
    assert handler.level == logging.WARNING
