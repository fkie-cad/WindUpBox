# internal imports
from windupbox.packerAPI.provisioner import Provisioner
from windupbox.packerAPI.postprocessor import PostProcessor
from windupbox.packerAPI.source import Source

# configure logging
import logging
log = logging.getLogger(__name__)


class BuildBlock:
    """
        represents a packer build block
    """
    sources: list[str] = []
    provisioners: list[Provisioner] = []
    postprocessors: list[PostProcessor] = []

    def __init__(self, sources: list[Source]):
        self.sources = [f'source.{S.first_label}.{S.second_label}' for S in sources]

    def get_sources_as_str(self):
        return str(self.sources).replace('\'', '"')

    def add_provisioner(self, provisioner: Provisioner):
        self.provisioners.append(provisioner)

    def add_postprocessor(self, postprocessor: PostProcessor):
        self.postprocessors.append(postprocessor)
