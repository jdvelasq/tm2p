from enum import Enum

from .field import Field


class CouplingUnit(Enum):

    AUTH = Field.AUTH_NORM.value
    CTRY = Field.CTRY_ISO3.value
    DOC = "DOC"
    ORG = Field.ORG_NORM.value
    SRC = Field.SRC_ISO4_NORM.value
