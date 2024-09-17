"""
TODO:
- split test_evaluate_cli_input_args into two separate tests:
  - test_evaluate_cli_input_args_success
  - test_evaluate_cli_input_args_fail
- test_main
- docstrings
"""

import pytest
from docopt import docopt, DocoptExit
from pytest_mock import MockerFixture
from unittest.mock import MagicMock
import sys
from typing import Any

import main
from main import CliInputArgs
from main import IntlLogger
from main import exc

@pytest.mark.parametrize(
    "docopt_passes, cli_cmd, exp_res", [
        (True, r'.\main.py', {"-v": False, "-q": False,"--hello": False,}),
        (True, r'.\main.py -v', {"-v": True, "-q": False,"--hello": False,}),
        (True, r'.\main.py -q', {"-v": False, "-q": True,"--hello": False,}),
        (True, r'.\main.py --hello', {"-v": False, "-q": False,"--hello": True,}),
        (True, r'.\main.py -v --hello', {"-v": True, "-q": False,"--hello": True,}),
        (False, r'.\main.py --dummy-test', {}),
        (False, r'.\main.py -v -q', {}),
    ]
)
def test_evaluate_cli_input_args(
    mocker: MockerFixture,
    docopt_passes: bool,
    cli_cmd: str,
    exp_res: dict[str, Any]
):

    sys.argv = cli_cmd.split(" ")
    mocked_set_cli_input_args: MagicMock = mocker.patch.object(
        CliInputArgs,
        "set_cli_input_args",
    )

    # act #
    if docopt_passes:
        main.evaluate_cli_input_args()
        mocked_set_cli_input_args.assert_called_once_with(
            verbose=exp_res["-v"],
            quiet=exp_res["-q"],
            hello=exp_res["--hello"],
        )
    else:
        with pytest.raises(DocoptExit):
            main.evaluate_cli_input_args()
            mocked_set_cli_input_args.assert_not_called()


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
