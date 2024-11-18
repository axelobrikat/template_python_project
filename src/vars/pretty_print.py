from pathlib import Path
import logging


SEPARATOR: str = "========================================"
"""returns a line that acts as a visual separator"""


def log_exec_start_msg():
    """log a debug msg for program execution start
    """
    logging.debug((
        f"Program execution starts.\n"
        f"Logging and Input Arguments configured successfully.\n"
        f"{SEPARATOR}\n"
        f"{SEPARATOR}\n\n"
    ))
