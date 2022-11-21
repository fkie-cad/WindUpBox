# external imports
import attrs
from sqlalchemy import Table, Column, Integer, Boolean, String

# internal imports
from windupbox.osinfo.osinfo import OsInfo, OsInfoFilter
from .load_database import mapper_registry

# configure logging
import logging
log = logging.getLogger(__name__)


@mapper_registry.mapped
@attrs.define(slots=False)
class WindowsInfo(OsInfo):
    """
        stores information about a specific Windows version
    """
    __table__ = Table(
        'windows_os_available',
        mapper_registry.metadata,
        Column('id', Integer, primary_key=True),
        Column('windows_version', String),
        Column('version', String),
        Column('edition', String),
        Column('language', String),
        Column('architecture', String),
        Column('build', String),
        Column('release', String),
        # Column('language_bcp47', String),
        Column('tested', Boolean),
    )
    windows_version: str or None = attrs.field(default=None)
    version: str or None = attrs.field(default=None)
    edition: str or None = attrs.field(default=None)
    language: str or None = attrs.field(default=None)
    architecture: str or None = attrs.field(default=None)
    build: str = attrs.field(default='')
    release: str = attrs.field(default='')
    language_bcp47: str or None = attrs.field(default=None)
    language_bcp47_installation_uilanguage: str or None = attrs.field(default=None)
    tested: bool = attrs.field(default=False)

    label: str = attrs.field(init=False)

    def __attrs_post_init__(self):
        if self.windows_version and self.version and self.edition and self.language:
            self.set_label(f'{self.windows_version} {self.edition} {self.version} {self.language}')
        else:
            self.set_label('')

    def is_valid(self) -> bool:
        if self.return_missing_attributes():
            return False
        else:
            return True

    def return_missing_attributes(self) -> list:
        __mandatory_attributes = {
            'windows_version': self.windows_version,
            'version': self.version,
            'edition': self.edition,
            'language': self.language,
            'architecture': self.architecture
        }
        missing_attributes = []
        for key, value in __mandatory_attributes.items():
            if not value:
                missing_attributes.append(key)
        return missing_attributes

    @classmethod
    def get_mandatory_attributes(cls) -> list:
        return ['windows_version', 'version', 'edition', 'language', 'architecture']

    def set_label(self, label: str):
        self.label = label

    def set_version(self, version: str):
        self.version = version
        self.__attrs_post_init__()

    def set_edition(self, edition: str):
        self.edition = edition
        self.__attrs_post_init__()

    def set_language(self, language: str):
        self.language = language
        self.__attrs_post_init__()

    def set_bcp47(self, bcp47_code: str):
        self.language_bcp47 = bcp47_code
        self.__attrs_post_init__()

    def set_ui_bcp47(self, bcp47_code: str):
        self.language_bcp47_installation_uilanguage = bcp47_code
        self.__attrs_post_init__()

    def __repr__(self):
        self.__attrs_post_init__()
        return self.label

    def as_list(self) -> list:
        return [self.windows_version, self.edition, self.version, self.build, self.release]

    @classmethod
    def from_dict(cls, windows_info_dict: dict):
        obj = cls(**windows_info_dict)
        return obj



@attrs.define(slots=False)
class WindowsInfoFilter(OsInfoFilter):
    """
        a filter for WindowsInfo, that take into account Windows version, version, edition, language and architecture
    """
    windows_version: list = attrs.field(default=None)
    version: list = attrs.field(default=None)
    edition: list = attrs.field(default=None)
    language: list = attrs.field(default=None)
    architecture: list = attrs.field(default=None)

    def match(self, windows_info: WindowsInfo) -> int:
        parameters = [
            [self.windows_version, windows_info.windows_version],
            [self.version, windows_info.version],
            [self.edition, windows_info.edition],
            [self.language, windows_info.language],
            [self.architecture, windows_info.architecture]
        ]

        match_level = 0
        for parameter in parameters:
            filter_param = parameter[0]
            info_param = parameter[1]
            if not filter_param:
                break
            if info_param in filter_param:
                match_level += 1
            else:
                break
        return match_level
