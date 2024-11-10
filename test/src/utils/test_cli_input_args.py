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
            {"v": True, "vv": False, "q": False, "qq": False},
            lambda: CLI.v,
        ),
        (
            "Test case 2: Set verbosity to more verbose",
            {"v": False, "vv": True, "q": False, "qq": False},
            lambda: CLI.vv,
        ),
        (
            "Test case 3: Set verbosity to quiet",
            {"v": False, "vv": False, "q": True, "qq": False},
            lambda: CLI.q,
        ),
        (
            "Test case 4: Set verbosity to more quiet",
            {"v": False, "vv": False, "q": False, "qq": True},
            lambda: CLI.qq,
        ),
    ],
)
def test_set_cli_args_verbosity(test_case: str, input: str, get_cli_input_class_arg: Callable):
    """test setting of CLI input args regarding verbosity (i.e. -v, -q)
    - note, parameterized test
    """
    # test default value (tearDown must work properly) #
    assert get_cli_input_class_arg() == False

    # act #
    CLI.set_cli_input_args(
        v=input["v"],
        vv=input["vv"],
        q=input["q"],
        qq=input["qq"],
        hello=False,
    )

    # assert #
    assert get_cli_input_class_arg() == True, \
        f"'{test_case}' failed."
