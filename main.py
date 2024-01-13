"""
Purpose:
    - Python Project Template which includes
      - project structure
      - test stucture using pytest and coverage
      - configured logging, arg parsing and exception handling
      - .gitignore
      - LICENSE
      - README.md
      - requirements.txt

Usage:
    main.py [--hello]

Options:
    --hello        print "Hello World!"
"""
from docopt import docopt
from pathlib import Path
import os
import sys

from src.utils.cli_input_args import CliInputArgs

# global vars #
ROOT: Path = Path(os.path.dirname(sys.executable)) if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
"""path of root dir of repo"""


def main():
    """
    - get and process CLI input args
    - and start program
    """
    # get CLI input args #
    CliInputArgs.set_cli_input_args(docopt(__doc__))

    print(docopt(__doc__))
    print("Hello World!")


if __name__=="__main__":
    main()
