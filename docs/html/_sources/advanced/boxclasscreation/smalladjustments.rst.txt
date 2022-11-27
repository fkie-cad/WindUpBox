small and easy doable adjustments
#################################

We start with showing in a simple example how to change, set and delete builder configuration variables (stored in the source_attributes attribute), provisioners and postprocessors.
Therefore we create a *boxcreator class*, that should be used for all editions, languages and architectures for the windows version Windows 10 in version 21H1.
To demonstrate the creation of such a class we will show some possible changes.
Please be aware that these changes are just meant to demonstrate how changes in general are done - these changes are not needed to make the box creation for this specific windows version work.

To create a boxcreator class we start with the creation of a python file in the ``src/windupbox/boxcreator/custom/`` directory.
In there we create our new boxcreator class.
This boxcreator class extends the *Win10BoxCreator* boxcreator class, which is provided by the tool (located in ``src/windupbox/boxcreator/provided/windows10.py``).
After the creation of the python file the content should look like the following:

.. code-block:: python3
    :linenos:

    # external imports
    from pathlib import Path

    # internal imports
    from windupbox.boxcreator.provided import Win10BoxCreator
    from windupbox.winconstants.windowsinfo import WindowsInfo

    # configure logging
    import logging
    log = logging.getLogger(__name__)


    class CustomWindows10BoxCreator(Win10BoxCreator):

        def __init__(self, boxdirectory: Path, windows_info: WindowsInfo):
            super().__init__(boxdirectory, windows_info)

The first thing to do is always to specify the windows versions, versions, editions and so for which your boxcreator class should be used.
This can be done by setting the os_info_filter attribute to an instance of the WindowsInfoFilter class (located in ``src/windupbox/winconstants/windowsinfo.py``).
In our example we want that our *boxcreator class* will be used for all windows 10 systems in version 21H1.
Therefore we create the WindowsInfoFilter instance with the keyword arguments ``windows_version='Windows 10'`` and ``version='21H1'``.
The result should look like the following:

.. code-block:: python3
    :linenos:
    :emphasize-lines: 6,14-18

    # external imports
    from pathlib import Path

    # internal imports
    from windupbox.boxcreator.provided import Win10BoxCreator
    from windupbox.winconstants.windowsinfo import WindowsInfo, WindowsInfoFilter

    # configure logging
    import logging
    log = logging.getLogger(__name__)


    class CustomWindows10BoxCreator(Win10BoxCreator):
        # specify the Windows version the boxcreator class should be used for
        os_info_filter: WindowsInfoFilter = WindowsInfoFilter(
            windows_version='Windows 10',
            version='21H2',
        )

        def __init__(self, boxdirectory: Path, windows_info: WindowsInfo):
            super().__init__(boxdirectory, windows_info)

Now we can start to implement some changes to the os installation process.
We will therefore show code implementing the following changes:

#. change/add/remove a builder configuration variable
#. disable a provisioner
#. add/replace a provisioner


change/add/remove builder configuration variables
-------------------------------------------------

All builder configuration variables are stored within an attribute of a boxcreator class, called source_attributes.
This attribute is a dictionary, where each key represents a builder configuration variable name and each value the builder configuration variable value.
To change, add or remove a builder configuration variable it is best to create a method performing the necessary dictionary operation.
An example with all three actions can be seen below.

.. code-block:: python3
    :linenos:
    :emphasize-lines: 23-25,27-29,31-33

    # external imports
    from pathlib import Path

    # internal imports
    from windupbox.boxcreator.provided import Win10BoxCreator
    from windupbox.winconstants.windowsinfo import WindowsInfo, WindowsInfoFilter

    # configure logging
    import logging
    log = logging.getLogger(__name__)


    class CustomWindows10BoxCreator(Win10BoxCreator):
        # specify the Windows version the changes should apply
        os_info_filter: WindowsInfoFilter = WindowsInfoFilter(
            windows_version='Windows 10',
            version='21H2',
        )

        def __init__(self, boxdirectory: Path, windows_info: WindowsInfo):
            super().__init__(boxdirectory, windows_info)

        # add builder configuration variable
        def _add_usb_bus(self):
            self.source_attributes['usb'] = True

        # change builder configuration variable
        def _change_cpus(self):
            self.source_attributes['cpus'] = 6

        # remove builder configuration variable
        def _remove_headless(self):
            del self.source_attributes['headless']


