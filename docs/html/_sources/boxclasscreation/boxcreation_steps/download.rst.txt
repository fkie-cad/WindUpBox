download of the system image
----------------------------

For the download of the system image overload the _download_image method, that will download the system image and add the necessary builder configuration variables.
We therefore first need to find the location where to place the system image.
This can be done by using the _get_image_path method provided by the BoxCreator baseclass.
Then you can download the image and set the attribute image to the filepath of the downloaded file.
Because packer wants the sha256 checksum of the image, we then calculate the sha256 checksum by calling the _get_image_sha256checksum method, which is also provided by the BoxCreator baseclass.
In a next step we determine the path of the image relative to our project directory, because this is needed for the packerfile.
As a last step we add this relative path as well as the checksum of the iso to the builder configuration variables.
The resulting code then looks something like the following:

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


        def _download_image(self):
            filepath = self._get_image_path()
            downloader = WindowsDownloader(self.windows_info)
            downloader.download_iso(filepath)
            self.image = filepath
            self.image_sha256checksum = self._get_image_sha256checksum()
            iso_url = self.image.relative_to(self.base_directory)
            self.source_attributes['iso_urls'] = [iso_url.as_posix()]
            self.source_attributes['iso_checksum'] = f'sha256:{self.image_sha256checksum}'


        def create_box(self):
            # if you have methods that should be done not in the initialization but right before the box creation, you can place them here
            super().create_box()

As already mentioned before, there is no need to call the _download_image method here due to the fact that it is called by the BoxCreator baseclass.

