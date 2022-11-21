# external imports
import attrs
from typing import Any

# internal imports
from windupbox.packerAPI.attributes import Attribute

# configure logging
import logging
log = logging.getLogger(__name__)


@attrs.define
class Source:
    first_label: str
    second_label: str

    attributes: dict = attrs.Factory(dict)

    def __add_attribute_to_attributes(self, name: str, value: Any):
        attribute = Attribute(name, value)
        if attribute.name in self.attributes.keys():
            log.warning(f'Attribute {attribute.name} will get overwritten.')
        self.attributes[attribute.name] = attribute

    def set_attribute(self, name: str, value: Any):
        self.__add_attribute_to_attributes(name, value)

    def set_attribute_by_dict(self, attr_dict: dict):
        for key, value in attr_dict.items():
            self.__add_attribute_to_attributes(key, value)
