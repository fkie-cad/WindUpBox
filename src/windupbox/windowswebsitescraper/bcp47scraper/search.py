# external imports
import pandas as pd

# internal imports
from .constants import WINDOWS_BCP47_CODES

# configure logging
import logging
log = logging.getLogger(__name__)


def search(provide: tuple, get: str, contain=True) -> list:
    df: pd.DataFrame = pd.read_csv(WINDOWS_BCP47_CODES)
    result = df[df[provide[0]] == provide[1]]
    if result.empty:
        if contain:
            found_lines = df.apply(lambda row: provide[1] in row[provide[0]], axis=1)
            found_entries = df[found_lines].values
            if len(found_entries) <= 0:
                log.error(f'no entries for {provide} could be found')
                return []
            else:
                return df[found_lines][get].tolist()
    else:
        return result[get].tolist()


def check_bcp47_code(bcp47: str) -> bool:
    df: pd.DataFrame = pd.read_csv(WINDOWS_BCP47_CODES)
    result = df[df['bcp47code'] == bcp47].tolist()
    return result


def bcp47_to_language(bcp47: str) -> list:
    return search(
        ('bcp47code', bcp47),
        'name'
    )


def language_to_bcp47(lang: str) -> list:
    return search(
        ('name', lang),
        'bcp47code'
    )
