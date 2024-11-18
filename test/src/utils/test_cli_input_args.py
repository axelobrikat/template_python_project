import logging
import pytest
from collections.abc import Callable

from src.utils.cli_input_args import CLI


@pytest.fixture(autouse=True)
def tearDown():
    """yield test
    - tearDown and reset class args of class CLI

    Yields:
        CLI: class CLI
    """
    yield

    # tearDown: set class args back to default values #
    CLI.set_cli_input_args()


def test_set_cli_args_hello():
    """test setting of CLI input args --hello
    """
    # test default value #
    assert CLI.hello == False

    # set args and test values afterwards #
    CLI.set_cli_input_args(
        v=False,
        q=False,
        hello=True,
    )
    assert CLI.hello == True


@pytest.mark.parametrize(
    "test_case,input,get_cli_input_class_arg",
    [
        (
            "Test case 1: Set verbosity to verbose",
            {"v": True, "V": False, "q": False, "Q": False},
            lambda: CLI.v,
        ),
        (
            "Test case 2: Set verbosity to more verbose",
            {"v": False, "V": True, "q": False, "Q": False},
            lambda: CLI.V,
        ),
        (
            "Test case 3: Set verbosity to quiet",
            {"v": False, "V": False, "q": True, "Q": False},
            lambda: CLI.q,
        ),
        (
            "Test case 4: Set verbosity to more quiet",
            {"v": False, "V": False, "q": False, "Q": True},
            lambda: CLI.Q,
        ),
    ],
)
def test_set_cli_args_verbosity(test_case: str, input: str, get_cli_input_class_arg: Callable):
    """test setting of CLI input args regarding verbosity (i.e. -v, -q)
    - note, parameterized test

    Args:
        test_case (str): name of test case
        input (str): input parameters
        get_cli_input_class_arg (Callable): lambda function that returns respective class arg
    """
    # test default value (tearDown must work properly) #
    assert get_cli_input_class_arg() == False

    # act #
    CLI.set_cli_input_args(
        v=input["v"],
        V=input["V"],
        q=input["q"],
        Q=input["Q"],
        hello=False,
    )

    # assert #
    assert get_cli_input_class_arg() == True, \
        f"'{test_case}' failed."


@pytest.mark.parametrize(
    "test_case,cli_args,expected_log_level",
    [
        (
            "Test case 1: More verbose mode (-V) selected",
            {"v": False, "V": True, "q": False, "Q": False},
            logging.DEBUG,
        ),
        (
            "Test case 2: Verbose mode (-v) selected",
            {"v": True, "V": False, "q": False, "Q": False},
            logging.INFO,
        ),
        (
            "Test case 3: Quiet mode (-q) selected",
            {"v": False, "V": False, "q": True, "Q": False},
            logging.ERROR,
        ),
        (
            "Test case 4: More quiet mode (-Q) selected",
            {"v": False, "V": False, "q": False, "Q": True},
            logging.CRITICAL,
        ),
        (
            "Test case 5: Default log level (no flags set)",
            {"v": False, "V": False, "q": False, "Q": False},
            logging.WARNING,
        ),
    ],
)
def test_get_wanted_log_level(test_case: str, cli_args: dict, expected_log_level: int):
    """test getting the wanted log level based on CLI input args
    - note, parameterized test

    Args:
        test_case (str): name of the test case
        cli_args (dict): CLI arguments with flags set to True/False
        expected_log_level (int): expected log level as returned by the method
    """
    # Arrange: Directly set class attributes #
    CLI.v = cli_args["v"]
    CLI.V = cli_args["V"]
    CLI.q = cli_args["q"]
    CLI.Q = cli_args["Q"]
    CLI.hello = False

    # Act: Get the log level #
    log_level = CLI.get_wanted_log_level()

    # Assert: Verify the expected log level #
    assert log_level == expected_log_level, \
        f"'{test_case}' failed. Expected log level {expected_log_level}, got {log_level}."
