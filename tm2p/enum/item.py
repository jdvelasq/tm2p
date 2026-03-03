from enum import Enum

from .common import Common


class ItemOrderBy(Enum):

    OCC = Common.OCC.value
    GCS = Common.GCS.value
    LCS = Common.LCS.value

    LCS_PER_YEAR = Common.LCS_PER_YEAR.value
    GCS_PER_YEAR = Common.GCS_PER_YEAR.value

    GCS_PER_YEAR_AVG = Common.GCS_PER_YEAR_AVG.value

    H_INDEX = Common.H_INDEX.value
    G_INDEX = Common.G_INDEX.value
    M_INDEX = Common.M_INDEX.value
