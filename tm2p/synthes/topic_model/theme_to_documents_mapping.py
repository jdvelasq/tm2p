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
    >>> from tm2p import ItemOrderBy, Field
    >>> from tm2p.synthes.topic_model import ThemeToDocumentsMapping
    >>> mapping = (
    ...     ThemeToDocumentsMapping()
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
    >>> import pprint
    >>> pprint.pprint(mapping)  # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    {0: ['Allen, 2022, J INT MONEY FINANC, V124',
         'Anagnostopoulos, 2018, J ECON BUS, V100, P7',
         'Barberis, 2016, ECON WIND, P69',
         'Bernards, 2019, REV INT POLIT ECON, V26, P815',
         'C., 2022, J INNOV KNOWL, V7',
         'Chen, 2016, CHINA ECON J, V9, P225',
         'Cheng, 2020, PAC BASIN FINANC J, V63',
         'Cheng, 2023, INT REV FINANC ANAL, V87',
    ...
"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.topic_model.documents_by_theme_dataframe import (
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
