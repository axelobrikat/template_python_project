class CliInputArgs():
    """class holds cli input args
    """
    verbose: bool = False
    quiet: bool = False
    hello: bool = False

    @classmethod
    def set_cli_input_args(
        cls,
        verbose: bool = False,
        quiet: bool = False,
        hello: bool = False,
    ):
        """set class vars

        Args:
            verbose (bool, optional): run program with verbose output. Defaults to False.
            quiet (bool, optional): run program with quiet output. Defaults to False.
            hello (bool, optional): hello-world. Defaults to False.
        """        
        cls.verbose = verbose
        cls.quiet = quiet
        cls.hello = hello
