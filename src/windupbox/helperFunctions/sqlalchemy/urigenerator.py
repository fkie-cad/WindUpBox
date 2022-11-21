# external imports
from pathlib import Path
import platform

# configure logging
import logging
log = logging.getLogger(__name__)


def path_to_sqlite_uri(path: Path) -> str:
    """
        converts a path to a valid splite uri depending on the host os
    """
    local_platform = platform.system()
    db_uri = ''
    if local_platform in ['Linux', 'Darwin']:
        db_uri = f'sqlite:///{path.absolute().as_posix()}'
    elif local_platform == 'Windows':
        db_path_windows_style = path.absolute().as_posix().replace('/', '\\')
        db_uri = f'sqlite:///{db_path_windows_style}'
    return db_uri