After creating the methods it is needed to call them.
This can be done by calling the function at the end of the initialization method:

.. code-block:: python3
    :linenos:
    :emphasize-lines: 23-26

    # external imports
    from pathlib import Path

    # internal imports
    from windupbox.boxcreator.provided import Win10BoxCreator
    from windupbox.winconstants.windowsinfo import WindowsInfo, WindowsInfoFilter

    # configure logging
    import logging
    log = logging.getLogger(__name__)


    class CustomWindows10BoxCreator(Win10BoxCreator):
        # specify the Windows version the changes should apply
        os_info_filter: WindowsInfoFilter = WindowsInfoFilter(
            windows_version='Windows 10',
            version='21H2',
        )

        def __init__(self, boxdirectory: Path, windows_info: WindowsInfo):
            super().__init__(boxdirectory, windows_info)

            # call own functions here
            self._add_usb_bus()
            self._change_cpus()
            self._remove_headless()

        def _add_usb_bus(self):
            self.source_attributes['usb'] = True

        def _change_cpus(self):
            self.source_attributes['cpus'] = 6

        def _remove_headless(self):
            del self.source_attributes['headless']


add/change a provisioner
------------------------

In our case we will add a PowerShellProvisioner, that executes a Powershell Script called donothing.ps1, which we have stored in the directory ``X:\donothing.ps1``.
In a first step we create a own method for adding the provisioner, that in our case is called _add_provisioner_donothing.
First we copy the donothing.ps1 into our projects scripts directory.
This can be easily done by using the provided _copy_script_to_packer method as shown below.

.. code-block:: python3
    :linenos:
    :emphasize-lines: 23-26

    # external imports
    from pathlib import Path

    # internal imports
    from windupbox.boxcreator.provided import Win10BoxCreator
    from windupbox.winconstants.windowsinfo import WindowsInfo, WindowsInfoFilter

    # configure logging
    import logging
    log = logging.getLogger(__name__)


    class CustomWindows10BoxCreator(Win10BoxCreator):
        # specify the Windows version the changes should apply
        os_info_filter: WindowsInfoFilter = WindowsInfoFilter(
            windows_version='Windows 10',
            version='21H2',
        )

        def __init__(self, boxdirectory: Path, windows_info: WindowsInfo):
            super().__init__(boxdirectory, windows_info)

        def _add_provisioner_donothing(self):
            script_path_source = Path(r'X:\donothing.ps1')
            script_path_dst_relative_to_script_dir = Path('X:\donothing.ps1')
            script_path_for_packerfile = self._copy_script_to_packer(script_path_source, script_path_dst_relative_to_script_dir)

Now we need to add a Provisioner to the provisioners of our class (stored in the attribute provisioners).
This is done by creating an instance of a provisioner class (located in ``src/windupbox/packerAPI/provisioner.py``).
In our case the PowerShellProvisioner class, because we want to run a powershell script as a provisioner.
The constructor of the PowerShellProvisioner class requires a type first.
The three available types are inline, script and scripts.
If inline is chosen the second parameter needs to be a string with a powershell code line.
If instead script/scripts is chosen the script path/list of script paths needs to be provided in the second parameter.
Additionally there are many ways to customize the provisioner by setting different attributes.
All attributes can be found in the `powershell provisioner section in the packer documentation <https://developer.hashicorp.com/packer/docs/provisioners/powershell>`_.
In our example we create a PowerShellProvisioner instance with type script and set the attribute debug_mode to 1.
The resulting code can be seen below:


