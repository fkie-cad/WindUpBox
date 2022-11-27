# internal imports
from windupbox.osinfo.database import print_table, return_if_exists
from windupbox.osinfo.database_modifications import add_windowsinfo_to_database, remove_windowsinfo_to_database, set_tested
from windupbox.osinfo.windowsinfo import WindowsInfo
from windupbox.windowswebsitescraper.isoscraper.isolistupdate import WindowsIsoListUpdater
from windupbox.helperFunctions.input.yesnoinput import yesnoinput
from ._parse_parameters import get_windowsinfo_if_valid, parse_osinfo_argument

# configure logging
import logging
log = logging.getLogger(__name__)


def os_list(arguments, parser):
    """
        cli function to list available os by filtering the output and selecting certain columns
    """
    if arguments.filter or arguments.select_columns:
        filter_dict = dict()
        select_list = []
        if arguments.filter:
            args, filter_dict = parse_osinfo_argument(arguments.filter)
            for arg in args:
                log.warning(f'filter {arg} get ignored - os list --filter needs keyword value pairs in the following format "key=value" to filter successfully')
        if arguments.select_columns:
            select_list += list(filter_dict.keys())
            args, keyword_args = parse_osinfo_argument(arguments.select_columns)
            for arg in args:
                if hasattr(WindowsInfo, arg[1]):
                    select_list.append(arg[1])
                else:
                    log.warning(f'windows info class does not have the attribute {arg[1]} -> this attribute will be therefore be ignored')
            select_list += list(keyword_args.keys())
        print_table(select=select_list, filters=filter_dict)
    elif arguments.show_all:
        print_table()
    else:
        parser.print_help()


def os_add(arguments):
    """
        cli function to add os information to the os information database
    """
    windows_info = get_windowsinfo_if_valid(arguments.windows_info)
    if not windows_info:
        log.error('os information can not be added to database due to missing attributes in the provided windows info')
        return
    instances = return_if_exists(windows_info)
    if instances:
        log.error(f'os information can not be added to database because the entry for {windows_info} does already exist in database')
        return
    add_windowsinfo_to_database(windows_info)


def os_remove(arguments):
    """
        cli function to remove os information from the os information database
    """
    windows_info = get_windowsinfo_if_valid(arguments.windows_info)
    if not windows_info:
        log.error('os information can not be removed from database due to missing attributes in the provided windows info')
        return
    instances = return_if_exists(windows_info)

    if not instances:
        log.warning(f'os information can not be removed because no entry for {windows_info} exist in database')
        return
    for inst in instances:
        remove_windowsinfo_to_database(inst)


def os_set_tested(arguments):
    """
        cli function to set an os information to tested in the os information database
    """
    windows_info = get_windowsinfo_if_valid(arguments.windows_info)
    if not windows_info:
        log.error('os can not be set to tested in database due to missing attributes in the provided windows info')
        return
    set_tested(windows_info)


def os_update(arguments):
    """
        cli function to update the list of available windows images and writes all regarding os information to the os information database
    """
    updater = WindowsIsoListUpdater()
    answer = yesnoinput(
        'The update process takes some time due to the scraping process of the microsoft website. Are you sure you wanna continue? ')
    if not answer:
        return
    updater.update()

