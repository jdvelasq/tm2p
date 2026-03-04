from enum import Enum


class RecordOrderBy(Enum):

    GCS_HIGHEST = "GCS_HIGHEST"
    GCS_LOWEST = "GCS_LOWEST"

    LCS_HIGHEST = "LCS_HIGHEST"
    LCS_LOWEST = "LCS_LOWEST"

    AUTH_A_TO_Z = "AUTH_A_TO_Z"
    AUTH_Z_TO_A = "AUTH_Z_TO_A"

    YEAR_NEWEST = "YEAR_NEWEST"
    YEAR_OLDEST = "YEAR_OLDEST"

    SRC_A_TO_Z = "SRC_A_TO_Z"
    SRC_Z_TO_A = "SRC_Z_TO_A"
