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
        verbose=False,
        quiet=False,
        hello=True,
    )
    assert CLI.hello == True


@pytest.mark.parametrize(
    "test_case,input,get_cli_input_class_arg", [
        ("Set verbosity to verbose",{"verbose": True, "quiet": False}, lambda: CLI.verbose),
        ("Set verbosity to quiet",{"verbose": False, "quiet": True}, lambda: CLI.quiet),
    ]
)
def test_set_cli_args_verbosity(test_case: str, input: str, get_cli_input_class_arg: Callable):
    """test setting of CLI input args regarding verbosity (i.e. -v, -q)
    - note, parameterized test
    """
    # test default value #
    assert get_cli_input_class_arg() == False

    # act #
    CLI.set_cli_input_args(
        verbose=input["verbose"],
        quiet=input["quiet"],
        hello=False,
    )

    # assert #
    assert get_cli_input_class_arg() == True, \
        f"Test Case '{test_case}' failed."
