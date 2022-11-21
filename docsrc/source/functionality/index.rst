.. _functionality:

A short insight into the box creation process
#############################################

This section gives a short insight on how the windupbox performs the box creation, while referring where needed to the regarding section of the `packer documentation <https://developer.hashicorp.com/packer/docs>`_.

The creation of a box contains the following major steps:

.. _boxcreationsteps:

#. finding the proper class that contains the information on how to install the os the right way
#. creation of the directory structure for the box output, log files and temporary needed files
#. download of the system image (if not provided)
#. create OS specific files for the automated unattended os installation
#. copy of provisioner scripts
#. prepare a Packerfile
#. create a Packerfile
#. run packer to create a vagrant box

Before getting started with explaining each step in more detail we shortly explain the two terms *provisioner* and *builder configuration variables*, which are used a lot in the following.

*provisioners* are used to configure the system and install additional software after the OS is installed.
This tool mainly uses the `PowerShell Provisioner <https://developer.hashicorp.com/packer/docs/provisioners/powershell>`_ to do this task on windows systems.

*builder configuration variables* are the configuration variables for the builder used by packer (in our case its the VirtualBox ISO Builder).
These contain information about the vm such as used cpus, memory and VRAM as well as much other configurations used for the OS installation process.
A full list of the possible configuration parameters and their meaning can be found in `this section <https://developer.hashicorp.com/packer/plugins/builders/virtualbox/iso>`_ of the packer documentation.

finding the proper class for box creation
*****************************************

First off the tool needs to find a class, that contains information on how to perform the os installation for a specific os, version, edition and so on.
These classes are called boxcreator classes.
How this is done in more detail can be read in :ref:`this section <specify os>`.

creation of the directory structure
***********************************

The first step in the box creation after finding the proper class is creating a directory structure for the temporary files needed for the packer build process as well as the final vagrant box and log of the installation process.
Therefore the following directorys/files will get created at every box creation.

.. _structure:

.. code-block:: none

    .
    └── base/                    (can be specified using the command line option -d)
        ├── box                  (used for the vagrant box)*
        ├── floppyfiles          (used to provide files to the vm during installation)
        ├── image                (place for the windows iso image file)
        ├── logs                 (stores the program as well as the packer logs)*
        ├── scripts              (place for the scripts used for the provisioners)
        └── packerfile.pkr.hcl   (Packerfile)

    *: after the successful box creation only those directory will not be deleted

.. The path of each directory is stored in an attribute in the boxcreator class, simply named ``box_directory``, ``floppyfiles_directory`` and so on.

download of the system image
****************************

The download of the windows system images are done via a scraper, that can be found in the ``src/windupbox/windowswebsitescraper/isoscraper/``.
To explain how it done in detail please have a look at the source code.

create OS specific files for the automated unattended os installation
**********************************************************************

Most OS provide a way to install them with a file providing the input a user would normally provide during a GUI installation.
In most cases in this files there is the possibility to custom the os installation process even more.
For windows installations (beginning from Windows 7) this file is called ``Autoanattend.xml``.
This tool provides a minimal API to create such files, while using a template file.
The regarding module can be found in ``src/windupbox/winautounattendAPI/``.

copy of provisioner scripts
***************************

In this step the provisioner scripts will be copied to the scripts directory, such that they can be easily accessed by packer.
Some simple powershell scripts for Windows are already part of the tool. Those can be found in ``src/windupbox/data/scripts``.

prepare and create a Packerfile
*******************************

The next step is the creation of the Packerfile.
A Packerfile contains all the information needed for packer to create the box.
This includes builder configuration variables, provisioners as well as a `post-processor for vagrant <https://developer.hashicorp.com/packer/plugins/post-processors/vagrant/vagrant>`_.

.. If you create a boxcreator it is not needed to create the Packerfile manual.
    Instead it is you can just set or change the attributes source_attributes (for builder configuration variables), provisioners and postprocessors.
    The BoxCreator base class will then create a Packerfile from this information, when you call the create_box method of any boxcreator class.

run packer to create a vagrant box
**********************************

The next performed step is to run packer with the ``packer build`` command, which will boot up a Virtualbox virtual machine in where the os will be installed.
This process takes some time.
At last the temporary files needed for the packer build process, such as the Packerfile will be removed.



