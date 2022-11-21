# internal imports
from windupbox.windowswebsitescraper.isoscraper.isolistupdate import WindowsIsoListUpdater
from windupbox.helperFunctions.input.yesnoinput import yesnoinput

# configure logging
import logging
log = logging.getLogger(__name__)


def update(arguments):
    """
        cli function to update the list of available windows images and writes all regarding os information to the os information database
    """
    updater = WindowsIsoListUpdater()
    answer = yesnoinput('The update process takes some time due to the scraping process of the microsoft website. Are you sure you wanna continue? ')
    if not answer:
        return
    updater.update()
