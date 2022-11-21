# configure logging
import logging
log = logging.getLogger(__name__)


def replace_multiple_strings(string, characters, replacement):
    """
        replace multiple characters in a string with one other char (replacement)
    """
    for c in characters:
        string = string.replace(c, replacement)
    return string
