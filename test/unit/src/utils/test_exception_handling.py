import pytest
from pytest_mock import MockerFixture
from pytest import LogCaptureFixture
import logging

from src.utils import exception_handling as exc

TEST_LOGGER_NAME: str = "test-logger"


@pytest.fixture(autouse=True)
def setUp_tearDown(mocker: MockerFixture):
    """setUp and tearDown
    - patch the logger object
    - yield the test
    - delete logger objects that have been created during testing
    - clear catched Exceptions

    Args:
        mocker (MockerFixture): pytest mocker fixture
    """
    mocker.patch.object(
        exc,
        "logger",
        logging.getLogger(TEST_LOGGER_NAME)
    )

    yield

    del logging.root.manager.loggerDict[TEST_LOGGER_NAME]
    exc.clear_catched_exceptions()


def test_clear_catched_exceptions():
    exc.EXC.append("test")
    exc.clear_catched_exceptions()
    assert len(exc.EXC) == 0

def test_log_exc(caplog: LogCaptureFixture):
    caplog.set_level(logging.ERROR)
    exc_msg = "Test Exception"
    err_msg = "Test Value Error"
    exc_info = (ValueError, ValueError(err_msg), None)
    exc.log_exc(exc_msg, exc_info)
    assert f"{exc_msg}" in caplog.text
    assert f"{err_msg}" in caplog.text

def test_process_exc():
    exc_msg = "Test Exception"
    with pytest.raises(Exception, match=fr"{exc_msg}"):
        exc.raise_exception(exc_msg)
    assert len(exc.EXC) == 1

def test_program_end_without_exceptions(caplog: LogCaptureFixture):
    caplog.set_level(logging.WARNING)
    exc.program_end()
    assert caplog.text.strip().endswith("Program ends..")
    
def test_program_end_with_exception(caplog: pytest.LogCaptureFixture):
    caplog.set_level(logging.WARNING)
    exc_msg = "Test Exception"
    err_msg = "Test Error"
    exc_info = (ValueError, ValueError(err_msg), None)
    exc.EXC.append([exc_msg, exc_info])
    exc.program_end()
    assert "Program ends.." in caplog.text
    assert "Roundup of catched exceptions" in caplog.text
    assert f"{exc_msg}" in caplog.text
