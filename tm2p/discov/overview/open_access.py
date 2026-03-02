"""
Open access
=========================================================================================

Smoke test:
    >>> import pandas as pd
    >>> from tm2p.discov.overview import OpenAccess
    >>> oa = (
    ...     OpenAccess()
    ...     #
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> assert isinstance(oa, pd.Series)
    >>> assert len(oa) > 0
    >>> oa
    OPEN_ACCESS
    all open access               66
    green open access             52
    green accepted open access    51
    gold open access              28
    hybrid gold open access       22
    bronze open access             5
    green final open access        3
    Name: count, dtype: int64


"""

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p.enum.corpus import Field

__reviewed__ = "2026-01-29"


class OpenAccess(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        open_access = Field.OA.value

        df = load_filtered_main_csv_zip(params=self.params)
        return (
            df[open_access]
            .dropna()
            .str.split("; ")
            .explode()
            .str.strip()
            .str.lower()
            .value_counts()
            .sort_index()
            .sort_values(ascending=False)
        )
