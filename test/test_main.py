"""
TODO:
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
    "cli_cmd", [
        (r'.\main.py --dummy-test'),
        (r'.\main.py -v -q'),
        (r'.\main.py -v -q --hello'),
        (r'.\main.py -'),
    ]
)
def test_evaluate_cli_input_args_fail(
    mocker: MockerFixture,
    cli_cmd: str,
):
    """test function evaluate_cli_input_args with invalid input arg options
    - test different test cases
    - expect DocoptExit to be thrown

    Args:
        mocker (MockerFixture): pytest mocker
        cli_cmd (str): cli cmd to run the python file
    """
    # arrange #
    sys.argv = cli_cmd.split(" ")
    mocked_set_cli_input_args: MagicMock = mocker.patch.object(
        CliInputArgs,
        "set_cli_input_args",
    )

    # act and assert #
    with pytest.raises(DocoptExit):
        main.evaluate_cli_input_args()
        mocked_set_cli_input_args.assert_not_called()



@pytest.mark.parametrize(
    "cli_cmd, exp_res", [
        (r'.\main.py', {"-v": False, "-q": False,"--hello": False,}),
        (r'.\main.py -v', {"-v": True, "-q": False,"--hello": False,}),
        (r'.\main.py -q', {"-v": False, "-q": True,"--hello": False,}),
        (r'.\main.py --hello', {"-v": False, "-q": False,"--hello": True,}),
        (r'.\main.py -v --hello', {"-v": True, "-q": False,"--hello": True,}),
        (r'.\main.py -q --hello', {"-v": False, "-q": True,"--hello": True,}),
    ]
)
def test_evaluate_cli_input_args_success(
    mocker: MockerFixture,
    cli_cmd: str,
    exp_res: dict[str, Any],
):
    """test function evaluate_cli_input_args with valid input arg options
    - test different test cases
    - expect func set_cli_input_args to be run with resp. parameters

    Args:
        mocker (MockerFixture): pytest mocker
        cli_cmd (str): cli cmd to run the python file
    """
    # arrange #
    sys.argv = cli_cmd.split(" ")
    mocked_set_cli_input_args: MagicMock = mocker.patch.object(
        CliInputArgs,
        "set_cli_input_args",
    )

    # act and assert #
    main.evaluate_cli_input_args()
    mocked_set_cli_input_args.assert_called_once_with(
        verbose=exp_res["-v"],
        quiet=exp_res["-q"],
        hello=exp_res["--hello"],
    )



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
