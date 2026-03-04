"""
Theme to Documents Mapping
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
    >>> from tm2p.packages.topic_modeling.user import ThemeToDocumentsMapping
    >>> mapping = (
    ...     ThemeToDocumentsMapping()
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
    >>> import pprint
    >>> pprint.pprint(mapping)  # doctest: +SKIP
    {0: ['Anagnostopoulos I., 2018, J ECON BUS, V100, P7',
         'Belanche D., 2019, IND MANAGE DATA SYS, V119, P1411',
         'Dorfleitner G., 2017, FINTECH IN GER, P1',
         'Du W.D., 2019, J STRATEGIC INFORM SYST, V28, P50',
         'Jagtiani J., 2018, J ECON BUS, V100, P43',
         'Lee I., 2018, BUS HORIZ, V61, P35',
         'Leong C., 2017, INT J INF MANAGE, V37, P92',
         'Magnuson W., 2018, VANDERBILT LAW REV, V71, P1167'],
     1: ['Brummer C., 2019, GEORGET LAW J, V107, P235',
         'Das S.R., 2019, FINANC MANAGE, V48, P981',
         'Gozman D., 2018, J MANAGE INF SYST, V35, P145',
    ...

"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.topic_model.documents_by_theme_data_frame import (
    DocumentsByThemeDataFrame,
)


class ThemeToDocumentsMapping(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        frame = DocumentsByThemeDataFrame().update(**self.params.__dict__).run()

        assigned_topics_to_documents = frame.idxmax(axis=1)

        mapping = {}
        for article, theme in zip(
            assigned_topics_to_documents.index, assigned_topics_to_documents
        ):
            if theme not in mapping:
                mapping[theme] = []
            mapping[theme].append(article)

        return mapping
