# configure logging
import logging
log = logging.getLogger(__name__)

DEFAULT_DELIM = [',']
START_CHARS = ['[']
END_CHARS = [']']
IGNORE_CHARS = [' ']


def str_to_list(string: str, delim: list = None, start_chars: list = None, end_chars: list = None, ignore_chars: list = None) -> list:
    """
        converts a string into a list

        :param string: string to convert
        :param delim: possible delimiter between elements of the list
        :param start_chars: starting characters allowed
        :param end_chars: ending characters allowed
        :param ignore_chars: chars to be ignored
    """
    if not delim:
        delim = DEFAULT_DELIM
    if not start_chars:
        start_chars = START_CHARS
    if not end_chars:
        end_chars = END_CHARS
    if not ignore_chars:
        ignore_chars = IGNORE_CHARS

    for char in start_chars:
        if string[0:len(char)] == char:
            string = string[len(char):]
            break

    for char in end_chars:
        if string[-len(char):] == char:
            string = string[:-len(char)]
            break

    max_occurance = -1
    max_occurance_char = None
    for char in delim:
        x = string.count(char)
        if x > max_occurance:
            max_occurance = x
            max_occurance_char = char

    split_string = string.split(max_occurance_char)
    split_string_cleaned = []
    for string in split_string:
        string_cleaned = string
        if string[0] in IGNORE_CHARS:
            string_cleaned = string[1:]
        elif len(string) >= 2 and string[-1] in IGNORE_CHARS:
            string_cleaned = string[:-1]
        split_string_cleaned.append(string_cleaned)
    return split_string_cleaned

