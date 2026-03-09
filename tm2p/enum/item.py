from enum import Enum

from .column import G_INDEX as G_INDEX_
from .column import GCS as GCS_
from .column import GCS_PER_YEAR as GCS_PER_YEAR_
from .column import GCS_PER_YEAR_AVG as GCS_PER_YEAR_AVG_
from .column import H_INDEX as H_INDEX_
from .column import LCS as LCS_
from .column import LCS_PER_YEAR as LCS_PER_YEAR_
from .column import M_INDEX as M_INDEX_
from .column import OCC as OCC_


class ItemOrderBy(Enum):

    OCC = OCC_
    GCS = GCS_
    LCS = LCS_

    LCS_PER_YEAR = LCS_PER_YEAR_
    GCS_PER_YEAR = GCS_PER_YEAR_

    GCS_PER_YEAR_AVG = GCS_PER_YEAR_AVG_

    H_INDEX = H_INDEX_
    G_INDEX = G_INDEX_
    M_INDEX = M_INDEX_
