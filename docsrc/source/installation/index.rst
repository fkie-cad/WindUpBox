*************
Installation
*************

To install the windupbox clone the `repository <https://github.com/fkie-cad/WindUpBox>`_, navigate into the directory and run ``pip install .``.
To check whether the tool is successfully installed and ready to use run ``windupbox -v``.

Requirements
************
To use the tools main functionality of creation vagrant boxes two programs are required.
The first one is `VirtualBox <https://www.virtualbox.org/>`_ , which is used as a hypervisor in the box creation process.
As a second tool `packer <https://www.packer.io/>`_ will be used for automating the os installation process and creating the vagrant box.
Before using the tool make sure that VirtualBox is installed and that packer is downloaded.
Additionally it is needed to add the packer executable path to the PATH environment variable.

Tested Configurations
*********************

The tool was tested with the following versions of Python, packer and VirtualBox:

.. list-table::
   :widths: 25 30
   :header-rows: 1

   * - program
     - versions
   * - Python
     - ``3.8``, ``3.9``, ``3.10``
   * - VirtualBox
     - ``6.1``, ``7.0``
   * - packer
     - ``1.8.0``, ``1.8.1``, ``1.8.2``, ``1.8.3``, ``1.8.4``
