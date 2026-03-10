"""
Components by Term Frame
===============================================================================

Smoke tests:
    >>> from sklearn.decomposition import LatentDirichletAllocation
    >>> lda = LatentDirichletAllocation(
    ...     n_components=10,
    ...     learning_decay=0.7,
    ...     learning_offset=50.0,
    ...     max_iter=10,
    ...     batch_size=128,
    ...     evaluate_every=-1,
    ...     perp_tol=0.1,
    ...     mean_change_tol=0.001,
    ...     max_doc_update_iter=100,
    ...     random_state=0,
    ... )
    >>> from tm2p import ItemOrderBy, Field
    >>> from tm2p.synthes.topic_model import ComponentsByItemDataFrame
    >>> df = (
    ...     ComponentsByItemDataFrame()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.CONCEPT_NORM)
    ...     .having_items_in_top(50)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # DECOMPOSITION:
    ...     .using_decomposition_algorithm(lda)
    ...     .using_top_items_by_theme(5)
    ...     #
    ...     # TFIDF:
    ...     .using_binary_item_frequencies(False)
    ...     .using_tfidf_norm(None)
    ...     .using_tfidf_smooth_idf(False)
    ...     .using_tfidf_sublinear_tf(False)
    ...     .using_tfidf_use_idf(False)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df
    term       fintech 155:33245  ...  fintech innovation 009:02472
    component                     ...
    0                  26.451087  ...                      1.439931
    1                  21.426701  ...                      0.100003
    2                   6.679625  ...                      0.100000
    3                  13.678684  ...                      0.100003
    4                  13.682582  ...                      0.100000
    5                  11.191485  ...                      0.100008
    6                  12.022431  ...                      0.100007
    7                  12.722319  ...                      0.100000
    8                  16.057747  ...                      2.453718
    9                  22.087339  ...                      5.406330
    <BLANKLINE>
    [10 rows x 50 columns]


"""

import pandas as pd  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.discov.tfidf.matrix import Matrix as TfIdf


class ComponentsByItemDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        tf_matrix = TfIdf().update(**self.params.__dict__).run()

        self.params.decomposition_algorithm.fit(tf_matrix)  # type: ignore

        frame = pd.DataFrame(
            self.params.decomposition_algorithm.components_,  # type: ignore
            index=range(self.params.decomposition_algorithm.n_components),  # type: ignore
            columns=tf_matrix.columns,
        )

        frame.columns.name = "term"
        frame.index.name = "component"

        return frame
