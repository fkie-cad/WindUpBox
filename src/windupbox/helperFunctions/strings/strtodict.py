# external imports
import re

# configure logging
import logging
log = logging.getLogger(__name__)


DEFAULT_DELIM = '='


def str_to_keyval(string: str, delim: str = DEFAULT_DELIM) -> list:
    """
        convert a string to a key, value pair by a delimiter such as '='
    """
    return string.split(delim, 1)


def dict_str_insert_quotes_to_values(string: str):
    """
        inserts double quotes around values in a dict format string such as {'key': value} -> {'key': 'value'}
        can be used before ast.literal_eval
    """
    regex = r"\"[ ]*:[ ]*(?P<notinquotes>[^\"{}, ]+)"
    regex_compile = re.compile(regex)

    matches = regex_compile.finditer(string, re.MULTILINE)
    matches_list = [x for x in matches]
    while len(matches_list) > 0:
        match_element = matches_list[0]
        string_not_in_quotes = match_element.groupdict()['notinquotes']
        string_replacement = f'"{string_not_in_quotes}"'
        offset_in_match = match_element.group().find(string_not_in_quotes)
        string = f'{string[:match_element.start()+offset_in_match]}{string_replacement}{string[match_element.end():]}'
        matches = regex_compile.finditer(string, re.MULTILINE)
        matches_list = [x for x in matches]

    return string
