from enum import Enum

from tm2p import Field


class Column(Enum):
    """:meta private:"""

    CITAB_YEAR = "CITAB_YEAR"
    CUMUL_GCS = "CUMUL_GCS"
    CUMUL_LCS = "CUMUL_LCS"
    CUMUL_OCC = "CUMUL_OCC"
    GCS = Field.GCS.value
    LCS = Field.LCS.value
    MEAN_GCS = "MEAN_GCS"
    MEAN_LCS = "MEAN_LCS"
    MEAN_GCS_PER_YEAR = "MEAN_GCS_PER_YEAR"
    MEAN_LCS_PER_YEAR = "MEAN_LCS_PER_YEAR"
    OCC = "OCC"
    YEAR = Field.YEAR.value
