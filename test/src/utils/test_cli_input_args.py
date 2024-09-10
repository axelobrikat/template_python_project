import pytest
from collections.abc import Callable

from src.utils.cli_input_args import CliInputArgs


@pytest.fixture(autouse=True)
def tearDown():
    """yield test
    - tearDown and reset class args of class CliInputArgs

    Yields:
        CliInputArgs: class CliInputArgs
    """
    yield

    # tearDown: set class args back to default values #
    CliInputArgs.set_cli_input_args()



def test_set_cli_args_hello():
    """test setting of CLI input args --hello
    """
    # test default value #
    assert CliInputArgs.hello == False

    # set args and test values afterwards #
    CliInputArgs.set_cli_input_args(
        verbose=False,
        quiet=False,
        hello=True,
    )
    assert CliInputArgs.hello == True


@pytest.mark.parametrize(
    "test_case,input,get_cli_input_class_arg", [
        ("Set verbosity to verbose",{"verbose": True, "quiet": False}, lambda: CliInputArgs.verbose),
        ("Set verbosity to quiet",{"verbose": False, "quiet": True}, lambda: CliInputArgs.quiet),
    ]
)
def test_set_cli_args_verbosity(test_case: str, input: str, get_cli_input_class_arg: Callable):
    """test setting of CLI input args regarding verbosity (i.e. -v, -q)
    - note, parameterized test
    """
    # test default value #
    assert get_cli_input_class_arg() == False

    # act #
    CliInputArgs.set_cli_input_args(
        verbose=input["verbose"],
        quiet=input["quiet"],
        hello=False,
    )

    # assert #
    assert get_cli_input_class_arg() == True, \
        f"Test Case '{test_case}' failed."
