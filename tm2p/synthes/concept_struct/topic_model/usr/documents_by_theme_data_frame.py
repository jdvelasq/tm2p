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
    >>> from tm2p.packages.topic_modeling.user import DocumentsByThemeDataFrame
    >>> df =(
    ...     DocumentsByThemeDataFrame()
    ...     #
    ...     # FIELD:
    ...     .with_field("raw_descriptors")
    ...     .having_items_in_top(50)
    ...     .having_items_ordered_by("OCC")
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # DECOMPOSITION:
    ...     .using_decomposition_algorithm(lda)
    ...     .using_top_terms_by_theme(5)
    ...     #
    ...     # TFIDF:
    ...     .using_binary_item_frequencies(False)
    ...     .using_row_normalization(None)
    ...     .using_idf_reweighting(False)
    ...     .using_idf_weights_smoothing(False)
    ...     .using_sublinear_tf_scaling(False)
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
    >>> df.head() # doctest: +SKIP
    cluster                                                    0  ...         9
    article                                                       ...
    Alt R., 2018, ELECTRON MARK, V28, P235              0.033338  ...  0.699979
    Anagnostopoulos I., 2018, J ECON BUS, V100, P7      0.947050  ...  0.005883
    Anshari M., 2019, ENERGY PROCEDIA, V156, P234       0.016672  ...  0.016670
    Arner D.W., 2017, NORTHWEST J INTL LAW BUS, V37...  0.006668  ...  0.006668
    Belanche D., 2019, IND MANAGE DATA SYS, V119, P...  0.899982  ...  0.011113
    <BLANKLINE>
    [5 rows x 10 columns]



"""

import pandas as pd  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.discov.tfidf._intern.matrix import Matrix as TfIdfDataFrame


class DocumentsByThemeDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        tf_matrix = TfIdfDataFrame().update(**self.params.__dict__).run()

        self.params.decomposition_algorithm.fit(tf_matrix)

        frame = pd.DataFrame(
            self.params.decomposition_algorithm.transform(tf_matrix),
            index=tf_matrix.index,
            columns=range(self.params.decomposition_algorithm.n_components),
        )
        frame.columns.name = "cluster"
        frame.index.name = "article"

        return frame
