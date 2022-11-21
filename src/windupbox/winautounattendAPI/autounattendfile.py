# external imports
import attrs
import pkg_resources
from pathlib import Path

# internal imports
from windupbox.helperFunctions.jinja.jinjafeatures import init_jinja_environment
from windupbox.osinfo.windowsinfo import WindowsInfo
from windupbox.winautounattendAPI.synchronouscommand import SynchronousCommand
from windupbox.winautounattendAPI.constants import WINDOWS_GENERICKEYS

# configure logging
import logging
log = logging.getLogger(__name__)


@attrs.define
class Autounantendfile:
    windows_info: WindowsInfo
    commands: list[SynchronousCommand] = attrs.field(default=[])
    productkey: str = attrs.field(default='')

    def add_command(self, command: SynchronousCommand):
        self.commands.append(command)

    def save(self, directory: Path) -> Path:
        template_directory = Path(pkg_resources.resource_filename('windupbox', 'data/templates/'))
        jinja_env = init_jinja_environment(template_directory)
        template = jinja_env.get_template('Autounattend.xml')
        template_dict = {
            'languagecode': self.windows_info.language_bcp47,
            'languagecode_ui_install': self.windows_info.language_bcp47_installation_uilanguage,
            'label': self.windows_info.label,
            'commands': self.commands
        }

        if not self.productkey:
            self.productkey = WINDOWS_GENERICKEYS[self.windows_info.windows_version][self.windows_info.version]['editions'][self.windows_info.edition]
        template_dict['productkey'] = self.productkey

        file = directory/'Autounattend.xml'
        with open(file.as_posix(), mode="w") as f:
            f.write(
                template.render(
                    template_dict
                )
            )
        return file


def order_commands_by_list_order(commands: list[SynchronousCommand]):
    for index, element in enumerate(commands):
        element.order = str(index+1)
