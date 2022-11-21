# external imports
import uuid
import requests
from pyquery import PyQuery as pq
import json
from pathlib import Path
import pkg_resources

# internal imports
from windupbox.osinfo.windowsinfo import WindowsInfo
from windupbox.windowswebsitescraper.isoscraper.constants import *
from windupbox.helperFunctions.web.download import download

# configure logging
import logging
log = logging.getLogger(__name__)


WINDOWS_ISO_FILE = Path(pkg_resources.resource_filename('windupbox', 'data/windows_download_possibilities.json'))


class WindowsDownloadLinkCreator:

    def __init__(self, windows_info: WindowsInfo):
        self.windows_info = windows_info
        self.windowsversion_id = WINDOWS_VERSION_IDENT_MAPPING[self.windows_info.windows_version]

    def check_if_link_creation_is_possible(self):
        pass

    def _check_response_for_blocked_error(self, response: bytes) -> bool:
        query = pq(response)
        select_error_message = query('#errorModalMessage')
        if select_error_message:
            log.error(f'error message "{select_error_message.text()}" during getting windows download link occured \n '
                      f'(most likely due to many requests to the microsoft website - wait some time or use a VPN will fix this)')
            return False
        return True

    def get_link(self):
        pass

    def get_supported_languages_and_architectures(self):
        pass


class WindowsDownloadLinkCreatorStatic(WindowsDownloadLinkCreator):

    def __init__(self, windows_info: WindowsInfo):
        super().__init__(windows_info)
        self.links_mapping = WINDOWS_LINK_MAPPING[self.windows_info.windows_version]

    def check_if_link_creation_is_possible(self) -> bool:
        if not self.links_mapping:
            return False
        try:
            self.links_mapping[self.windows_info.version]['editions'][self.windows_info.edition]
        except (KeyError, AttributeError):
            return False
        return True

    def _get_link_dict_by_windows_version_version_edition(self):
        version_info = self.links_mapping[self.windows_info.version]
        editions = version_info['editions']
        link_dict = editions[self.windows_info.edition]
        return link_dict

    def get_link(self) -> str:
        if not self.check_if_link_creation_is_possible():
            return ''
        link_dict = self._get_link_dict_by_windows_version_version_edition()
        download_link = link_dict[self.windows_info.architecture]
        return download_link

    def get_supported_languages_and_architectures(self) -> dict:
        if not self.check_if_link_creation_is_possible():
            return {}
        link_dict = self._get_link_dict_by_windows_version_version_edition()
        supported_architectures = list(link_dict.keys())
        return {
            'English': supported_architectures
        }

