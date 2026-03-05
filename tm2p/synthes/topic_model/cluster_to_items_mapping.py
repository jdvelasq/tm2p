"""
Cluster to Terms Mapping
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
    >>> from tm2p.synthes.topic_model import ClusterToItemsMapping
    >>> mapping = (
    ...     ClusterToItemsMapping()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.CONCEPT_NORM)
    ...     .having_items_in_top(20)
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
    >>> import pprint
    >>> pprint.pprint(mapping)  # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    {0: ['the development 026:05689',
         'fintech 155:33245',
         'financial technology 051:09258',
         'banks 029:06252',
         'china 033:06419',
         'fintech development 015:03625',
         'financial services 030:06887',
    ...

"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.topic_model.components_by_item_dataframe import (
    ComponentsByItemDataFrame,
)


class ClusterToItemsMapping(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        theme_term_matrix = (
            ComponentsByItemDataFrame().update(**self.params.__dict__).run()
        )

        mapping = {}
        for i_row in range(theme_term_matrix.shape[0]):
            sorting_indices = theme_term_matrix.iloc[i_row, :].sort_values(
                ascending=False
            )
            theme_term_matrix = theme_term_matrix[sorting_indices.index]
            if self.params.top_n is not None:
                mapping[i_row] = list(theme_term_matrix.columns[: self.params.top_n])
            else:
                mapping[i_row] = list(theme_term_matrix.columns)

        return mapping
