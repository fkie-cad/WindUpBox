# external imports
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import registry

# internal imports
from windupbox.helperFunctions.sqlalchemy.urigenerator import path_to_sqlite_uri
from .constants import DATABASE_FILE_OSINFO

# configure logging
import logging
log = logging.getLogger(__name__)


mapper_registry = registry()
Base = mapper_registry.generate_base()


def load_database(database_path: Path = DATABASE_FILE_OSINFO) -> Engine:
    """
        load a sqlite database with sqlalchemy and returning and sqlalchemy engine object
    """
    db_uri = path_to_sqlite_uri(database_path)
    engine = create_engine(db_uri)
    mapper_registry.metadata.create_all(engine)
    return engine

