# external imports
from typing import Any

# internal imports
from windupbox.packerAPI.attributes import Attribute

# configure logging
import logging
log = logging.getLogger(__name__)


class PostProcessor:
    """
        represents a packer post-processor
    """
    type: str
    attributes: dict

    def __init__(self):
        self.attributes = {}

    def _check(self) -> bool:
        return True


class VagrantPostProcessor(PostProcessor):
    """
        represents packers vagrant post-processor (https://developer.hashicorp.com/packer/plugins/post-processors/vagrant/vagrant)
    """
    type = 'vagrant'

    def __init__(self):
        super().__init__()

    def add_compression_level(self, value: int):
        self.attributes['compression_level'] = Attribute('compression_level', value)

    def add_output(self, value: Any):
        self.attributes['output'] = Attribute('output', value)
