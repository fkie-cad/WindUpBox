# configure logging
import logging
log = logging.getLogger(__name__)


DEFAULT_DELIM = '='


def str_to_keyval(string: str, delim: str = DEFAULT_DELIM) -> list:
    """
        convert a string to a key, value pair by a delimiter such as '='
    """
    return string.split(delim, 1)