.. code-block:: python3
    :linenos:
    :emphasize-lines: 7, 28-30

    # external imports
    from pathlib import Path

    # internal imports
    from windupbox.boxcreator.provided import Win10BoxCreator
    from windupbox.winconstants.windowsinfo import WindowsInfo, WindowsInfoFilter
    from windupbox.packerAPI.provisioner import PowershellProvisioner

    # configure logging
    import logging
    log = logging.getLogger(__name__)


    class CustomWindows10BoxCreator(Win10BoxCreator):
        # specify the Windows version the changes should apply
        os_info_filter: WindowsInfoFilter = WindowsInfoFilter(
            windows_version='Windows 10',
            version='21H2',
        )

        def __init__(self, boxdirectory: Path, windows_info: WindowsInfo):
            super().__init__(boxdirectory, windows_info)

        def _add_provisioner_donothing(self):
            script_path_source = Path(r'X:\donothing.ps1')
            script_path_dst_relative_to_script_dir = Path('X:\donothing.ps1')
            script_path_for_packerfile = self._copy_script_to_packer(script_path_source, script_path_dst_relative_to_script_dir)
            provisioner_donothing = PowershellProvisioner('script', script_path_for_packerfile.as_posix())
            provisioner_donothing.add_custom_attribute('debug_mode', '1')
            self.provisioners.append(provisioner_donothing)


As a last step we need to call our newly created function.
Therefore we again call the method at the end of the initialization method as shown below:

.. code-block:: python3
    :linenos:
    :emphasize-lines: 24-25

    # external imports
    from pathlib import Path

    # internal imports
    from windupbox.boxcreator.provided import Win10BoxCreator
    from windupbox.winconstants.windowsinfo import WindowsInfo, WindowsInfoFilter
    from windupbox.packerAPI.provisioner import PowershellProvisioner

    # configure logging
    import logging
    log = logging.getLogger(__name__)


    class CustomWindows10BoxCreator(Win10BoxCreator):
        # specify the Windows version the changes should apply
        os_info_filter: WindowsInfoFilter = WindowsInfoFilter(
            windows_version='Windows 10',
            version='21H2',
        )

        def __init__(self, boxdirectory: Path, windows_info: WindowsInfo):
            super().__init__(boxdirectory, windows_info)

            # call own functions here
            self._add_provisioner_donothing()

        def _add_provisioner_donothing(self):
            script_path_source = Path(r'X:\donothing.ps1')
            script_path_dst_relative_to_script_dir = Path('X:\donothing.ps1')
            script_path_for_packerfile = self._copy_script_to_packer(script_path_source, script_path_dst_relative_to_script_dir)
            provisioner_donothing = PowershellProvisioner('script', script_path_for_packerfile.as_posix())
            provisioner_donothing.add_custom_attribute('debug_mode', '1')
            self.provisioners.append(provisioner_donothing)



If you want to replace an already existing provisioner, find out the method name by looking at the source code and overload the function, as shown below.
In this case it is import to NOT call the function in the initialization method because its should be already called in the parent class.


disable a provisioner
---------------------

In order to disable a provisioner (or another function of a parent class) just simply overload the regarding method with an empty one
as shown below with the _add_provisioner_disable_hibernate method.

.. code-block:: python3
    :linenos:
    :emphasize-lines: 23-24

    # external imports
    from pathlib import Path

    # internal imports
    from windupbox.boxcreator.provided import Win10BoxCreator
    from windupbox.winconstants.windowsinfo import WindowsInfo, WindowsInfoFilter

    # configure logging
    import logging
    log = logging.getLogger(__name__)


    class CustomWindows10BoxCreator(Win10BoxCreator):
        # specify the Windows version the changes should apply
        os_info_filter: WindowsInfoFilter = WindowsInfoFilter(
            windows_version='Windows 10',
            version='21H2',
        )

        def __init__(self, boxdirectory: Path, windows_info: WindowsInfo):
            super().__init__(boxdirectory, windows_info)

        def _add_provisioner_disable_hibernate(self):
            log.info(f'provisioner disable hibernate disabled')