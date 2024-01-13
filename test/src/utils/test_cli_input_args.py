import pytest

from src.utils.cli_input_args import CliInputArgs


@pytest.fixture
def default_args() -> dict:
    """return default cli input args after from docopt

    Returns:
        dict: default cli input args
    """
    return {
        '-v': False,
        '-q': False,
        '--hello': False,
    }


def test_set_cli_args_hello(default_args: dict):
    """test setting of CLI input args --hello
    """
    default_args['--hello'] = True

    # test default value #
    assert CliInputArgs.hello == False

    # set args and test values afterwards #
    CliInputArgs.set_cli_input_args(default_args)
    assert CliInputArgs.hello == True

def test_set_cli_args_v(default_args: dict):
    """test setting of CLI input args -v
    """
    default_args['-v'] = True

    # test default value #
    assert CliInputArgs.verbose == False

    # set args and test values afterwards #
    CliInputArgs.set_cli_input_args(default_args)
    assert CliInputArgs.verbose == True

def test_set_cli_args_q(default_args: dict):
    """test setting of CLI input args -q
    """
    default_args['-q'] = True

    # test default value #
    assert CliInputArgs.quiet == False

    # set args and test values afterwards #
    CliInputArgs.set_cli_input_args(default_args)
    assert CliInputArgs.quiet == True
