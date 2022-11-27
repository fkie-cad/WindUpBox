System Customizations
#####################
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