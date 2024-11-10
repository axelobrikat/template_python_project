class CLI():
    """class holds cli input args
    """
    v: bool = False
    vv: bool = False
    q: bool = False
    qq: bool = False
    hello: bool = False

    @classmethod
    def set_cli_input_args(
        cls,
        v: bool = False,
        vv: bool = False,
        q: bool = False,
        qq: bool = False,
        hello: bool = False,
    ):
        """set class vars

        Args:
            v (bool, optional): run program with verbose output. Defaults to False.
            vv (bool, optional): run program with more verbose output. Defaults to False.
            q (bool, optional): run program with quiet output. Defaults to False.
            qq (bool, optional): run program with more quiet output. Defaults to False.
            hello (bool, optional): hello-world. Defaults to False.
        """        
        cls.v = v
        cls.vv = vv
        cls.q = q
        cls.qq = qq
        cls.hello = hello
