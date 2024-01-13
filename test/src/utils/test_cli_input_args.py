from src.utils.cli_input_args import CliInputArgs


def test_set_cli_args_hello():
    """test setting of CLI input args --hello
    """
    args: dict = {
        '--hello': True,
    }

    # test default value #
    assert CliInputArgs.hello == False

    # set args and test values afterwards #
    CliInputArgs.set_cli_input_args(args)
    assert CliInputArgs.hello == True
