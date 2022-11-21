# external imports


# internal imports


# configure logging
import logging
log = logging.getLogger(__name__)


def find_uilanguage_forinstallation(bcp47: str) -> str:
    """
        find a language usable for the installation (UILanguage field in Microsoft-Windows-International-Core-WinPE part of Autounattend file)
    """
