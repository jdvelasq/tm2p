"""
Matrix
===============================================================================

Smoke Test:
    >>> from tm2p import ItemOrderBy, Field, Correlation
    >>> from tm2p.discov.correl.auto import Matrix
    >>> (
    ...     Matrix()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # CORRELATION:
    ...     .with_correlation_method(Correlation.PEARSON)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... ).round(3)
                                       fintech 117:25478  ...  financial services 007:01673
    fintech 117:25478                                1.0  ...                         0.000
    financial inclusion 017:03823                    0.0  ...                         0.013
    financial technology 014:02508                   0.0  ...                         0.031
    green finance 011:02844                          0.0  ...                         0.000
    blockchain 011:02023                             0.0  ...                         0.000
    banking 010:02599                                0.0  ...                         0.190
    china 009:01947                                  0.0  ...                         0.000
    innovation 009:01703                             0.0  ...                         0.206
    artificial intelligence 008:01915                0.0  ...                         0.000
    financial services 007:01673                     0.0  ...                         1.000
    <BLANKLINE>
    [10 rows x 10 columns]


    >>> (
    ...     Matrix()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # CORRELATION:
    ...     .with_correlation_method(Correlation.COSINE)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... ).round(3)
                                       fintech 117:25478  ...  financial services 007:01673
    fintech 117:25478                                1.0  ...                           0.0
    financial inclusion 017:03823                    0.0  ...                           0.0
    financial technology 014:02508                   0.0  ...                           0.0
    green finance 011:02844                          0.0  ...                           0.0
    blockchain 011:02023                             0.0  ...                           0.0
    banking 010:02599                                0.0  ...                           0.0
    china 009:01947                                  0.0  ...                           0.0
    innovation 009:01703                             0.0  ...                           0.0
    artificial intelligence 008:01915                0.0  ...                           0.0
    financial services 007:01673                     0.0  ...                           0.0
    <BLANKLINE>
    [10 rows x 10 columns]

    >>> (
    ...     Matrix()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # CORRELATION:
    ...     .with_correlation_method(Correlation.MAXPROPORTIONAL)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... ).round(3)
                                       fintech 117:25478  ...  financial services 007:01673
    fintech 117:25478                              1.000  ...                         0.034
    financial inclusion 017:03823                  0.120  ...                         0.059
    financial technology 014:02508                 0.060  ...                         0.071
    green finance 011:02844                        0.068  ...                         0.000
    blockchain 011:02023                           0.068  ...                         0.000
    banking 010:02599                              0.060  ...                         0.200
    china 009:01947                                0.060  ...                         0.000
    innovation 009:01703                           0.051  ...                         0.222
    artificial intelligence 008:01915              0.051  ...                         0.000
    financial services 007:01673                   0.034  ...                         1.000
    <BLANKLINE>
    [10 rows x 10 columns]

"""

from tm2p._intern import ParamsMixin

from ...tfidf.matrix import Matrix as TfIdf
from .._intern.comput_correl_matrix import comput_correl_matrix


class Matrix(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        tfidf_matrix = (
            TfIdf()
            .update(**self.params.__dict__)
            .using_binary_item_frequencies(True)
            .using_tfidf_norm(None)
            .using_tfidf_smooth_idf(False)
            .using_tfidf_sublinear_tf(False)
            .using_tfidf_use_idf(False)
            .run()
        )

        matrix = comput_correl_matrix(
            params=self.params,
            tfidf=tfidf_matrix,
        )

        return matrix
