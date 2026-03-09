"""
InspectColumn
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.ingest.oper import InspectColumn
    >>> items = (
    ...     InspectColumn()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.PUBTYPE_NORM)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     #
    ...     .run()
    ... )
    >>> from pprint import pprint
    >>> pprint(items[:10])
    PUBTYPE_NORM
    Article             142
    Review               14
    Book                  8
    Conference paper      7
    Book chapter          3
    Editorial             3
    Retracted             1
    Note                  1
    Short survey          1
    Name: count, dtype: int64



"""

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip


class InspectColumn(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        df = load_filtered_main_csv_zip(params=self.params)
        series = df[self.params.source_field.value].copy()
        series = series.dropna()
        series = series.str.split(";")
        series = series.explode()
        series = series.str.strip()
        values = series.value_counts()

        return values
