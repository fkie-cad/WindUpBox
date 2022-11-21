# external imports
from pathlib import Path
import pkg_resources
import yaml

# internal imports
from windupbox.boxcreator.boxcreator import BoxCreator
from windupbox.osinfo.windowsinfo import WindowsInfo, WindowsInfoFilter
from windupbox.windowswebsitescraper.isoscraper.isoscraper import WindowsDownloader
from windupbox.iso.iso import extract_languagecodes_from_windows_os_iso
from windupbox.packerAPI.variable import Variable, VariableStringMix

# configure logging
import logging
log = logging.getLogger(__name__)


class WindowsBoxCreator(BoxCreator):
    """
        base boxcreator class for windows boxes, that can be extended to create boxcreator classes for specific windows version, edition, ...
        the class therefore provides basic methods needed for nearly all windows boxes
    """
    os_info: WindowsInfo
    os_info_filter: WindowsInfoFilter
    product_key: str or None = None

    def __init__(self, boxdirectory: Path, os_info: WindowsInfo):
        super(WindowsBoxCreator, self).__init__(boxdirectory, os_info)
        self._add_winrm_setting_to_source_attr()
        self._set_guest_os_type()

    def _is_tested(self) -> bool:
        """
            checks whether the used boxcreator class is marked as tested in a provided dataset
        """
        with open(pkg_resources.resource_filename('windupbox', 'data/windows_versions_tested.yml'), mode='r') as f:
            data = yaml.safe_load(f)
        return data[self.os_info.windows_version][self.os_info.version]['editions'][self.os_info.edition]

    def _check_windows_version_match(self):
        """
            check if the provided os_info matches the os_info_filter of the boxcreator class and prints an error if not
        """
        if self.os_info_filter.match(self.os_info) == 0:
            log.error(f'windows info {self.os_info} does not match the class which requires {self.os_info_filter}')

    def _check_if_tested(self):
        """
            checks whether the boxcreator class is tested and gives a warning if not
        """
        if not self._is_tested():
            message = f'this windows version is not fully tested - please be aware that the installation process may differ'
            log.warning(message)

    def _add_winrm_setting_to_source_attr(self):
        """
            add attributes for winrm configuration to source attributes
        """
        self.packer_variables.update({
            'winrm_user': Variable('winrm_user', 'string', 'vagrant'),
            'winrm_password': Variable('winrm_password', 'string', 'vagrant'),
        })
        self.source_attributes.update({
            'communicator': 'winrm',
            'winrm_insecure': 'true',
            'winrm_username': self.packer_variables['winrm_user'],
            'winrm_password': self.packer_variables['winrm_password'],
            'winrm_timeout': '1h',
            'winrm_use_ssl': 'true'
        })

    def _set_guest_os_type(self):
        """
            set guest os type in source attributes
        """
        winversion = self.os_info.windows_version.replace(" ", "")
        arch = self.os_info.architecture.replace("x", "")
        self.source_attributes['guest_os_type'] = f'{winversion}_{arch}'

    def _download_image(self) -> bool:
        """
            download the os image and add related attributes to source attributes
        """
        filepath = self._get_image_path()
        downloader = WindowsDownloader(self.os_info)
        ret = downloader.download_iso(filepath)
        if not ret:
            log.error(f'download of windows iso failed')
            return False
        language_code_installation = extract_languagecodes_from_windows_os_iso(filepath)
        log.info(f'ui language code for installation {language_code_installation}')
        if not language_code_installation:
            log.error(f'no bcp47 language code for installation found on iso image')
            language_code_installation = [self.os_info.language_bcp47]
        self.os_info.set_ui_bcp47(language_code_installation[0])
        self.image = filepath
        self.image_sha256checksum = self._get_image_sha256checksum()
        iso_url = self.image.relative_to(self.base_directory)
        self.packer_variables['iso_url'] = Variable('iso_url', 'string', iso_url.as_posix())
        self.source_attributes['iso_urls'] = [self.packer_variables['iso_url']]
        self.packer_variables['iso_checksum'] = Variable('iso_checksum', 'string', self.image_sha256checksum)
        self.source_attributes['iso_checksum'] = VariableStringMix([self.packer_variables['iso_checksum']], 'sha256:%VAR%')
        return True

    def set_product_key(self, product_key: str):
        """
            set product key applied during installation for the specific Windows version
        """
        self.product_key = product_key

    def add_chocolatey_provisioner(self, packages: list = None):
        raise NotImplementedError

    def add_powershell_provisioners(self, provisioners: list):
        raise NotImplementedError

    def add_provisioner_setup_ssh(self):
        raise NotImplementedError

