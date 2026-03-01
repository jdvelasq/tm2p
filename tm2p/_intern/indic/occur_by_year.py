"""
Smoke tests:
    >>> from tm2p import CorpusField, ItemsOrderBy
    >>> from tm2p._intern.indic.occur_by_year import OccurrencesByYear
    >>> df = (
    ...     OccurrencesByYear()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(CorpusField.AUTHKW_NORM)
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # PARAMS:
    ...     .using_cumulative_sum(False)
    ...     #
    ...     # COUNTERS:
    ...     .using_item_counters(True)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
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
    >>> df.head(10) # doctest: +NORMALIZE_WHITESPACE
    YEAR                               2015  2016  2017  ...  2022  2023  2024
    AUTHKW_NORM                                          ...
    fintech 117:25478                     0    11    11  ...    13    17    17
    financial inclusion 017:03823         0     1     3  ...     4     3     2
    financial technology 014:02508        0     1     1  ...     0     1     2
    green finance 011:02844               0     0     0  ...     3     5     0
    blockchain 011:02023                  0     1     1  ...     0     1     2
    banking 010:02599                     0     1     1  ...     2     1     3
    china 009:01947                       0     1     0  ...     3     1     1
    innovation 009:01703                  0     3     2  ...     1     2     0
    artificial intelligence 008:01915     0     0     0  ...     0     2     1
    financial services 007:01673          0     1     0  ...     0     0     1
    <BLANKLINE>
    [10 rows x 10 columns]


    >>> df = (
    ...     OccurrencesByYear()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(CorpusField.AUTHKW_NORM)
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # PARAMS:
    ...     .using_cumulative_sum(False)
    ...     #
    ...     # COUNTERS:
    ...     .using_item_counters(False)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
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
    YEAR         2015  2016  2017  2018  2019  2020  2021  2022  2023  2024
    AUTHKW_NORM
    fintech         0    11    11    12     6    13    17    13    17    17
    financial       0     1     3     1     1     2     0     4     3     2
    financial       0     1     1     1     1     3     4     0     1     2
    green           0     0     0     0     0     0     3     3     5     0
    blockchain      0     1     1     1     1     3     1     0     1     2
    banking         0     1     1     0     0     1     1     2     1     3
    china           0     1     0     0     0     1     2     3     1     1
    innovation      0     3     2     1     0     0     0     1     2     0
    artificial      0     0     0     0     2     2     1     0     2     1
    financial       0     1     0     4     0     1     0     0     0     1


    >>> df = (
    ...     OccurrencesByYear()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(CorpusField.AUTHKW_NORM)
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # PARAMS:
    ...     .using_cumulative_sum(True)
    ...     #
    ...     # COUNTERS:
    ...     .using_item_counters(True)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
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

from tm2p import CorpusField, ItemsOrderBy
from tm2p._intern import ParamsMixin, SortAxesMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip

from ..get_zero_digits import get_zero_digits
from .bibliom_indic import BibliometricIndicators

GCS = CorpusField.GCS.value
OCC = ItemsOrderBy.OCC.value
YEAR = CorpusField.YEAR.value

COUNTERS = "COUNTERS"


class OccurrencesByYear(
    ParamsMixin,
    SortAxesMixin,
):
    """:meta private:"""

    def _get_years_range(self, df):
        return df[YEAR].min(), df[YEAR].max()

    def _compute_item_occurrences_by_year(self, df):

        field = self.params.source_field.value

        df = df[[field, YEAR]].copy()
        df = df.dropna()

        df[field] = df[field].str.split(";")
        df = df.explode(field)
        df[field] = df[field].str.strip()

        df[OCC] = 1
        df = df.groupby([field, YEAR], as_index=False).agg({OCC: "sum"})
        df = df.set_index(field)
        df = df.pivot(columns=YEAR)
        df.columns = df.columns.droplevel(0)
        df = df.fillna(0)
        df = df.astype(int)

        if self.params.cumulative_sum is True:
            df = df.cumsum(axis=1)

        return df

    def _complete_year_range(self, df, year_range):

        year_min = year_range[0]
        year_max = year_range[1]

        for year in range(year_min, year_max + 1):
            if year not in df.columns:
                df[year] = 0

        df = df.sort_index(axis=1)

        return df

    def _get_items_mapping(self, df):

        field = self.params.source_field.value

        df = df[[field, GCS]].copy()
        df = df.dropna()
        df[field] = df[field].str.split(";")
        df = df.explode(field)
        df[field] = df[field].str.strip()

        df[OCC] = 1
        df = df.groupby(field).agg({OCC: "sum", GCS: "sum"})

        df[COUNTERS] = df.index.astype(str)

        occ_digits, gcs_digits = get_zero_digits(self.params.root_directory)
        df[COUNTERS] += " " + df[OCC].map(lambda x: f"{x:0{occ_digits}d}")
        df[COUNTERS] += ":" + df[GCS].map(lambda x: f"{x:0{gcs_digits}d}")

        mapping = df[COUNTERS].to_dict()

        return mapping

    def _filter_items(self, items_by_year):

        items_by_year = items_by_year.copy()

        terms_in = BibliometricIndicators().update(**self.params.__dict__).run().index
        items_by_year = items_by_year[items_by_year.index.isin(terms_in)]

        return items_by_year

    def _append_counters_to_axis(self, df, mapping):
        df.index = df.index.map(mapping)
        return df

    def _sort_index(self, df):
        return self.sort_index(df)

    def _remove_counter_from_axis(self, df):
        if self.params.item_counters is False:
            df.index = df.index.str.split().str[0]
        return df

    def run(self):

        df = load_filtered_main_csv_zip(params=self.params)

        year_range = self._get_years_range(df)

        items_by_year = self._compute_item_occurrences_by_year(df)
        items_by_year = self._complete_year_range(items_by_year, year_range)

        mapping = self._get_items_mapping(df)

        items_by_year = self._filter_items(items_by_year)
        items_by_year = self._append_counters_to_axis(items_by_year, mapping)
        items_by_year = self._sort_index(items_by_year)
        items_by_year = self._remove_counter_from_axis(items_by_year)

        return items_by_year
