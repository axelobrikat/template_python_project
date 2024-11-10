class CLI():
    """class holds cli input args
    """
    v: bool = False
    V: bool = False
    q: bool = False
    Q: bool = False
    hello: bool = False

    @classmethod
    def set_cli_input_args(
        cls,
        v: bool = False,
        V: bool = False,
        q: bool = False,
        Q: bool = False,
        hello: bool = False,
    ):
        """set class vars

        Args:
            v (bool, optional): run program with verbose output. Defaults to False.
            V (bool, optional): run program with more verbose output. Defaults to False.
            q (bool, optional): run program with quiet output. Defaults to False.
            Q (bool, optional): run program with more quiet output. Defaults to False.
            hello (bool, optional): hello-world. Defaults to False.
        """        
        cls.v = v
        cls.V = V
        cls.q = q
        cls.Q = Q
        cls.hello = hello
