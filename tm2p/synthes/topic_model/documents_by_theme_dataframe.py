"""
Documents by Theme Frame
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
    >>> from tm2p.synthes.topic_model import DocumentsByThemeDataFrame
    >>> df =(
    ...     DocumentsByThemeDataFrame()
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
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()
    cluster                                                    0  ...         9
    article                                                       ...
    Agarwal, 2020, ASIAPACIFIC J FINANC STUD, V49, ...  0.014288  ...  0.014287
    Ajouz, 2023, CUAD ECON, V46, P189                   0.016671  ...  0.016675
    Al-Sartawi, 2024, J FINANC REPORT ACCOUNT           0.014290  ...  0.014288
    Alam, 2019, FINTECH ISLAM FINANC DIGIT DEV DISR...  0.020003  ...  0.020002
    Aldboush, 2023, INT J FINANC STUD, V11              0.020002  ...  0.020002
    <BLANKLINE>
    [5 rows x 10 columns]



"""

import pandas as pd  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.discov.tfidf.matrix import Matrix as TfIdf


class DocumentsByThemeDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        tf_matrix = TfIdf().update(**self.params.__dict__).run()

        self.params.decomposition_algorithm.fit(tf_matrix)

        frame = pd.DataFrame(
            self.params.decomposition_algorithm.transform(tf_matrix),
            index=tf_matrix.index,
            columns=range(self.params.decomposition_algorithm.n_components),
        )
        frame.columns.name = "cluster"
        frame.index.name = "article"

        return frame
