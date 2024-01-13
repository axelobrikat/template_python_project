import logging
import os
from pathlib import Path
import pytest
from pytest import LogCaptureFixture

from src.utils.logger import Logger


@pytest.fixture
def logger():
    """return instance of default internal logger with name test-logger

    Returns:
        Logger: default internal logger with name test-logger
    """
    return Logger(logger_name="test-logger")


def test__str__(logger: Logger):
    """test __str__ method

    Args:
        logger (Logger): internal logger
    """
    assert f"This is the internal logger: 'test-logger'." in logger.__str__()

import logging
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from src.utils.cli_input_args import CliInputArgs
from src.vars.paths import ROOT
from src.utils.logger import Logger
from py import path



@patch.object(Logger, 'configure_and_add_handler')
@patch.object(logging, 'StreamHandler')
def test_add_stream_handler(mock_stream_handler, mock_configure_handler, caplog):
    """Test adding a StreamHandler.

    Args:
        mock_stream_handler (MagicMock): Mock for the StreamHandler class.
        mock_configure_handler (MagicMock): Mock for the configure_and_add_handler method.
        caplog (pytest.fixture): Fixture to capture log messages during the test.
    """
    # Arrange
    logger = Logger()

    # Act
    logger.add_stream_handler()

    # Assert
    assert isinstance(logger.logger.handlers[0], logging.StreamHandler)
    mock_configure_handler.assert_called_once_with(mock_stream_handler())

@patch.object(Logger, 'configure_and_add_handler')
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
    logger = Logger()
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
    logger = Logger()

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
    logger = Logger()

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
    logger = Logger()

    # Act
    logger.set_verbosity(handler)

    # Assert
    assert handler.level == logging.WARNING
