# internal imports
from windupbox.boxcreator.provided import *
from windupbox.boxcreator.custom import *
from windupbox.osinfo.windowsinfo import WindowsInfo

# configure logging
import logging
log = logging.getLogger(__name__)


def select_boxcreator_by_windows_info(windows_info: WindowsInfo) -> WindowsBoxCreator or None:
    """
        finds the best matching boxcreator class by their box_creator_info attribute.
        therefore if two matches are found the more precise on are used.
        So for instance if the filter of a boxcreator class B1 includes only windows_version and version and
        a filter of a boxcreator class B2 includes additionally the edition and both filters match the boxcreator class B2 will be used.
    """
    boxcreators = WindowsBoxCreator.__subclasses__()
    matching_boxcreators = dict()
    for boxcreator in boxcreators:
        if boxcreator.os_info_filter:
            match_level = boxcreator.os_info_filter.match(windows_info)
            if match_level > 0:
                if match_level not in matching_boxcreators.keys():
                    matching_boxcreators[match_level] = boxcreator
                else:
                    log.error(f'two boxcreators with same level found -> {matching_boxcreators[match_level]} will be used and {boxcreator} will be ignored ')
    boxcreator = None
    max_level = 0
    for key in matching_boxcreators.keys():
        if int(key) > max_level:
            boxcreator = matching_boxcreators[key]
            max_level = int(key)
    return boxcreator

