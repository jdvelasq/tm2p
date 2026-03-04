"""
Data Frame
===============================================================================

Smoke tests:
    >>> from tm2p.packages.associations import DataFrame
    >>> (
    ...     DataFrame()
    ...     #
    ...     # COLUMNS:
    ...     .with_field("author_keywords_raw")
    ...     .having_items_in_top(None)
    ...     .having_items_ordered_by("OCC")
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(["FINTECH", "INNOVATION", "FINANCIAL_SERVICES"])
    ...     #
    ...     # ROWS:
    ...     .having_other_terms_in_top(10)
    ...     .having_other_terms_ordered_by("OCC")
    ...     .having_other_term_occurrences_between(None, None)
    ...     .having_other_term_citations_between(None, None)
    ...     .having_other_terms_in(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )


"""

from tm2p._intern import ParamsMixin
from tm2p.discov.co_occur_matrix import Matrix


class DataFrame(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def _step_01_compute_co_occurence_matrix(self):
        return (
            Matrix()
            .update(**self.params.__dict__)
            .using_counters(True)
            .with_other_field(self.params.source_field)
            .run()
        )

    # -------------------------------------------------------------------------
    def _step_02_remove_rows_with_only_zeros(self, matrix):
        return matrix.loc[matrix.index[matrix.sum(axis=1) > 0], :]

    # -------------------------------------------------------------------------
    def _step_03_remove_counters(self, matrix):
        if self.params.item_counters:
            return matrix
        matrix.columns = [col.split(" ")[0] for col in matrix.columns]
        matrix.index = [idx.split(" ")[0] for idx in matrix.index]
        return matrix

    # -------------------------------------------------------------------------
    def run(self):

        matrix = self._step_01_compute_co_occurence_matrix()
        matrix = self._step_02_remove_rows_with_only_zeros(matrix)
        matrix = self._step_03_remove_counters(matrix)

        return matrix
