Create a boxcreator class
*********************************

A boxcreator class defines how a Vagrant box for a specific OS, version, edition and so on will be created.
Before you start with the creation a boxcreator class, it is really helpful to first read the chapter :doc:`/functionality/index` to better understand how the creation of a box works.
Additionally it is recommended to have a basic knowledge of `packer <https://www.packer.io/>`_ and the way how this tool performs the box creation process.

Creating a new boxcreator class can be done by extending the BoxCreator baseclass, which provides some functionality of a box creation.
Your class therefore just needs to cover the following functionality:

.. _boxcreator_functionality_steps:

#. specify os (version) the boxcreator class should be used for
#. download of the system image
#. create OS specific files for the automated unattended os installation
#. copy of provisioner scripts
#. configure builder configuration variables, provisioners and postprocessors

Nevertheless in most cases you do not need to implement all of those functionality by yourself, due to the fact that some already existing boxcreator classes cover this steps.
In this cases it is much easier to create a class that extend an already existing boxcreator class than the BoxCreator baseclass.
Sometimes you may even just want to replace or add a single provisioner or source_attribute, due to some minor change in the installation process from version to version.

.. The WindowsBoxCreator class for instance implements the image download as well as setting basic source_attributes.

The following sections first explain how to make small changes while extending an existing boxcreator class before a short overview on how to create a boxcreator class from scratch is provided.

But before we start we have a look at the boxcreator classes available so far, so that you know where you can start.
The following diagram shows all so far available boxcreator classes.
Orange marked are those, who just implement a part of the functionality needed to create a box.
Those are used to share some attributes and methods between their childs.
Blue marked are the boxcreator classes implementing the full functionality of creating a box.

.. image:: _img/boxcreator_class_hierarchy.svg

.. include:: smalladjustments.rst

.. include:: boxcreationfromscratch.rst




