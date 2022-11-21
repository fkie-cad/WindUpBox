import logging

# set DEBUG mode
DEBUG = False

# set program details
NAME = 'fwinpacker'
VERSION = '1.0.0'

# timestamp format
TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'

# LOGGING DEFAULTS
if DEBUG:
    LOGLEVEL_CONSOLE_DEFAULT = logging.INFO
    LOGLEVEL_FILE_DEFAULT = logging.DEBUG
else:
    LOGLEVEL_CONSOLE_DEFAULT = logging.WARNING
    LOGLEVEL_FILE_DEFAULT = logging.INFO

CONSOLEHANDLER = '%(levelprefix)s %(name)s - %(message)s'
CONSOLEHANDLER_SHORT = '%(levelprefix)s %(message)s'
FILEHANDLER = '[%(asctime)s]: %(name)s: %(levelname)s - %(message)s'

DEFAULTLOGFILE = f"{NAME}.log"
ABBREV_DEBUG = ['DEBUG', 'debug', 'Debug', 'd', 'D']
ABBREV_INFO = ['INFO', 'info', 'Info', 'i', 'I']
ABBREV_WARNING = ['WARNING', 'warning', 'Warning', 'w', 'W']
ABBREV_ERROR = ['ERROR', 'error', 'Error', 'e', 'E']
ABBREV_CRITICAL = ['CRITICAL', 'critical', 'Critical', 'c', 'C']

