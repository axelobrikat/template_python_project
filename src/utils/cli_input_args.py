class CliInputArgs():
    """class holds cli input args
    """
    hello: bool = False

    @classmethod
    def set_cli_input_args(cls, args: dict[str, str | bool | None ]):
        """set class vars

        Args:
            args (dict[str, str | bool | None ]): docopt cli input args
        """
        cls.hello = args["--hello"]
