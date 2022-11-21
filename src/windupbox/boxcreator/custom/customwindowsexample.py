# external imports
from pathlib import Path

# internal imports
from windupbox.boxcreator.boxcreator import BoxCreator
from windupbox.osinfo.windowsinfo import WindowsInfo, WindowsInfoFilter
from windupbox.winautounattendAPI.autounattendfile import Autounantendfile, SynchronousCommand

# configure logging
import logging

log = logging.getLogger(__name__)


class CustomBoxCreator(BoxCreator):
    # specify the Windows version the changes should apply
    box_creator_info: WindowsInfoFilter = WindowsInfoFilter(
        windows_version='Windows 10',
        version='21H2',
    )

    def __init__(self, boxdirectory: Path, windows_info: WindowsInfo):
        super().__init__(boxdirectory, windows_info)
        self.windows_info = windows_info
        self.setup_os_specific_files()

    def setup_os_specific_files(self):
        autounantendfile = Autounantendfile(self.windows_info)
        set_execution_policy = SynchronousCommand(
            command=r'cmd.exe /c powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Force"',
            description=r'Set Execution Policy',
        )
        autounantendfile.add_command(set_execution_policy)
        filepath_abs = autounantendfile.save(self.floppy_directory)
        filepath_rel = filepath_abs.relative_to(self.base_directory)
        self.floppy_files.append(filepath_rel)

