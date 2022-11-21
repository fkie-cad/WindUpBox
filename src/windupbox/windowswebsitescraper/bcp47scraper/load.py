# external imports
import pandas as pd

# internal imports
from .constants import WINDOWS_BCP47_CODES

# configure logging
import logging
log = logging.getLogger(__name__)


def load_as_dict(orient='records') -> dict:
    df: pd.DataFrame = pd.read_csv(WINDOWS_BCP47_CODES)
    return df.to_dict(orient=orient)
