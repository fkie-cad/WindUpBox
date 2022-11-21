specify os
----------

It is important to specify for which os and which version your boxcreator class should be used.
To better understand how this is done properly we shortly explain how the tool chooses a boxcreator class for the input given in the command line interface.

If a user run the tool, it provide them a list of os, versions, editions and so on.
These data will be stored in an instance of the so called OsInfo class and determines which boxcreator class will be used for the box creation.
Each boxcreator class contains an instance of the so called OsInfoFilter class, which is used to specify which os given through their OsInfo match with the filter.
Therefore the OsInfoFilter has a method called match, which returns whether the OsInfo matches the filter.
Additionally it provides the information how precise it matches the filter.

For specific os, the characteristic data can vary.
Therefore we work with childs of the OsInfo and OsInfoFilter class for certain os.
So far the tool supports only windows, where the regarding classes are called WindowsInfo and WindowsInfoFilter.
All this classes are located in the ``src/windupbox/osinfo/`` module.

As an example let us say we just have two boxcreator called Windows10_21H1BoxCreator and Windows10_BoxCreator.
In the Windows10_21H1BoxCreator class the os_info_filter has the value ``WindowsInfoFilter(windows_version=['Windows 10'], version=['21H1'])`` while the Windows10_BoxCreator os_info_filter attribute is ``WindowsInfoFilter(windows_version=['Windows 10'])``.
If the user now chooses any os_info containing 'Windows 10' as the windows version and '21H1' as the version the Windows10_21H1BoxCreator class will be used, due to the fact it matches more precise.
Accordingly if the user chooses any os_info containing 'Windows 10' and another windows version the Windows10_BoxCreator will be used.
This provides the possibility to build a flexible structure, which allows small adjustments in the installation process for certain versions.

If you create a new boxcreator class it may be needed for you to add options to the os selection in the command line interface.
An tutorial on how to do that can be found :ref:`here <How to add an os specification to the os option list>`.