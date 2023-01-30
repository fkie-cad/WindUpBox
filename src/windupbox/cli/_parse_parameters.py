# external imports
from pathlib import Path

# internal imports
from windupbox.helperFunctions.strings.strtolist import str_to_list
from windupbox.osinfo.windowsinfo import WindowsInfo
from windupbox.helperFunctions.strings.strtodict import str_to_keyval
from windupbox.osinfo.database import print_table, return_if_exists
from windupbox.windowswebsitescraper.bcp47scraper.search import check_bcp47_code, language_to_bcp47
from windupbox.helperFunctions.input.listselectioninput import listselectinput
from windupbox.helperFunctions.input.yesnoinput import yesnoinput
from windupbox.boxcreator.provided.windows import WindowsBoxCreator

# configure logging
import logging
log = logging.getLogger(__name__)


def parse_osinfo_argument(os_info_string: str) -> tuple:
    """
        parse string with os information to list of arguments and dict of keyword arguments
        (e.g. (1,x=2,y=3) will be parsed to arguments=[1] and keyword_arguments={'x':2,'y':3}
    """
    arg_list = str_to_list(os_info_string, delim=[','], start_chars=['[', '('], end_chars=[']', ')'])
    keyword_arguments = dict()
    arguments = []
    for position, entry in enumerate(arg_list):
        if '=' in entry:
            key, val = str_to_keyval(entry, delim='=')
            keyword_arguments[key] = val
        else:
            arguments.append((position, entry))
    return arguments, keyword_arguments


def parse_windows_info_string_to_dict(os_info_string: str) -> dict:
    """
        parse string with os information to a dictionary
    """
    windows_info_dict = dict()
    windows_info_attribute_list = WindowsInfo.get_mandatory_attributes()
    args, keyword_args = parse_osinfo_argument(os_info_string)
    for arg in args:
        key = windows_info_attribute_list[arg[0]]
        windows_info_dict[key] = arg[1]
    windows_info_dict.update(keyword_args)

    for key in windows_info_dict.keys():
        if not hasattr(WindowsInfo, key):
            log.warning(f'attribute {key} does not exist in the windows info class -> will be therefore ignored')
            del windows_info_dict[key]

    return windows_info_dict


def filter_available_osinfo(os_info_string: str):
    """
        print available os information by using filter data provided in os information string
    """
    windows_info_dict = parse_windows_info_string_to_dict(os_info_string)
    print_table(filters=windows_info_dict)


def parse_windows_info_string_to_instance(os_info_string: str) -> WindowsInfo:
    """
        parse string with os information to an instance of the WindowsInfo class
    """
    windows_info_dict = parse_windows_info_string_to_dict(os_info_string)
    windows_info = WindowsInfo.from_dict(windows_info_dict)
    return windows_info


def get_windowsinfo_if_valid(os_info_string: str) -> WindowsInfo or None:
    """
        check whether os information provided in an os information string contains all data for a valid WindowsInfo file.
        If so an instance of the class with the data will be returned and if not None.
    """
    windows_info = parse_windows_info_string_to_instance(os_info_string)
    missing_attributes = windows_info.return_missing_attributes()
    if not missing_attributes:
        return windows_info
    else:
        print(f'the attributes {missing_attributes} are missing \n')
    return None


def get_windowsinfo_for_creation(os_info_string: str) -> WindowsInfo or None:
    """
       parse string with os information to an instance of the WindowsInfo class and checks whether all data for a valid WindowsInfo file are there.
       If so an instance of the class with the data will be returned and if not None.
    """
    windows_info = get_windowsinfo_if_valid(os_info_string)
    if not return_if_exists(windows_info):
        print(f'the chosen os does not exist in database')
        return None
    if not windows_info:
        print(f'your options for the chosen os info are the following:')
        filter_available_osinfo(os_info_string)
        print(f'\n')
        return None
    return windows_info

def determine_bcp47(arguments, windows_info: WindowsInfo) -> str or None:
    bcp47 = None
    if arguments.bcp47:
        if check_bcp47_code(arguments.bcp47):
            bcp47 = arguments.bcp47
        else:
            log.error(f'the provided bcp47 code {arguments.bcp47} does not exist')
    else:
        log.info(f'no bcp47 provided')
    if not bcp47:
        possible_bcp_codes = language_to_bcp47(windows_info.language)
        if not possible_bcp_codes:
            log.error(
                f'no bcp47 code for language {windows_info.language} could be found -> therefore no box can be created')
            return None
        if len(possible_bcp_codes) == 1:
            bcp47 = possible_bcp_codes[0]
            message = f'the tool suggest to use the bcp47 code {bcp47}. If you want to continue with this bcp47 code, ' \
                      f'press yes if not press no and restart the tool with the -bcp option to specify the bcp47 code '
            result = yesnoinput(message)
            if not result:
                return None
        else:
            str_stop = 'stop the tool'
            options = possible_bcp_codes + [str_stop]
            message = f'\nFor your chosen language multiple bcp47 codes are suggested - please choose one. '
            result = listselectinput(message, options)
            if result == str_stop:
                return None
            else:
                bcp47 = result
    return bcp47



