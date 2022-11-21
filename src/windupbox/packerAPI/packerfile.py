# external imports
from pathlib import Path
import pkg_resources
from typing import Union

# internal imports
from windupbox.packerAPI.variable import Variable
from windupbox.packerAPI.source import Source
from windupbox.packerAPI.commands import packer_build
from windupbox.packerAPI.buildblock import BuildBlock
from windupbox.helperFunctions.jinja import init_jinja_environment

# configure logging
import logging
log = logging.getLogger(__name__)


class Packerfile:
    """
        represents a Packerfile
    """
    variables: list[Variable] = []
    sources: list[Source] = []
    buildblock: BuildBlock = None
    filepath: Path

    def __check(self) -> bool:
        """
            check whether Packerfile contains all necessary sections (sources, buildblock) as well as a filepath to be saved to
        """
        if not self.sources:
            log.error(f'packerfile is missing a source block')
            return False
        if not self.buildblock:
            log.error(f'packerfile is missing a build block')
            return False
        if not self.filepath:
            log.error(f'filepath to save the file is not set (please set it with set_filepath()')
            return False
        return True

    def add_variables(self, variable: Union[list[Variable], Variable]):
        """
            add variables to the Packerfile
        """
        if type(variable) == list:
            self.variables += variable
        elif type(variable) == Variable:
            self.variables.append(variable)

    def add_source(self, source: Source):
        """
            set source of the Packerfile
        """
        self.sources.append(source)

    def set_buildblock(self, buildblock: BuildBlock):
        """
            set the buildblock of the Packerfile
        """
        if self.buildblock:
            log.error(f'build block is already set')
            return
        self.buildblock = buildblock

    def set_filepath(self, filepath: Path):
        """
            set the filepath of the Packerfile
        """
        self.filepath = filepath

    def build(self, logfile: Path = None) -> dict:
        """
            start packer build process
        """
        if not self.filepath.is_file():
            log.error(f'please save the file first before trying to build it')
            return dict()
        if logfile:
            return packer_build(self.filepath, logfile=logfile)
        else:
            return packer_build(self.filepath)

    def save(self):
        """
            save the Packerfile to a file by using a jinja2 template
        """
        if not self.__check():
            log.error(f'check failed -> can NOT save packerfile')
        template_folder = Path(pkg_resources.resource_filename('windupbox', 'data/templates/'))
        jinja_env = init_jinja_environment(template_folder)
        template = jinja_env.get_template('packertemplate.pkr.hcl')
        with open(self.filepath.as_posix(), mode="w") as f:
            f.write(
                template.render(
                    {
                        'variables': self.variables,
                        'sources': self.sources,
                        'buildblock': self.buildblock
                    }
                )
            )
