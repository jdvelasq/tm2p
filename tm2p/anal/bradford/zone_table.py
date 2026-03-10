"""
ZoneTable
===============================================================================

Smoke tests:
    >>> from tm2p.anal.bradford import ZoneTable
    >>> (
    ...     ZoneTable()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).head() # doctest: +NORMALIZE_WHITESPACE
                                NO  OCC  CUM_OCC   GCS  ZONE
    SRC_ISO4_NORM
    RESOUR POLIC                 1    7        7  1074     1
    TECHNOL FORECAST SOC CHANG   2    6       13  1575     1
    INT REV FINANC ANAL          3    5       18   992     1
    FINANC INNOV                 4    5       23   877     1
    EUR J FINANC                 5    4       27  1002     1


"""

from tm2p import Field
from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip

SRC_ISO4_NORM = Field.SRC_ISO4_NORM.value
GCS = Field.GCS.value
OCC = "OCC"
CUM_OCC = "CUM_OCC"
ZONE = "ZONE"


class ZoneTable(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def internal__load_filtered_records(self):
        self.records = load_filtered_main_csv_zip(params=self.params)

    # -------------------------------------------------------------------------
    def internal__compute_citations_and_occurrences_by_source(self):

        indicators = self.records[[SRC_ISO4_NORM, GCS]]
        indicators = indicators.assign(OCC=1)
        indicators = indicators.groupby([SRC_ISO4_NORM], as_index=False).sum()
        indicators = indicators.sort_values(by=[OCC, GCS], ascending=False)
        indicators = indicators.assign(CUM_OCC=indicators[OCC].cumsum())
        indicators = indicators.assign(NO=1)
        indicators = indicators.assign(NO=indicators.NO.cumsum())

        self.indicators = indicators

    # -------------------------------------------------------------------------
    def internal__compute_zones(self):

        indicators = self.indicators.copy()
        cum_occ = indicators[OCC].sum()
        indicators = indicators.reset_index(drop=True)
        indicators = indicators.assign(ZONE=3)
        indicators.ZONE = indicators.ZONE.where(
            indicators.CUM_OCC >= int(cum_occ * 2 / 3), 2
        )
        indicators.ZONE = indicators.ZONE.where(
            indicators.CUM_OCC >= int(cum_occ / 3), 1
        )
        indicators = indicators.set_index(SRC_ISO4_NORM)
        indicators = indicators[["NO", OCC, CUM_OCC, GCS, ZONE]]

        self.indicators = indicators

    # -------------------------------------------------------------------------
    def run(self):

        self.internal__load_filtered_records()
        self.internal__compute_citations_and_occurrences_by_source()
        self.internal__compute_zones()

        return self.indicators


#

#
#
