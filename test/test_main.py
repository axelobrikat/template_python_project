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

from src import hello_world


TEST_LOGGER_NAME: str = "test-logger"


@pytest.fixture(autouse=True)
def patch___name__(mocker: MockerFixture):
    mocker.patch.object(
        main,
        "__name__",
        TEST_LOGGER_NAME
    )

    yield

    if TEST_LOGGER_NAME in logging.root.manager.loggerDict:
        del logging.root.manager.loggerDict[TEST_LOGGER_NAME]


@pytest.fixture
def mock_evaluate_cli_input_args(mocker: MockerFixture) -> MagicMock:
    """return function evaluate_cli_input_args
    """
    return mocker.patch.object(
        main,
        "evaluate_cli_input_args",
    )


@pytest.fixture
def mock_write_log_level(mocker: MockerFixture) -> MagicMock:
    """return function write_log_level
    """
    return mocker.patch.object(
        log,
        "write_log_level",
    )


@pytest.fixture
def mock_get_wanted_log_level(mocker: MockerFixture) -> MagicMock:
    """return function get_wanted_log_level
    """
    return mocker.patch.object(
        CLI,
        "get_wanted_log_level",
    )


@pytest.fixture
def mock_rotate_logs_of_all_rotating_file_handlers(mocker: MockerFixture) -> MagicMock:
    """return function rotate_logs_of_all_rotating_file_handlers
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
        hello_world,
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


# @pytest.fixture##debug
# def mock_IntlLogger(mocker: MockerFixture):
#     """yield class IntlLogger
#     """
#     # m = mocker.patch.object(
#     #     main,
#     #     "IntlLogger",
#     #     return_value=IntlLogger("test-logger")
#     # )

#     yield IntlLogger

#     print(str(IntlLogger.logger_names)) #debug
#     print(IntlLogger.log_file_path) #debug
#     print(IntlLogger.rotating_file_handler.baseFilename) #debug

#     # set back baseFilename #
#     IntlLogger.rotating_file_handler.baseFilename = str(IntlLogger.log_file_path)
#         ##TODO: why do I have to do this when handlers will be cleared?
#         ## ---> maybe try mocker.patch with side_effect callable that return IntlLogger("test-logger")
#         ##      maybe it is interferring with pytest root logger

#     # clear handlers from all created loggers #
#     for name in IntlLogger.logger_names:
#         print(str(logging.getLogger(name).handlers)) #debug
#         logging.getLogger(name).handlers.clear()
#         print(str(logging.getLogger(name).handlers)) #debug

#     # clear logger_names #
#     IntlLogger.logger_names = []
    
#     print(str(IntlLogger.logger_names)) #debug
#     print(IntlLogger.log_file_path) #debug
#     print(IntlLogger.rotating_file_handler.baseFilename) #debug



