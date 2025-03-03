"""
unit testing of main.py
"""
import pytest
from docopt import DocoptExit
from pytest_mock import MockerFixture
from pytest import LogCaptureFixture
from unittest.mock import MagicMock
import sys
from typing import Any
import logging

import main
from main import exc, log, CLI, SEPARATOR


TEST_LOGGER_NAME: str = "test-logger"


@pytest.fixture(autouse=True)
def setUp_tearDown(mocker: MockerFixture):
    """setUp and tearDown
    - patch the logger object
    - yield the test
    - delete logger objects that have been created during testing

    Args:
        mocker (MockerFixture): pytest mocker fixture
    """
    mocker.patch.object(
        main,
        "logger",
        logging.getLogger(TEST_LOGGER_NAME)
    )

    yield

    del logging.root.manager.loggerDict[TEST_LOGGER_NAME]

## TODO: to prevent actual log file creation ##
## This func does not work ##
@pytest.fixture(autouse=True)
def mock_configure_logger(mocker: MockerFixture) -> MagicMock:
    """return function configure_logger
    - to prevent actual log file creation
    """
    return mocker.patch.object(
        log,
        "configure_logger",
    )


@pytest.fixture(autouse=True)
def mock_rotate_logs_of_all_rotating_file_handlers(mocker: MockerFixture) -> MagicMock:
    """return function rotate_logs_of_all_rotating_file_handlers
    - to prevent actual log rotation
    """
    return mocker.patch.object(
        log,
        "rotate_logs_of_all_rotating_file_handlers",
    )


@pytest.fixture
def mock_hello(mocker: MockerFixture) -> MagicMock:
    """return function hello
    """
    return mocker.patch.object(
        main,
        "hello",
    )


@pytest.fixture
def mock_program_end(mocker: MockerFixture) -> MagicMock:
    """return function program_end
    """
    return mocker.patch.object(
        exc,
        "program_end",
    )



@pytest.mark.parametrize(
    "cli_cmd", [
        (r'.\main.py --dummy-test'),
        (r'.\main.py -v -q'),
        (r'.\main.py -v -Q'),
        (r'.\main.py -V --dummy'),
        (r'.\main.py -'),
    ]
)
def test__evaluate_cli_input_args_fail(
    mocker: MockerFixture,
    cli_cmd: str,
):
    """test function _evaluate_cli_input_args with invalid input arg options
    - test different test cases
    - expect DocoptExit to be thrown

    Args:
        mocker (MockerFixture): pytest mocker
        cli_cmd (str): cli cmd to run the python file
    """
    # arrange #
    sys.argv = cli_cmd.split(" ")
    mocked_set_cli_input_args: MagicMock = mocker.patch.object(
        CLI,
        "set_cli_input_args",
    )

    # act and assert #
    with pytest.raises(DocoptExit):
        main._evaluate_cli_input_args()
    mocked_set_cli_input_args.assert_not_called()



@pytest.mark.parametrize(
    "cli_cmd, exp_res", [
        (r'.\main.py', {"v": False, "V": False, "q": False, "Q": False, "hello": False}),
        (r'.\main.py -v', {"v": True, "V": False, "q": False, "Q": False, "hello": False}),
        (r'.\main.py -V', {"v": False, "V": True, "q": False, "Q": False, "hello": False}),
        (r'.\main.py -q', {"v": False, "V": False, "q": True, "Q": False, "hello": False}),
        (r'.\main.py -Q', {"v": False, "V": False, "q": False, "Q": True, "hello": False}),
        (r'.\main.py --hello', {"v": False, "V": False, "q": False, "Q": False, "hello": True}),
        (r'.\main.py -v --hello', {"v": True, "V": False, "q": False, "Q": False, "hello": True}),
        (r'.\main.py -q --hello', {"v": False, "V": False, "q": True, "Q": False, "hello": True}),
    ]
)
def test__evaluate_cli_input_args_success(
    mocker: MockerFixture,
    cli_cmd: str,
    exp_res: dict[str, Any],
):
    """test function _evaluate_cli_input_args with valid input arg options
    - test different test cases
    - expect func set_cli_input_args to be run with resp. parameters

    Args:
        mocker (MockerFixture): pytest mocker
        cli_cmd (str): cli cmd to run the python file
        exp_res (dict[str, Any]): holds expected test case results
    """
    # arrange #
    sys.argv = cli_cmd.split(" ")
    mocked_set_cli_input_args: MagicMock = mocker.patch.object(
        CLI,
        "set_cli_input_args",
    )

    # act and assert #
    main._evaluate_cli_input_args()
    mocked_set_cli_input_args.assert_called_once_with(
        v=exp_res["v"],
        V=exp_res["V"],
        q=exp_res["q"],
        Q=exp_res["Q"],
        hello=exp_res["hello"],
    )


@pytest.mark.parametrize(
    "test_case, log_level", [
        ("1: DEBUG", logging.DEBUG),
        ("3: INFO", logging.INFO),
        ("2: WARNING", logging.WARNING),
        ("4: ERROR", logging.ERROR),
        ("5: CRITICAL", logging.CRITICAL),
    ]
)
def test_main(
        caplog: LogCaptureFixture,
        mock_hello: MagicMock,
        mock_program_end: MagicMock,
        test_case: str,
        log_level: int,
    ):
    """test main function
    - only test basic functionality like
      - ...does logger creation work
      - ...does logging work
      - ...are function calls correct

    Args:
        caplog (LogCaptureFixture): pytest log fixture
        mock_hello (MagicMock): mocked function hello
        mock_program_end (MagicMock): mocked function program_end
        test_case (str): test case name
        log_level (int): Logging level to test
    """
    # arrange #
    caplog.set_level(log_level)

    # act #
    main.main()

    # assert that logger got created #
    assert TEST_LOGGER_NAME in logging.Logger.manager.loggerDict, \
        f"Expected logger name '{TEST_LOGGER_NAME}' not found in logger list."

    # assert that msg was correctly logged #
    if log_level == logging.DEBUG:
        assert f"Program execution starts." in caplog.text, \
            f"test case '{test_case}' failed."
        assert f"Logging and Input Arguments configured successfully." in caplog.text, \
            f"test case '{test_case}' failed."
        assert f"{SEPARATOR}" in caplog.text, \
            f"test case '{test_case}' failed."
    else:
        assert "" == caplog.text, \
            f"test case '{test_case}' failed."

    # assert that mocked functions are called #
    mock_hello.assert_called_once()
    mock_program_end.assert_called_once()
