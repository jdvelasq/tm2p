from enum import Enum

from .field import Field


class CitationUnit(Enum):

    AUTH = Field.AUTH_NORM.value
    CTRY = Field.CTRY_ISO3.value
    DOC = "DOC"
    ORG = Field.ORG.value
    SRC = Field.SRC_ISO4_NORM.value
