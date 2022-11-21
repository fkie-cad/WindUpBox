# external imports
from pathlib import Path
import pkg_resources

# internal imports
from windupbox.helperFunctions.configlocation import get_default_config_directory

# configure logging
import logging
log = logging.getLogger(__name__)

try:
    CONFIG_DIR = get_default_config_directory(create_if_missing=True)
except (FileNotFoundError, FileExistsError, NotADirectoryError, IsADirectoryError) as e:
    CONFIG_DIR = None

if not CONFIG_DIR:
    CONFIG_DIR = Path(pkg_resources.resource_filename('windupbox', '/data/'))
    log.warning(f'the config directory could not be set - therefore {CONFIG_DIR} will be used as the database path')

DATABASE_FILE_OSINFO = CONFIG_DIR/'osinfo.db'
