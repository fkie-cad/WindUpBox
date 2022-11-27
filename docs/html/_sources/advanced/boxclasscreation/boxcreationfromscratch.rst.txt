create a boxcreator class from scratch
######################################

To create a boxcreator class from scratch it is needed to implement all functionality mentioned :ref:`in the list above <boxcreator_functionality_steps>`.
These are:

#. define specific os the boxcreator class should be used for
#. download of the system image (if not provided)
#. create OS specific files for the automated unattended os installation
#. copy of provisioner scripts
#. configure builder configuration variables, provisioners and postprocessors

Steps 4 and 5 are already covered in the section above.
Therefore in the following sections just cover how to define the os the boxcreator class should be used for , how to implement the os image download and how to create os specific files, that are needed for the box creation.

We first start with the basic structure of each boxcreator class, which looks like the following:

.. code-block:: python3
    :linenos:

    # external imports
    from pathlib import Path

    # internal imports
    from windupbox.boxcreator.boxcreator import BoxCreator
    from windupbox.winconstants.windowsinfo import WindowsInfo

    # configure logging
    import logging
    log = logging.getLogger(__name__)


    class CustomBoxCreator(BoxCreator):

        def __init__(self, boxdirectory: Path):
            super().__init__(boxdirectory)
            # you can be place methods that add provisioners, add builder configuration variables or create additional files here

        # custom methods

        def create_box(self):
            # if you have methods that should be done not in the initialization but right before the box creation, you can place them here
            super().create_box()

In the following we will create such a boxcreator class for Windows 10.
Because it would be way to much to explain every function needed we will just cover some basics, that help you understand how everything works.
For details please look at the real Windows 10 boxcreator class and the Windows boxcreator class (located in ``src/windupbox/boxcreator/provided/``).

.. include:: boxcreation_steps/specifyos.rst

.. include:: boxcreation_steps/download.rst

.. include:: boxcreation_steps/osspecificfiles.rst
