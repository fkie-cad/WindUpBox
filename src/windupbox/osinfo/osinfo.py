# external imports
import attrs

# configure logging
import logging
log = logging.getLogger(__name__)


@attrs.define
class OsInfo:
    """
        abstract parent class for specific os information, such as WindowsInfo
    """
    pass


@attrs.define
class OsInfoFilter:
    """
        abstract parent class for specific os information filter, such as WindowsInfoFilter
    """
    def match(self, os_info: OsInfo) -> int:
        """
            abstract method to check how well an OsInfo instance matches the filter
        """
        pass
