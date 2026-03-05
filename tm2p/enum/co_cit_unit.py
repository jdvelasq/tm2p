from enum import Enum

from .field import Field


class CoCitationUnit(Enum):

    CITED_AUTH = Field.AUTH_NORM.value
    CITED_REF = "REF"
    CITED_SRC = Field.SRC_ISO4_NORM.value
