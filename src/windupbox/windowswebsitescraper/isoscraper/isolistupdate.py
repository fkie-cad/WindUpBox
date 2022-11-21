# external imports
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import platform
import time
from pathlib import Path

# internal imports
from windupbox.osinfo.constants import DATABASE_FILE_OSINFO
from windupbox.windowswebsitescraper.isoscraper.constants import *
from windupbox.osinfo.windowsinfo import WindowsInfo, mapper_registry
from .isoscraper import WindowsDownloadLinkCreatorStatic, WindowsDownloadLinkCreatorDynamic

# configure logging
import logging
log = logging.getLogger(__name__)

# WINDOWS_ISO_FILE = pkg_resources.resource_filename('windupbox', 'data/windows_download_possibilities.json')


# def load_possible_windows_iso_from_file(file=WINDOWS_ISO_FILE):
#     with open(file, mode='r') as f:
#         data = json.load(f)
#     return data


class WindowsIsoListUpdater:

    def update(self, database_path: Path = DATABASE_FILE_OSINFO):
        local_platform = platform.system()
        if local_platform in ['Linux', 'Darwin']:
            db_uri = f'sqlite:///{database_path.absolute().as_posix()}'
        elif local_platform == 'Windows':
            db_path_windows_style = database_path.absolute().as_posix().replace('/', '\\')
            db_uri = f'sqlite:///{db_path_windows_style}'
        else:
            return
        engine = create_engine(db_uri)
        mapper_registry.metadata.create_all(engine)
        # create session and add objects
        with Session(engine) as session:
            for windows_version in SUPPORTED_WINDOWS_VERSIONS:
                print(windows_version)
                link_mapping = WINDOWS_LINK_MAPPING[windows_version]
                code_mapping = WINDOWS_CODE_MAPPING[windows_version]
                print(link_mapping, code_mapping)
                for mapping in [link_mapping, code_mapping]:
                    if mapping:
                        for version in mapping.keys():
                            build = None
                            release = None
                            if type(mapping[version]) == dict:
                                if 'build' in mapping[version].keys():
                                    build = mapping[version]['build']
                                if 'release' in mapping[version].keys():
                                    release = mapping[version]['release']
                            for edition in mapping[version]['editions'].keys():
                                if mapping[version]['editions'][edition]:
                                    if mapping == link_mapping:
                                        wincreator = WindowsDownloadLinkCreatorStatic(WindowsInfo(windows_version, version, edition))
                                    else:
                                        wincreator = WindowsDownloadLinkCreatorDynamic(WindowsInfo(windows_version, version, edition))
                                    lang_arch_dict = wincreator.get_supported_languages_and_architectures()
                                    time.sleep(0.5)
                                    for lang in lang_arch_dict.keys():
                                        for arch in lang_arch_dict[lang]:
                                            windows_info = WindowsInfo(
                                                windows_version=windows_version,
                                                version=version,
                                                edition=edition,
                                                language=lang,
                                                architecture=arch,
                                                build=build,
                                                release=release
                                            )
                                            session.add(windows_info)
            session.commit()

        # def update(self, list_file: Path = WINDOWS_ISO_FILE):
        #     result_dict = dict()
        #     for windows_version in SUPPORTED_WINDOWS_VERSIONS:
        #         result_dict[windows_version] = dict()
        #         link_mapping = WINDOWS_LINK_MAPPING[windows_version]
        #         code_mapping = WINDOWS_CODE_MAPPING[windows_version]
        #         for mapping in [link_mapping, code_mapping]:
        #             if mapping:
        #                 result_dict[windows_version].update(mapping.copy())
        #                 for version in mapping.keys():
        #                     for edition in mapping[version]['editions'].keys():
        #                         if mapping[version]['editions'][edition]:
        #                             if mapping == link_mapping:
        #                                 wincreator = WindowsDownloadLinkCreatorStatic(WindowsInfo(windows_version, version, edition))
        #                             else:
        #                                 wincreator = WindowsDownloadLinkCreatorDynamic(WindowsInfo(windows_version, version, edition))
        #                             lang_arch_dict = wincreator.get_supported_languages_and_architectures()
        #                             time.sleep(0.5)
        #                             result_dict[windows_version][version]['editions'][edition] = lang_arch_dict
        #     result_dict = delete_none(result_dict)
        #     with open(list_file, mode='w') as f:
        #         json.dump(result_dict, f, indent=3)

