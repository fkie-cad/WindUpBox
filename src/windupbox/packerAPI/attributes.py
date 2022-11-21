# external imports
import attrs
from typing import Any

# internal imports
from windupbox.packerAPI.variable import Variable, VariableStringMix

# configure logging
import logging
log = logging.getLogger(__name__)


def value_to_string(value: Any):
    dtype = type(value)
    if dtype == str:
        return f'"{value}"'
    elif dtype in [int, float]:
        return str(value)
    elif dtype == Variable:
        return f'"${{var.{value.name}}}"'
    elif dtype == VariableStringMix:
        newstring = ""
        for var in value.variables:
            newstring = value.string.replace(value.placeholder, f"${{var.{var.name}}}", 1)
        return f'"{newstring}"'
    elif dtype == list:
        return f'[{",".join([value_to_string(val) for val in value])}]'
    else:
        return ''


@attrs.define
class Attribute:
    """

    """
    name: str
    value: Any

    def str_value(self) -> str:
        return value_to_string(self.value)
