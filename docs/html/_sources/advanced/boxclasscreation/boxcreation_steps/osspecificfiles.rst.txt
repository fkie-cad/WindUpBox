creation of os specific files
-----------------------------

For most os installations additional files are needed that configure the installation process.
Newer windows versions, such as Windows 8, 10 and 11 for instance use a so called `Autounattend.xml <https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/update-windows-settings-and-scripts-create-your-own-answer-file-sxs?view=windows-11>`_ file.
These can be distributed to the packer virtual machine by a `floppy drive <https://developer.hashicorp.com/packer/plugins/builders/virtualbox/iso#floppy-configuration>`_ or a `http directory <https://developer.hashicorp.com/packer/plugins/builders/virtualbox/iso#http-directory-configuration>`_.
Dependent on the os it may be necessary to execute the file.
Therefore in most cases the `boot command <https://developer.hashicorp.com/packer/plugins/builders/virtualbox/iso#boot-configuration>`_ is used.
For windows systems no boot command is needed due to the fact that windows automatically finds the Autounattend.xml if provided through a drive, like the floppy drive.

In the following section it is shortly shown how to add a file to the `floppy drive <https://developer.hashicorp.com/packer/plugins/builders/virtualbox/iso#floppy-configuration>`_.
We therefore create an Autounattend file using a minimal API for Autounattend files provided by this tool.
We first setup the class as already done in the sections before and add a method where we create the Autounattend.xml and add it to the floppy files.
Additionally we import the Autounattendfile class as well as the SynchronousCommand class from the winautounattendAPI module.

.. code-block:: python3
    :linenos:
    :emphasize-lines: 7,23,25-26

    # external imports
    from pathlib import Path

    # internal imports
    from windupbox.boxcreator.boxcreator import BoxCreator
    from windupbox.winconstants.windowsinfo import WindowsInfo, WindowsInfoFilter
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
            self.setup_os_specific_files()

        def setup_os_specific_files(self):
            pass

In a next step we create an Autounattendfile instance.
Additionally we add a command to the Autounattend file, that will change the execution policy for windows powershell scripts.
As a last step we can save the Autounattend file to the floppy directory, by using the save method of the class, which will return the path were the file is saved.
The result looks like the following:

.. code-block:: python3
    :linenos:
    :emphasize-lines: 26-32

    # external imports
    from pathlib import Path

    # internal imports
    from windupbox.boxcreator.boxcreator import BoxCreator
    from windupbox.winconstants.windowsinfo import WindowsInfo, WindowsInfoFilter
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
            self.setup_os_specific_files()

        def setup_os_specific_files(self):
            autounantendfile = Autounantendfile(self.windows_info)
            set_execution_policy = SynchronousCommand(
                command=r'cmd.exe /c powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Force"',
                description=r'Set Execution Policy',
            )
            autounantendfile.add_command(set_execution_policy)
            filepath_abs = autounantendfile.save(self.floppy_directory)

No we need to add the relative path of our Autounattendfile to the floppy files.
This can simply be done by appending the relative path to the floppy_files attribute of the boxcreator class.

.. code-block:: python3
    :linenos:
    :emphasize-lines: 33-34

    # external imports
    from pathlib import Path

    # internal imports
    from windupbox.boxcreator.boxcreator import BoxCreator
    from windupbox.winconstants.windowsinfo import WindowsInfo, WindowsInfoFilter
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

As already mentioned this is just a small example, that should show you how its done in theory.
The here created box will not work, because more scripts are needed.
To have further insight have a look in the already existing boxcreator classes.

