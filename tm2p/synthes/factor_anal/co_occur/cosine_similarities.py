"""
CosineSimilarities
===============================================================================

Smoke test:
    >>> from sklearn.decomposition import PCA
    >>> pca = PCA(
    ...     n_components=5,
    ...     whiten=False,
    ...     svd_solver="auto",
    ...     tol=0.0,
    ...     iterated_power="auto",
    ...     n_oversamples=10,
    ...     power_iteration_normalizer="auto",
    ...     random_state=0,
    ... )
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.synthes.factor_anal.co_occur import CosineSimilarities
    >>> (
    ...     CosineSimilarities()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.CONCEPT_NORM)
    ...     .having_items_in_top(50)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # DECOMPOSITION:
    ...     .using_decomposition_estimator(pca)
    ...     #
    ...     # ASSOCIATION INDEX:
    ...     .using_association_index(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).head()




"""

import pandas as pd  # type: ignore
from sklearn.metrics.pairwise import (
    cosine_similarity as sklearn_cosine_similarity,  # type: ignore
)

from tm2p._intern import ParamsMixin
from tm2p.synthes.factor_anal.co_occur.items_by_dimension_data_frame import (
    terms_by_dimension_frame,
)


class CosineSimilarities(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        pass


def cosine_similarities(
    #
    # PARAMS:
    field,
    association_index=None,
    #
    # TERM PARAMS:
    top_n=None,
    occ_range=(None, None),
    gc_range=(None, None),
    custom_terms=None,
    #
    # DECOMPOSITION:
    decomposition_estimator=None,
    #
    # DATABASE PARAMS:
    root_dir="./",
    database="main",
    year_filter=(None, None),
    cited_by_filter=(None, None),
    **filters,
):
    """:meta private:"""

    embedding = terms_by_dimension_frame(
        #
        # FUNCTION PARAMS:
        field=field,
        association_index=association_index,
        #
        # TERM PARAMS:
        top_n=top_n,
        occ_range=occ_range,
        gc_range=gc_range,
        custom_terms=custom_terms,
        #
        # DECOMPOSITION:
        decomposition_estimator=decomposition_estimator,
        #
        # DATABASE PARAMS:
        root_dir=root_dir,
        database=database,
        year_filter=year_filter,
        cited_by_filter=cited_by_filter,
        **filters,
    )

    similarity = sklearn_cosine_similarity(embedding)

    term_similarities = []
    for i in range(similarity.shape[0]):
        values_to_sort = []
        for j in range(similarity.shape[1]):
            if i != j and similarity[i, j] > 0:
                values_to_sort.append(
                    (
                        embedding.index[j],
                        similarity[i, j],
                    )
                )
        sorted_values = sorted(values_to_sort, key=lambda x: x[1], reverse=True)
        sorted_values = [f"{x[0]} ({x[1]:>0.3f})" for x in sorted_values]
        sorted_values = "; ".join(sorted_values)
        term_similarities.append(sorted_values)

    term_similarities = pd.DataFrame(
        {"cosine_similariries": term_similarities},
        index=embedding.index,
    )

    return term_similarities

    return term_similarities