class WindowsDownloadLinkCreatorDynamic(WindowsDownloadLinkCreator):

    def __init__(self, windows_info: WindowsInfo):
        super().__init__(windows_info)
        self.code_mapping = WINDOWS_CODE_MAPPING[self.windows_info.windows_version]

    def check_if_link_creation_is_possible(self):
        if not self.code_mapping:
            return False
        try:
            self.code_mapping[self.windows_info.version]['editions'][self.windows_info.edition]
        except (KeyError, AttributeError):
            return False
        return True

    def get_link(self) -> str:
        if not self.check_if_link_creation_is_possible():
            return ''
        session_id = str(uuid.uuid4())
        code = self._determine_code_for_windows_info()
        language_code_dict = self._scrap_possible_languages(session_id, code)
        language_code = self._select_language(language_code_dict)
        return self._scrap_download_link(session_id, self.windows_info.language, language_code)

    def _determine_code_for_windows_info(self) -> int or None:
        try:
            version_info = self.code_mapping[self.windows_info.version]
        except KeyError:
            log.error(f'version {self.windows_info.version} of {self.windows_info.windows_version} does not exist or is not supported')
            return None
        editions = version_info['editions']
        try:
            code = editions[self.windows_info.edition]
        except KeyError:
            log.error(f'edition {self.windows_info.edition} does not exist or is not supported for {self.windows_info.windows_version} in version {self.windows_info.version}')
            return None
        return code

    def _scrap_possible_languages(self, session_id: str, code: int or str) -> dict:
        language_selection_url = r"https://www.microsoft.com/en-us/api/controls/contentinclude/html?"\
            fr"pageId={LANGUAGE_SELECTION_PAGE_ID}&"\
            r"host=www.microsoft.com&"\
            fr"segments=software-download%2c{self.windowsversion_id}&"\
            r"query=&"\
            r"action=getskuinformationbyproductedition&"\
            fr"sessionId={session_id}&"\
            fr"productEditionId={code}&"\
            r"sdVersion=2"

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Referer": fr'https://www.microsoft.com/software-download/{self.windowsversion_id}'
        }
        payload = r"controlAttributeMapping:"
        req = requests.post(language_selection_url, data=payload, headers=headers)
        query = pq(req.content)
        language_select = query('#product-languages')
        language_id_dict = {}
        for opt in language_select.children():
            values = opt.values()[0]
            if values:
                x = json.loads(values)
                language_id_dict[x['language']] = x['id']
        return language_id_dict

    def _select_language(self, language_code_dict: dict) -> str:
        languages = list(language_code_dict.keys())
        if self.windows_info.language not in languages:
            log.error(f'language {self.windows_info.language} is not a option for {self.windows_info.windows_version} {self.windows_info.edition} in version {self.windows_info.version}')
            return ''
        return language_code_dict[self.windows_info.language]

    def _scrap_download_link(self, session_id: str, language: str, language_code: int or str, return_possible_architectures_instead=False) -> str or list:
        download_url = r"https://www.microsoft.com/en-us/api/controls/contentinclude/html?" \
                       fr"pageId={DOWNLOAD_PAGE_ID}&" \
                       fr"host=www.microsoft.com&segments=software-download,{self.windowsversion_id}&" \
                       r"query=&" \
                       r"action=GetProductDownloadLinksBySku&" \
                       fr"sessionId={session_id}&" \
                       fr"skuId={str(language_code)}&" \
                       fr"language={language}&" \
                       r"sdVersion=2"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Referer": fr'https://www.microsoft.com/software-download/{self.windowsversion_id}'
        }
        payload = r"controlAttributeMapping:"
        req = requests.post(download_url, data=payload, headers=headers)
        if not self._check_response_for_blocked_error(req.content):
            return ''
        query = pq(req.content)
        buttons = query('.button, .button-long, .button-flat, .button-purple')
        supported_architectures = dict()
        for b in buttons:
            try:
                download_url = b.attrib['href']
            except KeyError:
                continue
            arch = [x.text for x in b.getchildren()][0]
            if arch in ARCHITECTURE_MAPPING.keys():
                supported_architectures[ARCHITECTURE_MAPPING[arch]] = download_url
        self.supported_architectures = list(supported_architectures.keys())
        if supported_architectures:
            if return_possible_architectures_instead:
                return list(supported_architectures.keys())
            return supported_architectures[self.windows_info.architecture]
        return ''

    def get_supported_languages_and_architectures(self) -> dict:
        supported_language_and_architectures = dict()
        if not self.check_if_link_creation_is_possible():
            return supported_language_and_architectures
        session_id = str(uuid.uuid4())
        code = self._determine_code_for_windows_info()
        language_code_dict = self._scrap_possible_languages(session_id, code)
        for language in language_code_dict.keys():
            architectures = [
                'x64',
                'x86'
            ]
            supported_language_and_architectures[language] = architectures
        return supported_language_and_architectures


class WindowsDownloader:
    windows_info: WindowsInfo
    download_link_creator: WindowsDownloadLinkCreator or None

    def __init__(self, windows_info: WindowsInfo):
        self.windows_info = windows_info
        if self.windows_info.windows_version in ['Windows 7', 'Windows 8', 'Windows 10', 'Windows 11']:
            self.download_link_creator = WindowsDownloadLinkCreatorStatic(windows_info)
            if not self.download_link_creator.check_if_link_creation_is_possible():
                log.info(f'no static link for {windows_info} could be found - so it will be tried to create a dynamic link')
                self.download_link_creator = WindowsDownloadLinkCreatorDynamic(windows_info)
        else:
            log.error(f'{self.windows_info.windows_version} is not supported by the WindowsDownloader')
            self.download_link_creator = None

    def download_iso(self, path: Path, quiet=False) -> bool:
        if not self.download_link_creator:
            return False
        link = self.download_link_creator.get_link()
        if not link:
            return False
        download(link, path, headers={}, quiet=quiet)
        return True
