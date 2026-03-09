"""
Metrics
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.synthes.collabor import Metrics
    >>> df = (
    ...     Metrics()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.CTRY_ISO3)
    ...     .having_items_in_top(20)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_items_in(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()  # doctest: +NORMALIZE_WHITESPACE
               OCC   GCS  LCS  SP  MP  MP_RATIO
    CTRY_ISO3
    CHN         45  9715    0  22  23      0.51
    GBR         33  6802    0  12  21      0.64
    USA         31  9562    0  13  18      0.58
    AUS         14  3468    0   4  10      0.71
    DEU         13  5295    0   5   8      0.62

"""

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p.anal.metrics.metrics import Metrics as PerformanceMetrics
from tm2p.enum.column import GCS, LCS, MP, MP_RATIO, OCC, RID, SP


class Metrics(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def _step_1_load_the_database(self):
        return load_filtered_main_csv_zip(params=self.params)

    # -------------------------------------------------------------------------
    def _step_2_compute_collaboration_metrics(self, df):

        field = self.params.source_field.value

        #
        # Add a column to represent the number of occurrences of a document
        df = df.copy()
        df = df.dropna(subset=[field])
        df[OCC] = 1

        #
        # Add columns to represent single and multiple publications for a document
        df[SP] = df[field].map(
            lambda x: 1 if isinstance(x, str) and len(x.split(";")) == 1 else 0
        )
        df[MP] = df[field].map(
            lambda x: 1 if isinstance(x, str) and len(x.split(";")) > 1 else 0
        )

        #
        # Split multi-topic documents into individual documents with one topic each
        exploded = df[
            [
                field,
                OCC,
                GCS,
                LCS,
                SP,
                MP,
                RID,
            ]
        ].copy()
        exploded[field] = exploded[field].str.split(";")
        exploded = exploded.explode(field)
        exploded[field] = exploded[field].str.strip()

        #
        # Compute collaboration indicators for each topic
        metrics = exploded.groupby(field, as_index=False).agg(
            {
                OCC: "sum",
                GCS: "sum",
                LCS: "sum",
                SP: "sum",
                MP: "sum",
            }
        )

        #
        # Compute the multiple publication ratio for each topic
        metrics[MP_RATIO] = metrics[MP] / metrics[OCC]
        metrics[MP_RATIO] = metrics[MP_RATIO].round(2)

        #
        # Sort the topics by number of occurrences, global citations, and local
        # citations
        metrics = metrics.sort_values(
            by=[OCC, GCS, LCS],
            ascending=[False, False, False],
        )

        #
        # Set the index to the criterion column
        metrics = metrics.set_index(field)

        return metrics

    # -------------------------------------------------------------------------
    def _step_3_filter_terms(self, data_frame):
        terms_in = PerformanceMetrics()
        terms_in = terms_in.update(**self.params.__dict__)
        terms_in = terms_in.run()
        terms_in = terms_in.index
        data_frame = data_frame[data_frame.index.isin(terms_in)]
        return data_frame

    # -------------------------------------------------------------------------
    def run(self):
        database = self._step_1_load_the_database()
        data_frame = self._step_2_compute_collaboration_metrics(database)
        data_frame = self._step_3_filter_terms(data_frame)
        return data_frame
