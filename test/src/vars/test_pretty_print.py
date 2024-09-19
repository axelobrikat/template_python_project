import logging
import pytest
from pytest import LogCaptureFixture
from pathlib import Path

from src.vars.pretty_print import SEPARATOR, log_exec_start_msg


def test_separator():
    assert SEPARATOR == 40*"="


@pytest.mark.parametrize(
    "test_case, log_level", [
        ("1: DEBUG", logging.DEBUG),
        ("3: INFO", logging.INFO),
        ("2: WARNING", logging.WARNING),
        ("4: ERROR", logging.ERROR),
        ("5: CRITICAL", logging.CRITICAL),
    ]
)
def test_log_exec_start_msg(caplog: LogCaptureFixture, test_case: str, log_level: int):
    """test func log_exec_start_msg
    - assert correct log

    Args:
        caplog (LogCaptureFixture): pytest fixture to capture logging
        test_case (str): test case name
        log_level (int): log level
    """
    # arrage #
    caplog.set_level(log_level)
    dummy_path: Path = Path(".")

    # act #
    log_exec_start_msg(dummy_path)

    # assert #
    if log_level == logging.DEBUG:
        assert f"Program execution starts." in caplog.text, \
            f"test case '{test_case}' failed."
        assert f"Logging and Input Arguments configured successfully." in caplog.text, \
            f"test case '{test_case}' failed."
        assert f"Log rotation of log files '{dummy_path}.<x>' performed succesfully." in caplog.text, \
            f"test case '{test_case}' failed."
        assert f"{SEPARATOR}" in caplog.text, \
            f"test case '{test_case}' failed."
    else:
        assert "" == caplog.text, \
            f"test case '{test_case}' failed."
