# external imports
import pycdlib as pycdlib
from pathlib import Path

# configure logging
import logging
log = logging.getLogger(__name__)


def extract_languagecodes_from_windows_os_iso(iso_path: Path) -> list:

    iso = pycdlib.PyCdlib()
    iso.open(iso_path.as_posix())

    language_codes = []
    for child in iso.list_children(udf_path='/boot'):
        if child:
            if child.is_dir():
                dir_name = child.file_identifier().decode('utf-16-be')
                if len(dir_name) == 5 and dir_name[2] == '-':
                    language_codes.append(dir_name)
    iso.close()
    return language_codes
