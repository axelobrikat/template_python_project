import pytest
from pytest import LogCaptureFixture

from src.utils import exception_handling as exc

def test_clear_catched_exceptions():
    exc.EXC.append("test")
    exc.clear_catched_exceptions()
    assert len(exc.EXC) == 0

def test_log_exc(caplog: LogCaptureFixture):
    exc_msg = "Test Exception"
    err_msg = "Test Value Error"
    exc_info = (ValueError, ValueError(err_msg), None)
    exc.log_exc(exc_msg, exc_info)
    assert f"{exc_msg}" in caplog.text
    assert f"{err_msg}" in caplog.text

def test_process_exc():
    exc.clear_catched_exceptions()
    exc_msg = "Test Exception"
    with pytest.raises(Exception, match=fr"{exc_msg}"):
        exc.raise_exception(exc_msg)
    assert len(exc.EXC) == 1

def test_program_end_without_exceptions(caplog: LogCaptureFixture):
    exc.clear_catched_exceptions()
    exc.program_end()
    assert caplog.text.strip().endswith("Program ends..")
    
def test_program_end_with_exception(caplog: pytest.LogCaptureFixture):
    exc.clear_catched_exceptions()
    exc_msg = "Test Exception"
    err_msg = "Test Error"
    exc_info = (ValueError, ValueError(err_msg), None)
    exc.EXC.append([exc_msg, exc_info])
    exc.program_end()
    assert "Program ends.." in caplog.text
    assert "Roundup of catched exceptions" in caplog.text
    assert f"{exc_msg}" in caplog.text
