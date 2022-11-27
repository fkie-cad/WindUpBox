List and filter available systems
*********************************

All available systems are stored in a database.
To list all available systems with all information stored run ``windupbox os list -a``.
This will return quite a long list.
In most cases you most likely just want a certain category of os such as all os with Windows 10 and language English.
Therefore the option ``-f`` can be used to apply such filters in your search.
In our example the command would be ``windupbox os list -f 'windows_version=Windows 10,language=English'``.
Additionally you may want to display only certain columns to see for instance all available windows versions without also seeing all languages.
In this case you can use the option ``-s`` to select which columns should be displayed.
In our example ``windupbox os list -s 'windows_version'``.

An overview over all existing columns and their meaning can be found below:




Of course it is also possible combine the column select and the filter.
If you for instance want to know 