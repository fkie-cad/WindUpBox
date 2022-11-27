Further command line options
############################
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