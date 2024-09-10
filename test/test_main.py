from docopt import docopt
from pytest_mock import MockerFixture
from unittest.mock import MagicMock
import sys

import main
from src.utils.cli_input_args import CliInputArgs
from src.utils.intl_logger import IntlLogger
from src.utils import exception_handling as exc


def test_main(mocker: MockerFixture):
    """test main function

    Args:
        mocker (MockerFixture): pytest mocker fixture
    """
    # Arrange #
    mocked__doc__: str = main.__doc__
    sys.argv = r'.\main.py'.split(" ")
    mock_set_cli_input_args: MagicMock = mocker.patch.object(
        CliInputArgs,
        "set_cli_input_args",
    )
    mock_set_verbosity: MagicMock = mocker.patch.object(
        IntlLogger,
        "set_verbosity",
    )
    mock_add_stream_handler: MagicMock = mocker.patch.object(
        IntlLogger,
        "add_stream_handler",
    )
    mock_add_file_handler: MagicMock = mocker.patch.object(
        IntlLogger,
        "add_file_handler",
    )
    mock_program_end: MagicMock = mocker.patch.object(
        exc,
        "program_end",
    )
    # TODO: test main for doRollover() with tmp_path from pytest

    # Act #
    main.main()

    # Assert #
    mock_set_cli_input_args.assert_called_once_with(docopt(mocked__doc__))
    mock_set_verbosity.assert_called_once()
    mock_add_stream_handler.assert_called_once()
    mock_add_file_handler.assert_called_once()
    mock_program_end.assert_called_once()
