import attrs
from typing import Union


@attrs.define
class Variable:
    name: str
    type: str
    default: str


@attrs.define
class VariableStringMix:
    variables: list[Variable]
    string: str
    placeholder: str = '%VAR%'


DTYPE_PACKER_VARIABLE = Union[Variable, VariableStringMix]
