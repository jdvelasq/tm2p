"""
Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.discov.associations._internals import DataFrame
    >>> (
    ...     DataFrame()
    ...     #
    ...     # COLUMNS:
    ...     .with_field(CorpusField.AUTH_KEY_RAW)
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
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    columns                       FINTECH 31:5168  ...  FINANCIAL_SERVICES 04:0667
    rows                                           ...
    FINTECH 31:5168                            31  ...                           3
    INNOVATION 07:0911                          5  ...                           2
    FINANCIAL_SERVICES 04:0667                  3  ...                           4
    FINANCIAL_INCLUSION 03:0590                 3  ...                           0
    FINANCIAL_TECHNOLOGY 03:0461                2  ...                           1
    CROWDFUNDING 03:0335                        2  ...                           0
    MARKETPLACE_LENDING 03:0317                 3  ...                           0
    BUSINESS_MODELS 02:0759                     2  ...                           1
    CYBER_SECURITY 02:0342                      2  ...                           0
    CASE_STUDY 02:0340                          2  ...                           0
    <BLANKLINE>
    [10 rows x 3 columns]

"""

from tm2p._intern import ParamsMixin
from tm2p.discov.co_occur_matrix._intern import Matrix


class DataFrame(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def _step_01_compute_co_occurence_matrix(self):
        return (
            Matrix()
            .update(**self.params.__dict__)
            .using_item_counters(True)
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
