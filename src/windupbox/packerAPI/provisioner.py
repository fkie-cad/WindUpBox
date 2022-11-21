import attrs
from typing import Union

from windupbox.packerAPI.attributes import Attribute
from windupbox.packerAPI.variable import DTYPE_PACKER_VARIABLE

# configure logging
import logging
log = logging.getLogger(__name__)


class Provisioner:
    """
        represent a packer provisioner
    """
    type: str
    attributes: dict

    def __init__(self):
        self.attributes = {}

    def _check(self) -> bool:
        return True


class ScriptProvisoner(Provisioner):
    """
        represent a packer provisioner for scripts such as powershell and shell provisioner
    """
    __code_added = False

    def add_code(self, code_type: str, code: Union[list[Union[DTYPE_PACKER_VARIABLE, str]], Union[DTYPE_PACKER_VARIABLE, str]]):
        if self.__code_added:
            log.error('code got already added to the provisioner')
        if code_type == 'inline':
            if type(code) != list:
                log.error('code type inline requires a list of strings not just a string')
                return
        elif code_type == 'script':
            if type(code) != str:
                log.error('code type script requires a string not a list of strings')
                return
        elif code_type == 'scripts':
            if type(code) != list:
                log.error('code type scripts requires a list of strings not just a string')
                return
        else:
            log.error(f'code type { code_type } is not supported by packer')
            return
        self.attributes[code_type] = Attribute(code_type, code)
        __code_added = True

    def _check(self) -> bool:
        if self.__code_added:
            return True
        else:
            return False


class PowershellProvisioner(ScriptProvisoner):
    """
        represent packers powershell provisioner (https://developer.hashicorp.com/packer/docs/provisioners/powershell)
    """
    type = "powershell"

    def __init__(self, code_type: str, code: Union[list[Union[DTYPE_PACKER_VARIABLE, str]], Union[DTYPE_PACKER_VARIABLE, str]]):
        super().__init__()
        self.add_code(code_type, code)

    def add_elevated_user(self, user: Union[str, DTYPE_PACKER_VARIABLE], password: Union[str, DTYPE_PACKER_VARIABLE]):
        self.attributes['elevated_user'] = Attribute('elevated_user', user)
        self.attributes['elevated_password'] = Attribute('elevated_password', password)

    def add_custom_attribute(self, key: str, val: Union[str, DTYPE_PACKER_VARIABLE]):
        self.attributes[key] = Attribute(key, val)
