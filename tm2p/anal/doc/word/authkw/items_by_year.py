"""
Items by year
===============================================================================

Smoke tests:
    >>> from tm2p.analyze.documents.words.author_keywords import ItemsByYear
    >>> df = (
    ...     ItemsByYear()
    ...     #
    ...     # FIELD:
    ...     .with_field("author_keywords_raw")
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by("OCC")
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
    >>> df.head(10)





"""

from tm2p._intern import ParamsMixin, SortAxesMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p.anal._intern.performance.performance_metrics import (
    PerformanceMetrics as PerformanceDataFrame,
)


class ItemsByYear(
    ParamsMixin,
    SortAxesMixin,
):
    """:meta private:"""

    # ----------------------------------------------------------------------------------------------------
    def _step_1_load_the_database(self):
        return load_filtered_main_csv_zip(params=self.params)

    def _step_2_get_years_range(self, data_frame):
        return data_frame.year.min(), data_frame.year.max()

    # ----------------------------------------------------------------------------------------------------
    def _step_3_compute_term_occurrences_by_year(self, data_frame):

        field = self.params.source_field

        # select the columns field and year
        data_frame = data_frame.reset_index()
        data_frame = data_frame[[field, "year"]].copy()
        data_frame = data_frame.dropna()

        # explode the field column
        data_frame[field] = data_frame[field].str.split(";")
        data_frame = data_frame.explode(field)
        data_frame[field] = data_frame[field].str.strip()

        # create the matrix of term occurrences by year
        data_frame["OCC"] = 1
        data_frame = data_frame.groupby([field, "year"], as_index=False).agg(
            {"OCC": "sum"}
        )
        data_frame = data_frame.set_index(field)
        data_frame = data_frame.pivot(columns="year")
        data_frame.columns = data_frame.columns.droplevel(0)
        data_frame = data_frame.fillna(0)
        data_frame = data_frame.astype(int)

        if self.params.cumulative_sum is True:
            data_frame = data_frame.cumsum(axis=1)

        return data_frame

    # ----------------------------------------------------------------------------------------------------
    def _step_4_check_years(self, data_frame, years_range):
        year_min = years_range[0]
        year_max = years_range[1]
        for year in range(year_min, year_max + 1):
            if year not in data_frame.columns:
                data_frame[year] = 0
        data_frame = data_frame.sort_index(axis=1)
        return data_frame

    # ----------------------------------------------------------------------------------------------------
    def _step_5_get_terms_mapping(self, data_frame):

        field = self.params.source_field

        data_frame = data_frame[[field, "global_citations"]].copy()
        data_frame = data_frame.dropna()
        data_frame[field] = data_frame[field].str.split(";")
        data_frame = data_frame.explode(field)
        data_frame[field] = data_frame[field].str.strip()

        data_frame["OCC"] = 1
        data_frame = data_frame.groupby(field).agg(
            {"OCC": "sum", "global_citations": "sum"}
        )

        data_frame["counters"] = data_frame.index.astype(str)

        n_zeros_occ = len(str(data_frame["OCC"].max()))
        data_frame["counters"] += " " + data_frame["OCC"].map(
            lambda x: f"{x:0{n_zeros_occ}d}"
        )

        n_zeros_citations = len(str(data_frame["global_citations"].max()))
        data_frame["counters"] += ":" + data_frame["global_citations"].map(
            lambda x: f"{x:0{n_zeros_citations}d}"
        )

        mapping = data_frame["counters"].to_dict()

        return mapping

    # ----------------------------------------------------------------------------------------------------
    def _step_6_filter_terms(self, terms_by_year):
        terms_in = PerformanceDataFrame().update(**self.params.__dict__).run().index
        terms_by_year = terms_by_year[terms_by_year.index.isin(terms_in)]
        return terms_by_year

    # ----------------------------------------------------------------------------------------------------
    def _step_7_append_counters_to_axis(self, data_frame, mapping):
        data_frame.index = data_frame.index.map(mapping)
        return data_frame

    # ----------------------------------------------------------------------------------------------------
    def _step_8_sort_index(self, data_frame):
        return self.sort_index(data_frame)

    def _step_9_remove_counter_from_axis(self, data_frame):
        if self.params.item_counters is False:
            data_frame.index = data_frame.index.str.split().str[0]
        return data_frame

    # ----------------------------------------------------------------------------------------------------
    def run(self):
        data_frame = self._step_1_load_the_database()
        years_range = self._step_2_get_years_range(data_frame)
        terms_by_year = self._step_3_compute_term_occurrences_by_year(data_frame)
        terms_by_year = self._step_4_check_years(terms_by_year, years_range)
        mapping = self._step_5_get_terms_mapping(data_frame)
        terms_by_year = self._step_6_filter_terms(terms_by_year)
        terms_by_year = self._step_7_append_counters_to_axis(terms_by_year, mapping)
        terms_by_year = self._step_8_sort_index(terms_by_year)
        terms_by_year = self._step_9_remove_counter_from_axis(terms_by_year)
        return terms_by_year


#
