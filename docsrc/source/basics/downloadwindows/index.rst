Download a windows os
*************************

In some cases you may just want to download a specific windows version from the microsoft website.
You can use this tool by running the command ``windupbox os download $WINDOWSINFO``, where ``$WINDOWSINFO`` must contain the windows version, version, edition, language of the os you want to download.
One example would be: ``windupbox os download 'Windows 11,21H2,Edu,English,x64'``.
As described in the section :doc:`/basics/listavailablesystems/index` it is possible to search through all available systems.

If you want to use a certain selection as input you can use the parameter ``-fi`` in your search.
An example would be ``windupbox os list -f 'windows_version=Windows 11, architecture=x64, language=English' -fi`` which will result in the following output, which can be used row by row as an input for the systematic download of the images:

.. code-block::

    Windows 11,21H2 v1,Home,English,x64
    Windows 11,21H2 v1,Pro,English,x64
    Windows 11,21H2 v1,Edu,English,x64
    Windows 11,21H2,Home,English,x64
    Windows 11,21H2,Pro,English,x64
    Windows 11,21H2,Edu,English,x64


