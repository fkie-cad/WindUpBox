# external imports
from pathlib import Path
from sqlalchemy.orm import Session

# internal imports
from .constants import DATABASE_FILE_OSINFO
from .windowsinfo import WindowsInfo
from .load_database import load_database
from .database import return_if_exists

# configure logging
import logging
log = logging.getLogger(__name__)


def add_windowsinfo_to_database(windows_info: WindowsInfo, database_path: Path = DATABASE_FILE_OSINFO) -> bool:
    """
        add a windows info instance to the database
    """
    engine = load_database(database_path)
    if return_if_exists(windows_info, database_path=database_path):
        log.error(f'windows info can not be added to the os info database {database_path} because it already exists')
        return False
    with Session(engine) as session:
        session.add(windows_info)
        session.commit()
    log.info(f'windows info was successfully added to the os info database {database_path}')
    return True


def remove_windowsinfo_to_database(windows_info: WindowsInfo, database_path: Path = DATABASE_FILE_OSINFO) -> bool:
    """
        add a windows info instance to the database
    """
    engine = load_database(database_path)
    query = return_if_exists(windows_info, database_path=database_path)
    if not query:
        log.error(f'windows info can not be remove from the os info database {database_path} because it does not exist')
        return False
    with Session(engine) as session:
        query.delete()
        session.commit()
    log.info(f'windows info was successfully removed from the os info database {database_path}')
    return True


def set_tested(windows_info: WindowsInfo, database_path: Path = DATABASE_FILE_OSINFO):
    """
        set a certain entry as tested
    """
    engine = load_database(database_path)
    instances = return_if_exists(windows_info, database_path=database_path)
    if not instances:
        log.error(f'windows info can not be set to tested in the os info database {database_path} because it does not exist')
        return
    with Session(engine) as session:
        for instance in instances:
            instance.tested = True
        session.commit()
