List and filter available systems
*********************************

All available systems are stored in a database.
To list all available systems with all information stored run ``windupbox os list -a``.
This will return quite a long list.
In most cases you most likely just want a certain category of os such as for instance all os with Windows 10 and language English.
Therefore the option ``-f`` can be used to apply such filters in your search.
In our example the command would be ``windupbox os list -f 'windows_version=Windows 10,language=English'``.
Additionally you may want to display only certain columns to see for instance all available windows versions without also seeing all languages.
In this case you can use the option ``-s`` to select which columns should be displayed.
In our example ``windupbox os list -s 'windows_version'``.

An overview over all existing columns and their meaning can be found below:

.. list-table::
   :widths: 25 30
   :header-rows: 1

   * - column
     - meaning
   * - windows_version
     - windows version (e.g. Windows 10, Windows 11, ...,)
   * - version
     - version of the windows version (e.g. 21H1)
   * - edition
     - windows edition (e.g. Home, Pro, Education)
   * - language
     - language (e.g. English, German, French, ...)
   * - architecture
     - processor architecture (x86 or x64)
   * - tested
     - tells whether the configuration was tested or not (1: tested, 0: not tested)


Of course it is also possible combine the column select and the filter.
If you for instance want to know all available version for the windows version 'Windows 10' you can run ``windupbox os list -f 'windows_version=Windows 10' -s 'version'``.
