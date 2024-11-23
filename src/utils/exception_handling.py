"""
TODO:
  - work through exception handling
  - log_exc does not log exception, raise_exception does but never enters program_end func
"""
import sys
import logging


from src.log.log import configure_logger
from src.vars.pretty_print import SEPARATOR

logger = logging.getLogger(__name__)
logger = configure_logger(logger)


EXC: list[list] = []
"""stores all occured exception messages [[exc_msg: str, exc_info: tuple[type[BaseException], BaseException, TracebackType]]]"""


def clear_catched_exceptions():
    """clear the list of catched exceptions
    """
    global EXC
    EXC = []

def log_exc(exc_msg: str, exc_info, store_exc_info: bool = True):
    """log exception using logging.exception
    - save exception info if wanted

    Args:
        exc_msg (str): exception message
        exc_info (_OptExcInfo): exception info
        store_exc_info (bool): indicates whether to store exc info or not.
            ... Defaults to True.
    """
    if store_exc_info:
        global EXC
        EXC.append([exc_msg, exc_info])
    logger.exception(
        f"\n"
        f"{SEPARATOR}\n"
        f"{SEPARATOR}\n"
        f"{exc_msg}\n"
        f"{SEPARATOR}\n"
        f"{SEPARATOR}",
        exc_info=exc_info
    )

def program_end():
    """when program exits, output all catched exceptions as roundup
    """        
    logger.warning((
        f"\n{SEPARATOR}"
        f"\n{SEPARATOR}"
        f"\n\nProgram ends.."
    ))
    if EXC:
        logger.warning(f"Roundup of catched exceptions (ordered by time):\n")
        for exc in EXC:
            log_exc(exc[0], exc[1], store_exc_info=False)
