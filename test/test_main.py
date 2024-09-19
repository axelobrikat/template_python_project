"""
TODO:
- test_main
- docstrings
"""

import pytest
from docopt import DocoptExit
from pytest_mock import MockerFixture
from pytest import LogCaptureFixture
from unittest.mock import MagicMock
import sys
from pathlib import Path
from typing import Any
import logging

import main
from main import CliInputArgs
from main import IntlLogger
from main import exc


@pytest.fixture##debug
def mock_IntlLogger(mocker: MockerFixture):
    """yield class IntlLogger
    """
    # m = mocker.patch.object(
    #     main,
    #     "IntlLogger",
    #     return_value=IntlLogger("test-logger")
    # )

    yield IntlLogger

    print(str(IntlLogger.logger_names)) #debug
    print(IntlLogger.log_file_path) #debug
    print(IntlLogger.rotating_file_handler.baseFilename) #debug

    # set back baseFilename #
    IntlLogger.rotating_file_handler.baseFilename = str(IntlLogger.log_file_path)
        ##TODO: why do I have to do this when handlers will be cleared?
        ## ---> maybe try mocker.patch with side_effect callable that return IntlLogger("test-logger")
        ##      maybe it is interferring with pytest root logger

    # clear handlers from all created loggers #
    for name in IntlLogger.logger_names:
        print(str(logging.getLogger(name).handlers)) #debug
        logging.getLogger(name).handlers.clear()
        print(str(logging.getLogger(name).handlers)) #debug

    # clear logger_names #
    IntlLogger.logger_names = []
    
    print(str(IntlLogger.logger_names)) #debug
    print(IntlLogger.log_file_path) #debug
    print(IntlLogger.rotating_file_handler.baseFilename) #debug



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


## TODO: fix usage of class vars and methods
def test_main(mocker: MockerFixture, tmp_path: Path, mock_IntlLogger: IntlLogger, caplog: LogCaptureFixture):
    """test main function

    Args:
        mocker (MockerFixture): pytest mocker fixture
        tmp_path (Path): pytest mocker fixture for paths
        mock_IntlLogger (IntlLogger): yield class IntlLogger
        caplog (LogCaptureFixture): pytest fixture to capture logging
    """
    # mock log dir path #
    tmp_log_path: Path = tmp_path / "log"
    tmp_log_path.mkdir(parents=True, exist_ok=True)

    def __get_len_tmp_log_path() -> int:
        """returns number of elements in tmp log dir path

        Returns:
            int: number of elements in tmp log dir path
        """
        return len(list(tmp_log_path.iterdir()))

    def __get_elements_name(num: int) -> Path:
        """get name of an element in tmp log dir path

        Args:
            num (int): number of element in folder to be retrieved (zero-indexed)

        Returns:
            Path: Path to element
        """
        return list(tmp_log_path.iterdir())[num]

    # ensure that tmp log dir path has been created correctly #
    assert __get_len_tmp_log_path() == 0, \
        f"Created tmp test dir. Expected to be empty, but is not. Abort test."

    # mock log file path #
    tmp_log_file_path: Path = tmp_log_path / "test.log"
    tmp_log_file_path.touch(exist_ok=True)
    log_msg_1: str = "First dummy log msg."
    tmp_log_file_path.write_text(log_msg_1)

    # ensure that tmp log file path has been created correctly #
    assert __get_len_tmp_log_path() == 1, \
        f"Created tmp test log file. Expected to only have created one file, but got '{__get_len_tmp_log_path()}'."
    assert str(__get_elements_name(0)).endswith("test.log"), \
        f"Created tmp test log file. Expected its name to be test.log, but got '{str(__get_elements_name(0))}'."
    assert __get_elements_name(0).read_text() == log_msg_1, \
        f"Wrote text to tmp test log file. Expected '{log_msg_1}', but got '{__get_elements_name(0).read_text()}'."


    # Arrange #
    mock_evaluate_cli_input_args: MagicMock = mocker.patch.object(
        main,
        "evaluate_cli_input_args",
    )
    mock_program_end: MagicMock = mocker.patch.object(
        exc,
        "program_end",
    )
    mock_log_exec_start_msg: MagicMock = mocker.patch.object(
        main,
        "log_exec_start_msg",
    )
    mock_IntlLogger.rotating_file_handler.baseFilename = str(tmp_log_file_path)

    # Act #
    main.main()

    # Assert #
    mock_evaluate_cli_input_args.assert_called_once()
    mock_log_exec_start_msg.assert_called_once()
    mock_program_end.assert_called_once()
    # ensure that rollover of tmp log file path was successful #
    assert __get_len_tmp_log_path() == 2, \
        f"Expected to have 2 log files due to logrotate, but got '{__get_len_tmp_log_path()}'."
    assert str(__get_elements_name(0)).endswith("test.log"), \
        f"Expected name of first log file to be test.log, but got '{str(__get_elements_name(0))}'."
    assert str(__get_elements_name(1)).endswith("test.log.1"), \
        f"Expected name of second log file to be test.log.1, but got '{str(__get_elements_name(1))}'."
    assert __get_elements_name(1).read_text() == log_msg_1, (
        f"Due to log rotation, log file content should have been rolled over."
        f"Expected '{log_msg_1}', but got '{__get_elements_name(1).read_text()}'."
    )

def test_main_danach(): ##debug
    IntlLogger("nice")
    print(IntlLogger.rotating_file_handler.baseFilename)