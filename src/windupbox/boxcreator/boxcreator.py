# external imports
import shutil
from pathlib import Path
import hashlib
import pkg_resources
from retry import retry

# internal imports
from windupbox.config import DEBUG
from windupbox.osinfo.osinfo import OsInfo, OsInfoFilter
from windupbox.packerAPI.variable import Variable, VariableStringMix
from windupbox.packerAPI import Packerfile, BuildBlock, Source, Provisioner, PostProcessor, VagrantPostProcessor
from windupbox.helperFunctions.hash.hash import checksum
from windupbox.logger.logger import add_filehandler

# configure logging
import logging
log = logging.getLogger(__name__)


class BoxCreator:
    """
    base class for all boxcreator classes, that implements basic structure that can be used as well as modified for specific boxcreator classes

    """
    os_info_filter: OsInfoFilter = None
    os_info: OsInfo

    label: str

    packerfile: Packerfile

    base_directory: Path
    box_directory: Path
    output_directory: Path
    scripts_directory: Path
    image_directory: Path
    floppy_directory: Path

    exclude_from_cleanup: list[Path]
    cleanup_active: bool = True

    packer_variables: dict
    source_attributes: dict
    provisioners: list[Provisioner]
    postprocessors: list[PostProcessor]
    floppy_files: list

    image_pre_set: bool = False
    image: Path
    image_sha256checksum: str

    __vagrant_add_box: bool = False
    vagrant_box_settings: dict
    VagrantfileTemplate: Path

    package_script_directory: Path = Path(pkg_resources.resource_filename('windupbox', 'data/scripts/'))
    package_template_directory: Path = Path(pkg_resources.resource_filename('windupbox', 'data/templates/'))

    _project_structure_valid: bool = True

    def __init__(self, base_directory: Path, os_info: OsInfo):
        self.os_info = os_info

        self.base_directory = base_directory
        self.logdirectory = base_directory / 'logs'
        self.scripts_directory = base_directory / 'scripts'
        # ! don't create this directory - it will be created by packer
        self.output_directory = base_directory/'output'
        self.box_directory = base_directory / 'box'
        self.image_directory = base_directory / 'image'
        self.floppy_directory = base_directory / 'floppyfiles'

        try:
            self.base_directory.mkdir(exist_ok=False)
            self.logdirectory.mkdir(exist_ok=False)
            self.image_directory.mkdir(exist_ok=False)
            self.floppy_directory.mkdir(exist_ok=False)
            self.box_directory.mkdir(exist_ok=False)
        except FileExistsError:
            log.error(f'the project structure could not get created due to the fact that the directory {self.base_directory} already exists -> please choose another location or delete the folder')
            self._project_structure_valid = False

        logfile = self.logdirectory / 'program.log'
        add_filehandler(logfile=logfile)

        self.exclude_from_cleanup = [self.logdirectory, self.box_directory]
        self.provisioners = []
        self.post_install_commands = []
        self.postprocessors = []
        self.floppy_files = []

        self._set_label()

        self._set_base_packer_variables()
        self._set_base_source_attributes()
        self._add_vagrant_postprocessor()

    def __check_label(self) -> bool:
        """
        checks whether the label of the boxcreator instance contains not valid characters
        """
        invalid_chars = ['.']
        for char in invalid_chars:
            if char in self.label:
                log.error(f'label is not correct because it contains the character "{char}", that is not allowed')
                return False
        return True

    def _set_label(self, label='boxcreatorVM'):
        """
        sets a label for the boxcreator instance
        can be overloaded to set specific labels for different OS versions and so on
        """
        self.label = label

    def _add_vagrant_postprocessor(self):
        """
        add a vagrant post-processor
        """
        processor = VagrantPostProcessor()
        processor.add_output(f'{self.box_directory.name}/{self.label}.box')
        self.postprocessors.append(processor)

    def __create_packerfile(self):
        """
        creates a Packerfile based on the attributes packer_variables, source_attributes, provisioners and postprocessors
        """
        self.packerfile = Packerfile()
        self.packerfile.add_variables([var[1] for var in self.packer_variables.items()])
        source = Source(f'virtualbox-iso', self.label)
        source.set_attribute_by_dict(self.source_attributes)
        self.packerfile.add_source(source)
        bb = BuildBlock([source])
        for prov in self.provisioners:
            bb.add_provisioner(prov)
        for postproc in self.postprocessors:
            bb.add_postprocessor(postproc)
        self.packerfile.set_buildblock(bb)

    def _set_base_packer_variables(self):
        """
        set some basic packer variables that are used in the source attributes
        """
        self.packer_variables = {
            'cpus': Variable('cpus', 'string', '4'),
            'memory': Variable('memory', 'string', '4096'),
            'disk_size': Variable('disk_size', 'string', '51200'),
        }
        if DEBUG:
            self.packer_variables['headless'] = Variable('headless', 'string', 'false')
        else:
            self.packer_variables['headless'] = Variable('headless', 'string', 'true')

    def _set_base_source_attributes(self):
        """
        set some basic source attributes, such as cpus, disk_size, memory and the output_directory
        """
        self.source_attributes = {
            'cpus': self.packer_variables['cpus'],
            'disk_size': self.packer_variables['disk_size'],
            'gfx_vram_size': 48,
            'guest_additions_mode': 'attach',
            'hard_drive_interface': 'sata',
            'headless': self.packer_variables['headless'],
            'memory': self.packer_variables['memory'],
            'output_directory': self.output_directory.name,
            'vboxmanage': [["modifyvm", "{{ .Name }}", "--graphicscontroller", "vboxsvga"],["modifyvm", "{{ .Name }}", "--audiocontroller", "ac97"]]
        }

    def _get_image_sha256checksum(self) -> str:
        """
        calculates the sha256 checksum of the os image

        :return: sha256 checksum of os image
        """
        return checksum(self.image.as_posix(), hash_factory=hashlib.sha256).hex()

    def _get_image_path(self) -> Path:
        path = self.image_directory / 'boximage.iso'
        return path

    def _copy_script(self, source: Path, dst_relative_to_scripts_directory: Path) -> Path:
        destination_path_absolute = self.base_directory/'scripts'/dst_relative_to_scripts_directory
        destination_path_absolute.parent.mkdir(exist_ok=True, parents=True)
        shutil.copy(source, destination_path_absolute)
        return destination_path_absolute.relative_to(self.base_directory)

    def _copy_and_set_floppyfile(self, source: Path, dst_relative_to_scripts_directory: Path):
        destination_path_absolute = self.base_directory/'floppyfiles'/dst_relative_to_scripts_directory
        destination_path_absolute.parent.mkdir(exist_ok=True, parents=True)
        shutil.copy(source, destination_path_absolute)
        self.floppy_files.append(destination_path_absolute.relative_to(self.base_directory).as_posix())

    def _set_floppyfile(self, floppy_path_absolute: Path):
        self.floppy_files.append(floppy_path_absolute.relative_to(self.base_directory).as_posix())

    def __add_floppy_files_to_source_attributes(self):
        self.source_attributes['floppy_files'] = self.floppy_files

    def _download_image(self):
        """
        function that download the os image -> needs to be overloaded by subclasses individually
        """
        log.error('the _download_image function is not supported by this box. Please implement it and try again.')
        raise NotImplementedError

    @retry(tries=10, delay=2, backoff=2)
    def cleanup(self, full: bool = False):
        """
        clean up the directory, by removing all used files.

        :param full: if set to false the box directory and the logdirectory will be preserved
        """
        if not self._project_structure_valid:
            log.info(f'no cleanup done due to the invalid project structure')
            return 
        log.info(f'cleanup of boxcreator project structure started')
        if not self.base_directory.is_dir():
            log.warning(f'project directory {self.base_directory} does not exist')
            return
        if full:
            shutil.rmtree(self.base_directory.as_posix())
            log.debug(f'project directory ({self.base_directory}) deleted')
        else:
            for path in self.base_directory.iterdir():
                if path.name not in [self.logdirectory.name, self.box_directory.name]:
                    if path.is_file():
                        path.unlink()
                    if path.is_dir():
                        shutil.rmtree(path.as_posix())

        log.info(f'cleanup of boxcreator project structure was successful')

    def disable_cleanup(self):
        """
        disable the cleanup process used after the box creation is done.
        can be used to debug the build process.
        """
        self.cleanup_active = False

    def set_image(self, image: Path):
        """
        used to set a fix image by a file path instead of downloading the image

        :param image: file path of the image
        """
        if image.is_file():
            dst = self._get_image_path().as_posix()
            shutil.copy(image.as_posix(), dst)
            self.image_pre_set = True
            log.info(f'image {image} is copied to {dst}')
        else:
            log.error(f'provided image with path {image} does not exist')

    def create_box(self, exclude_download: bool = False):
        """
        create a box based on the provided attributes.
        this includes downloading the image, creating the Packerfile, running the Packerfile as well as cleaning up the temporary needed files.
        """
        if not self._project_structure_valid:
            return
        self.__add_floppy_files_to_source_attributes()
        self.source_attributes['vm_name'] = self.label

        if not exclude_download:
            if not self.image_pre_set:
                ret = self._download_image()
                if not ret:
                    log.error(
                        f'download of image failed -> box can not be created please provide an iso or check above log messages')
                    return

        self.__create_packerfile()
        packerfile_path = self.base_directory / 'packerfile.pkr.hcl'
        self.packerfile.set_filepath(packerfile_path)
        self.packerfile.save()
        ret_dict = self.packerfile.build(logfile=self.logdirectory / 'packer.log')
                
        full_cleanup = False
        if ret_dict['returncode'] != 0:
            full_cleanup = True
        if self.cleanup_active:
            self.cleanup(full=full_cleanup)
        if ret_dict['returncode'] != 0:
            print(f'\nBox creation has finished with errors. \nSee above to check them out')
        else:
            print(f'\nBox creation has finished successfully. \nThe created box can be found in {self.box_directory.absolute()} directory')