@pytest.mark.parametrize(
    "cli_cmd", [
        (r'.\main.py --dummy-test'),
        (r'.\main.py -v -q'),
        (r'.\main.py -v -Q'),
        (r'.\main.py -V --dummy'),
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
        CLI,
        "set_cli_input_args",
    )

    # act and assert #
    with pytest.raises(DocoptExit):
        main.evaluate_cli_input_args()
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
        exp_res (dict[str, Any]): holds expected test case results
    """
    # arrange #
    sys.argv = cli_cmd.split(" ")
    mocked_set_cli_input_args: MagicMock = mocker.patch.object(
        CLI,
        "set_cli_input_args",
    )

    # act and assert #
    main.evaluate_cli_input_args()
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
        test_case: str,
        log_level: int,
        caplog: LogCaptureFixture,
        mock_evaluate_cli_input_args: MagicMock,
        mock_write_log_level: MagicMock,
        mock_get_wanted_log_level: MagicMock,
        mock_rotate_logs_of_all_rotating_file_handlers: MagicMock,
        mock_hello: MagicMock,
        mock_program_end: MagicMock,
    ):
    """test main function
    - only test basic functionality like
      - ...does logger creation work
      - ...does logging work
      - ...are function calls correct
      TODO: fix this test

    Args:
        test_case (str): test case name
        log_level (int): Logging level to test
        caplog (LogCaptureFixture): pytest log fixture
        mock_evaluate_cli_input_args (MagicMock): mocked function evaluate_cli_input_args
        mock_write_log_level (MagicMock): mocked function write_log_level
        mock_get_wanted_log_level (MagicMock): mocked function get_wanted_log_level
        mock_rotate_logs_of_all_rotating_file_handlers (MagicMock): mocked function rotate_logs_of_all_rotating_file_handlers
        mock_hello (MagicMock): mocked function hello
        mock_program_end (MagicMock): mocked function program_end
    """    
    caplog.set_level(log_level)

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
    mock_evaluate_cli_input_args.assert_called_once()
    mock_write_log_level.assert_called_once()
    mock_get_wanted_log_level.assert_called_once()
    mock_rotate_logs_of_all_rotating_file_handlers.assert_called_once()
    mock_hello.assert_called_once()
    mock_program_end.assert_called_once()

    


# ## TODO: fix usage of class vars and methods
# def test_main__(mocker: MockerFixture, tmp_path: Path, mock_IntlLogger, caplog: LogCaptureFixture):
#     """test main function

#     Args:
#         mocker (MockerFixture): pytest mocker fixture
#         tmp_path (Path): pytest mocker fixture for paths
#         mock_IntlLogger (IntlLogger): yield class IntlLogger
#         caplog (LogCaptureFixture): pytest fixture to capture logging
#     """
#     # mock log dir path #
#     tmp_log_path: Path = tmp_path / "log"
#     tmp_log_path.mkdir(parents=True, exist_ok=True)

#     def __get_len_tmp_log_path() -> int:
#         """returns number of elements in tmp log dir path

#         Returns:
#             int: number of elements in tmp log dir path
#         """
#         return len(list(tmp_log_path.iterdir()))

#     def __get_elements_name(num: int) -> Path:
#         """get name of an element in tmp log dir path

#         Args:
#             num (int): number of element in folder to be retrieved (zero-indexed)

#         Returns:
#             Path: Path to element
#         """
#         return list(tmp_log_path.iterdir())[num]

#     # ensure that tmp log dir path has been created correctly #
#     assert __get_len_tmp_log_path() == 0, \
#         f"Created tmp test dir. Expected to be empty, but is not. Abort test."

#     # mock log file path #
#     tmp_log_file_path: Path = tmp_log_path / "test.log"
#     tmp_log_file_path.touch(exist_ok=True)
#     log_msg_1: str = "First dummy log msg."
#     tmp_log_file_path.write_text(log_msg_1)

#     # ensure that tmp log file path has been created correctly #
#     assert __get_len_tmp_log_path() == 1, \
#         f"Created tmp test log file. Expected to only have created one file, but got '{__get_len_tmp_log_path()}'."
#     assert str(__get_elements_name(0)).endswith("test.log"), \
#         f"Created tmp test log file. Expected its name to be test.log, but got '{str(__get_elements_name(0))}'."
#     assert __get_elements_name(0).read_text() == log_msg_1, \
#         f"Wrote text to tmp test log file. Expected '{log_msg_1}', but got '{__get_elements_name(0).read_text()}'."


#     # Arrange #
#     mock_evaluate_cli_input_args: MagicMock = mocker.patch.object(
#         main,
#         "evaluate_cli_input_args",
#     )
#     mock_program_end: MagicMock = mocker.patch.object(
#         exc,
#         "program_end",
#     )
#     mock_log_exec_start_msg: MagicMock = mocker.patch.object(
#         main,
#         "log_exec_start_msg",
#     )
#     mock_IntlLogger.rotating_file_handler.baseFilename = str(tmp_log_file_path)

#     # Act #
#     main.main()

#     # Assert #
#     mock_evaluate_cli_input_args.assert_called_once()
#     mock_log_exec_start_msg.assert_called_once()
#     mock_program_end.assert_called_once()
#     # ensure that rollover of tmp log file path was successful #
#     assert __get_len_tmp_log_path() == 2, \
#         f"Expected to have 2 log files due to logrotate, but got '{__get_len_tmp_log_path()}'."
#     assert str(__get_elements_name(0)).endswith("test.log"), \
#         f"Expected name of first log file to be test.log, but got '{str(__get_elements_name(0))}'."
#     assert str(__get_elements_name(1)).endswith("test.log.1"), \
#         f"Expected name of second log file to be test.log.1, but got '{str(__get_elements_name(1))}'."
#     assert __get_elements_name(1).read_text() == log_msg_1, (
#         f"Due to log rotation, log file content should have been rolled over."
#         f"Expected '{log_msg_1}', but got '{__get_elements_name(1).read_text()}'."
#     )

# def test_main_danach(): ##debug
#     IntlLogger("nice")
#     print(IntlLogger.rotating_file_handler.baseFilename)