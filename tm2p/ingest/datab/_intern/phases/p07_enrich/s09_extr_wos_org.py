from pathlib import Path

import pandas as pd  # type: ignore

from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip
from tm2p._intern.packag_data import load_builtin_mapping
from tm2p.ingest.datab._intern.oper.ltwa_col import ltwa_column

from ...__affil._internals import (
    extract_country_name_from_string,
    extract_org_name_from_string,
)

AFFIL_RAW = Field.AFFIL_RAW.value
CTRY_AFFIL = Field.CTRY_AFFIL.value
CTRY = Field.CTRY.value
CTRY_FIRST = Field.CTRY_FIRST.value
CTRY_ISO3 = Field.CTRY_ISO3.value
CTRY_ISO3_FIRST = Field.CTRY_ISO3_FIRST.value
ORG_FIRST = Field.ORG_FIRST.value

ORG = Field.ORG_RAW.value


def s09_extr_wos_org(root_directory: str) -> int:

    return 0
