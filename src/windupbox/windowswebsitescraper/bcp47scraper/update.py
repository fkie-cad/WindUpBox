# external imports
import pandas as pd
import requests

# internal imports
from .constants import LINK, WINDOWS_BCP47_CODES

# configure logging
import logging
log = logging.getLogger(__name__)


def update_bcp47_codes(file=WINDOWS_BCP47_CODES):
    req = requests.get(LINK)
    df_list = pd.read_html(req.content.decode('utf-8'))
    df = df_list[0]
    df.columns = ['code', 'name', 'bcp47code']
    df = df.drop(df[df['bcp47code'].isnull()].index)
    df.to_csv(file)


