*********
WindUpBox
*********

This tool enables users to create Windows Vagrant Boxes in a short time.
It therefore uses `packer <https://www.packer.io/>`_ and `VirtualBox <https://www.virtualbox.org/>`_.
A user can choose the system image by providing the *windows version* (e.g. Windows 10), *version* (e.g. 21H1),
*edition* (e.g. Home), *language* (e.g. English) and *architecture* (e.g. x64) of the preferred windows image.
To create a box run the tool with the *boxcreate* subcommand as shown in the example below:

.. code-block:: text

    windupbox boxcreate 'Windows 10,21H2,Pro,English,x64'

After executing the command the tool will download the regarding system image from the microsoft website.
Alternatively it is also possible to provide the system image by the using the ``-iso`` option.
After the successful execution of the tool you will find a directory in your current working directory, named by the windows version, version and edition.
This directory contains a log directory with logfiles of the creation process as well as a box directory with the created box image, ready to use with vagrant.

In order to see which windows versions, versions, edition, languages and architectures are available the subcommand ``windupbox os list`` can be used.
For instance, the command ``windupbox os list -a`` will output all available os configurations.
It is also possible to filter them as explained further in the `documentation <https://fkie-cad.github.io/WindUpBox/html/basics/listavailablesystems/index.html>`_.

Due to the large amount of different windows versions, editions and so on, not all are tested so far.
If a specific windows version is not working for you feel free to create a github issue or even better build a custom so called *boxcreator class* catching the differences.
A tutorial on how to do that can be found `here <https://fkie-cad.github.io/WindUpBox/html/advanced/boxclasscreation/index.html>`_.

..
    System Customizations
    **********************
    To further customize the created boxes there are multiple options for the boxcreator subcommand available, which are described in the table below:

    .. list-table::
       :widths: 25 30
       :header-rows: 1

       * - command line option
         - description
       * - ``-bcp BCP47``
         - specify the bcp47 code used for the language for keyboard layout and installation (a list of bcp47 codes can be found `here <https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oe376/6c085406-a698-4e12-9d4d-c3b0ee3dbc4a>`_)
       * - ``-ssh``
         - install OpenSSH Server and set up so that it can be used be vagrant as the communicator
       * - ``-ch``
         - install `chocolatey <https://chocolatey.org/>`_
       * - ``-chp CHOCO_PACKAGES``
         - install provided packages with choco (and automatically install `chocolatey <https://chocolatey.org/>`_)
       * - ``-ps PS_SCRIPTS``
         - run provided powershell scripts (provide a directory or a set of paths)
       * - ``-key WINDOWS_KEY``
         - insert windows product key into the windows installation


    Further command line options
    *****************************
    There are a few other options for the boxcreator subcommand available to customize the execution.


    .. list-table::
       :widths: 20 30
       :header-rows: 1

       * - command line option
         - description
       * - ``-d BOXDIRECTORY``
         - | specify a directory, which is used for files that are created the box creation process such as the packerfile, scripts and the output box
           | (if not provided a directory will be created in the actual directory)
       * - ``--disable-cleanup``
         - disable cleanup after packer build process to preserve the used scripts and the used packerfile
       * - ``-iso ISO``
         - path of an windows iso file (will skip the download process)

Documentation
*************

A full documentation for can be found `here <https://fkie-cad.github.io/WindUpBox/>`_.
