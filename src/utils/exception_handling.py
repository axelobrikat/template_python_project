import sys
import logging

from src.vars.pretty_print import SEPARATOR


EXC: list[list] = []
""""stores all occured exception messages [[exc_msg: str, exc_info: tuple[type[BaseException], BaseException, TracebackType]]]"""


def clear_catched_exceptions():
    """clear the list of catched exceptions
    """
    global EXC
    EXC = []

def log_exc(exc_msg: str, exc_info):
    """log exception using logging.exception

    Args:
        exc_msg (str): exception message
        exc_info (_OptExcInfo): exception info
    """
    logging.exception(
        f"\n"
        f"{SEPARATOR}\n"
        f"{SEPARATOR}\n"
        f"{exc_msg}\n"
        f"{SEPARATOR}\n"
        f"{SEPARATOR}",
        exc_info=exc_info
    )

def process_exc(exc_msg: str="EXCEPTION occured"):
    """get exc info, append to global var EXC and log exc

    Args:
        exc_msg (str, optional): exception message. Defaults to "EXCEPTION occured".
    """
    global EXC
    exc_info = sys.exc_info()
    EXC.append([exc_msg, exc_info])
    log_exc(exc_msg, exc_info)

def raise_exception(exc_msg: str):
    """raise exception to exit the program immediately
    - works within try-except to be able of logging the raised Exception
    - depending on usage, second raise can also get catched by outer try-except

    Args:
        exc_msg (str): exception message

    Raises:
        Exception: raise Exception, log error that occured and exit program
    """
    try:
        raise Exception(exc_msg)
    except Exception:
        process_exc(f"EXCEPTION raised: {exc_msg}")
        raise # for process termination, raise last exception again without catching
    
def program_end():
    """when program exits, output all catched exceptions as roundup
    """        
    logging.warning((
        f"\n{SEPARATOR}"
        f"\n{SEPARATOR}"
        f"\n\nProgram ends.."
    ))
    if EXC:
        logging.warning(f"Roundup of catched exceptions (ordered by time):\n")
        for exc in EXC:
            log_exc(exc[0], exc[1])
            # logging.exception(f"\n\n-----> {exc[0]} <-----", exc_info=exc[1])
