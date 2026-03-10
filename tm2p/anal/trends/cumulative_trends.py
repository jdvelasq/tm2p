"""
CumulativeTrends
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.anal.trends import CumulativeTrends
    >>> df = (
    ...     CumulativeTrends()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> type(df).__name__
    'DataFrame'
    >>> df.shape[0] > 0
    True
    >>> df.shape[1] > 0
    True
    >>> df.head(10)  # doctest: +NORMALIZE_WHITESPACE
    YEAR                     2015  2016  2017  2018  ...  2021  2022  2023  2024
    AUTHKW_NORM                                      ...
    fintech                     0    11    22    34  ...    70    83   100   117
    financial inclusion         0     1     4     5  ...     8    12    15    17
    financial technology        0     1     2     3  ...    11    11    12    14
    green finance               0     0     0     0  ...     3     6    11    11
    blockchain                  0     1     2     3  ...     8     8     9    11
    banking                     0     1     2     2  ...     4     6     7    10
    china                       0     1     1     1  ...     4     7     8     9
    innovation                  0     3     5     6  ...     6     7     9     9
    artificial intelligence     0     0     0     0  ...     5     5     7     8
    financial services          0     1     1     5  ...     6     6     6     7
    <BLANKLINE>
    [10 rows x 10 columns]



    >>> df = (
    ...     CumulativeTrends()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> type(df).__name__
    'DataFrame'
    >>> df.shape[0] > 0
    True
    >>> df.shape[1] > 0
    True
    >>> df.head(10)  # doctest: +NORMALIZE_WHITESPACE
    YEAR                               2015  2016  2017  ...  2022  2023  2024
    AUTHKW_NORM                                          ...
    fintech 117:25478                     0    11    22  ...    83   100   117
    financial inclusion 017:03823         0     1     4  ...    12    15    17
    financial technology 014:02508        0     1     2  ...    11    12    14
    green finance 011:02844               0     0     0  ...     6    11    11
    blockchain 011:02023                  0     1     2  ...     8     9    11
    banking 010:02599                     0     1     2  ...     6     7    10
    china 009:01947                       0     1     1  ...     7     8     9
    innovation 009:01703                  0     3     5  ...     7     9     9
    artificial intelligence 008:01915     0     0     0  ...     5     7     8
    financial services 007:01673          0     1     1  ...     6     6     7
    <BLANKLINE>
    [10 rows x 10 columns]



"""

from tm2p._intern import ParamsMixin

from .trends import Trends


class CumulativeTrends(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        df = Trends().update(**self.params.__dict__).run()
        df = df.cumsum(axis=1)
        return df
