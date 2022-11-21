****************************
How to create a Windows Box
****************************

This tool enables users to create Windows Vagrant Boxes in a short time.
It therefore uses `packer <https://www.packer.io/>`_ and `VirtualBox <https://www.virtualbox.org/>`_.
A user can choose the system image by providing the *windows version* (e.g. Windows 10), *version* (e.g. 21H1),
*edition* (e.g. Home), *language* (e.g. English) and *architecture* (e.g. x64) of the preferred windows image.
After deciding on a a windows image the use can run the tool with the *boxcreate* subcommand to create the vagrant box as shown in the example below:

.. code-block:: text

    fwinpacker boxcreate 'Windows 10' '21H2' 'Pro' 'English' 'x64'

After executing the command the tool will download the regarding system image from the microsoft website.
Alternatively it is also possible to provide the system image by the using the ``-iso`` option.
After the successful execution of the tool you will find a directory in your current working directory, named by the windows version, version and edition.
This directory contains a log directory with logfiles of the creation process as well as a box directory with the created box file, ready to use with vagrant.

In order to see which windows versions, versions, edition, languages and architectures are available just run the command partially.
For instance, the command ``fwinpacker boxcreate 'Windows 10'`` will output all available versions.
Due to the large amount of different windows versions, editions and so on, not all are tested so far.
If a specific windows version is not working for you feel free to create a github issue or even better build a custom so called *boxcreator class* addressing the differences.
A tutorial on how to do that can be found in :doc:`../boxclasscreation/index`.

.. include:: system_customizations.rst

.. include:: further_command_line_options.rst