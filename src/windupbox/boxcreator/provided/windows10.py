# external imports
from pathlib import Path
import shutil

# internal imports
from windupbox.boxcreator.provided.windows import WindowsBoxCreator
from windupbox.packerAPI import Variable, PowershellProvisioner
from windupbox.winautounattendAPI.autounattendfile import Autounantendfile, order_commands_by_list_order
from windupbox.winautounattendAPI.synchronouscommand import SynchronousCommand
from windupbox.osinfo.windowsinfo import WindowsInfo, WindowsInfoFilter
from windupbox.winautounattendAPI.common_commands.remote_access import enable_winrm, set_execution_policy
from windupbox.winautounattendAPI.common_commands.gui import network_prompt_disable
from windupbox.helperFunctions.jinja.jinjafeatures import init_jinja_environment

# configure logging
import logging
log = logging.getLogger(__name__)


class Win10BoxCreator(WindowsBoxCreator):
    os_info_filter: WindowsInfoFilter = WindowsInfoFilter(
        ['Windows 10']
    )
    os_info: WindowsInfo

    personal_powershell_scripts: Path
    powershell_autounattend_commands: list[SynchronousCommand]

    def __init__(self, boxdirectory: Path, windows_info: WindowsInfo):
        super(Win10BoxCreator, self).__init__(boxdirectory, windows_info)

        self.personal_powershell_scripts = self.scripts_directory/'personal_scripts'

        self.powershell_autounattend_commands = []

        self._check_windows_version_match()
        self._add_os_information_to_packer_variables()

        self._add_floppyfile_configureremotingforpacker()
        self._add_floppyfile_autounattend()
        self._add_floppyfile_syspreb()
        self._add_floppyfile_unattend()

        self._add_provisioner_install_vboxguestadditions()
        self._add_provisioner_disable_hibernate()
        self._add_provisioner_setup_windows_account()

        self._add_powershell_commands_for_autounattend_file()

    def _set_label(self, mode='short'):
        forbidden_chars = [' ', '.']
        windows_version = self.os_info.windows_version
        version = self.os_info.version
        edition = self.os_info.edition
        for char in forbidden_chars:
            windows_version = windows_version.replace(char, '')
            version = version.replace(char, '')
            edition = edition.replace(char, '')

        if mode == 'short':
            self.label = f'{windows_version}-{edition}-{version}'
        elif mode == 'long':
            self.label = f'{windows_version}-{edition}-{version}-{self.os_info.language}-{self.os_info.architecture}'

    def _add_floppyfile_configureremotingforpacker(self):
        floppyfile_path_source = self.package_script_directory/'ConfigureRemotingForAnsible.ps1'
        floppyfile_path_dst_relative_to_script_dir = Path('ConfigureRemotingForAnsible.ps1')
        self._copy_and_set_floppyfile(floppyfile_path_source, floppyfile_path_dst_relative_to_script_dir)

    def _add_floppyfile_unattend(self):
        floppyfile_path_source = self.package_script_directory/'unattend.xml'
        floppyfile_path_dst_relative_to_script_dir = Path('unattend.xml')
        self._copy_and_set_floppyfile(floppyfile_path_source, floppyfile_path_dst_relative_to_script_dir)

    def _add_floppyfile_syspreb(self):
        floppyfile_path_source = self.package_script_directory/'sysprep.bat'
        floppyfile_path_dst_relative_to_script_dir = Path('sysprep.bat')
        self._copy_and_set_floppyfile(floppyfile_path_source, floppyfile_path_dst_relative_to_script_dir)
        self.source_attributes.update({
            'shutdown_command': r'A:\\sysprep.bat',
            'shutdown_timeout': '15m',
        })

    def _create_autounattend_file(self) -> Path:
        autounantendfile = Autounantendfile(self.os_info, self.powershell_autounattend_commands, self.product_key)
        return autounantendfile.save(self.floppy_directory)

    def _add_floppyfile_autounattend(self):
        autounattend_dile = self.floppy_directory/'Autounattend.xml'
        self._set_floppyfile(autounattend_dile)

    def _add_powershell_commands_for_autounattend_file(self):
        self.powershell_autounattend_commands.append(set_execution_policy)
        self.powershell_autounattend_commands.append(enable_winrm)
        self.powershell_autounattend_commands.append(network_prompt_disable)

    def _add_os_information_to_packer_variables(self):
        self.packer_variables['win_version'] = Variable('win_version', 'string', self.os_info.version)
        self.packer_variables['win_edition'] = Variable('win_edition', 'string', self.os_info.edition)
        self.packer_variables['win_build'] = Variable('win_build', 'string', self.os_info.build)

    def _get_image_path(self) -> Path:
        filename = f'{self.os_info.windows_version.replace(" ", "")}_{self.os_info.edition}_{self.os_info.version}_{self.os_info.build}_{self.os_info.language}.iso'
        path = self.image_directory/filename
        return path

    def _add_provisioner_install_vboxguestadditions(self):
        provisioner_install_vboxguestadditions = PowershellProvisioner('inline', [
            r"$cert = (Get-AuthenticodeSignature 'E:\\VBoxWindowsAdditions.exe').SignerCertificate; ["
            r"System.IO.File]::WriteAllBytes('C:\\vbox.cer', $cert.Export(["
            r"System.Security.Cryptography.X509Certificates.X509ContentType]::Cert));",
            r"certutil.exe -f -addstore TrustedPublisher C:\\vbox.cer",
            r"E:\\VBoxWindowsAdditions.exe /S",
            r"del C:\\vbox.cer"
        ])
        self.provisioners.append(provisioner_install_vboxguestadditions)

    def _add_provisioner_disable_hibernate(self):
        script_path_source = self.package_script_directory/Path('setup/DisableHibernate.ps1')
        script_path_dst_relative_to_script_dir = Path('setup/DisableHibernate.ps1')
        script_path_dst_relative_to_basedir = self._copy_script(script_path_source, script_path_dst_relative_to_script_dir)
        provisioner_disable_hibernate = PowershellProvisioner('script', script_path_dst_relative_to_basedir.as_posix())
        self.provisioners.append(provisioner_disable_hibernate)

    def _add_provisioner_setup_windows_account(self):
        script_path_source = self.package_script_directory/Path('setup/SetupAccount.ps1')
        script_path_dst_relative_to_script_dir = Path('setup/SetupAccount.ps1')
        script_path_dst_relative_to_basedir = self._copy_script(script_path_source, script_path_dst_relative_to_script_dir)
        provisioner_setup_windows_account = PowershellProvisioner('script', script_path_dst_relative_to_basedir.as_posix())
        self.provisioners.append(provisioner_setup_windows_account)

    def add_provisioner_setup_ssh(self):
        script_path_source = self.package_script_directory/Path('setup/SetupSSH.ps1')
        script_path_dst_relative_to_script_dir = Path('setup/SetupSSH.ps1')
        script_path_dst_relative_to_basedir = self._copy_script(script_path_source, script_path_dst_relative_to_script_dir)
        provisioner_setup_ssh = PowershellProvisioner('script', script_path_dst_relative_to_basedir.as_posix())
        provisioner_setup_ssh.add_elevated_user('Administrator', 'vagrant')
        self.provisioners.append(provisioner_setup_ssh)

    def add_chocolatey_provisioner(self, packages: list = None):
        if not packages:
            packages = []
        script_name = 'InstallChocolatey.ps1'
        packages_dict_list = []
        for pkg in packages:
            packages_dict_list.append(
                {
                    'name': pkg
                }
            )
        jinja_env = init_jinja_environment(self.package_template_directory)
        template = jinja_env.get_template('InstallChocolatey.ps1')
        dst = self.scripts_directory/script_name
        with open(dst, mode='w') as f:
            f.write(
                template.render(
                    packages=packages_dict_list
                )
            )
        self.provisioners.append(PowershellProvisioner('script', dst.relative_to(self.base_directory).as_posix()))

    def add_powershell_provisioners(self, provisioners: list[Path]):
        self.personal_powershell_scripts.mkdir(exist_ok=True)
        for file in provisioners:
            dst = self.personal_powershell_scripts/file.name
            if not file.is_file():
                log.error(f'file {file} could not be copied because its not existing')
            else:
                shutil.copy(file.as_posix(), dst.as_posix())
                log.debug(f'file {file} copied to {dst}')
                self.provisioners.append(PowershellProvisioner('script', dst.relative_to(self.base_directory).as_posix()))

    def create_box(self, exclude_download: bool = False):
        if not self._project_structure_valid:
            return
        if not self.image_pre_set:
            ret = self._download_image()
            if not ret:
                log.error(f'download of image failed -> box can not be created please provide an iso or check above log messages')
                return
        order_commands_by_list_order(self.powershell_autounattend_commands)
        self._create_autounattend_file()
        super().create_box(exclude_download=True)
