# internal imports
from windupbox.config import VERSION

# configure logging
import logging
log = logging.getLogger(__name__)


def show_version(arguments, parser):
    """
        cli function to show the program version
    """
    if arguments.version:
        print(f'Version {VERSION}')
    else:
        parser.print_help()
