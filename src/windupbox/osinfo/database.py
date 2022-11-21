# external imports
from pathlib import Path
from sqlalchemy.orm import Session
import prettytable

# internal imports
from .constants import DATABASE_FILE_OSINFO
from .windowsinfo import WindowsInfo
from .load_database import load_database

# configure logging
import logging
log = logging.getLogger(__name__)


def load_windowsinfo_table(database_path: Path = DATABASE_FILE_OSINFO) -> list:
    """
        load all instances of the WindowsInfo class from a given database
    """
    engine = load_database(database_path)
    with Session(engine) as session:
        windowsinfo_instances = session.query(WindowsInfo).all()
    return windowsinfo_instances


def return_if_exists(windows_info: WindowsInfo, database_path: Path = DATABASE_FILE_OSINFO):
    """
        return whether a certain WindowsInfo instance is already present in the os information database
    """
    engine = load_database(database_path)
    with Session(engine) as session:
        filter_keys = ['windows_version', 'version', 'edition', 'language', 'architecture']
        filter_list = [getattr(WindowsInfo, key) == getattr(windows_info, key) for key in filter_keys]
        results = session.query(WindowsInfo).filter(*filter_list).all()
    if results:
        return results
    return None


def get_table_as_list(database_path: Path = DATABASE_FILE_OSINFO, select: list = None, filters: dict = None) -> list:
    """
        return all os information lines from the os information database preprocessed with filters (:param filters) and column selections (:param select)
    """
    engine = load_database(database_path)
    with Session(engine) as session:
        if not filters:
            if not select:
                results = session.query(WindowsInfo).distinct().all()
            else:
                attributes = [getattr(WindowsInfo, a) for a in select]
                results = session.query(WindowsInfo).with_entities(*attributes).distinct().all()
        else:
            filter_list = [getattr(WindowsInfo, key) == val for key, val in filters.items()]
            if not select:
                session.query(WindowsInfo).filter(*filter_list).distinct().all()
            else:
                attributes = [getattr(WindowsInfo, a) for a in select]
                results = session.query(WindowsInfo).with_entities(*attributes).filter(*filter_list).distinct().all()
    return results


def print_table(database_path: Path = DATABASE_FILE_OSINFO, select: list = None, filters: dict = None):
    """
        print certain os information from the os information database dependent on filters (:param filters) and a column selections (:param select)
    """
    if not select:
        select = ['windows_version', 'version', 'edition', 'language', 'architecture', 'tested']
    table_data = get_table_as_list(database_path=database_path, select=select, filters=filters)
    table = prettytable.PrettyTable()
    table.field_names = select
    table_data_listformat = [[getattr(windows_info, attribute) for attribute in select] for windows_info in table_data]
    table.add_rows(table_data_listformat)
    print(table)
