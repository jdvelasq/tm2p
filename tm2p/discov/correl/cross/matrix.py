"""
Matrix
===============================================================================

Smoke tests:
    >>> from tm2p import ItemOrderBy, Field, Correlation
    >>> from tm2p.discov.correl.cross import Matrix
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
    ...     # CROSS WITH:
    ...     .with_cross_field(Field.CTRY_ISO3)
    ...     #
    ...     # CORRELATION:
    ...     .with_correlation_method(Correlation.PEARSON)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).round(3)
                                       fintech 117:25478  ...  financial services 007:01673
    fintech 117:25478                              1.000  ...                         0.125
    financial inclusion 017:03823                  0.255  ...                         0.249
    financial technology 014:02508                 0.000  ...                         0.212
    green finance 011:02844                        0.145  ...                         0.104
    blockchain 011:02023                           0.014  ...                         0.545
    banking 010:02599                              0.000  ...                         0.477
    china 009:01947                                0.114  ...                         0.022
    innovation 009:01703                           0.000  ...                         0.164
    artificial intelligence 008:01915              0.014  ...                         0.279
    financial services 007:01673                   0.125  ...                         1.000
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
    ...     # CROSS WITH:
    ...     .with_cross_field(Field.CTRY_ISO3)
    ...     #
    ...     # CORRELATION:
    ...     .with_correlation_method(Correlation.COSINE)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).round(3)
                                       fintech 117:25478  ...  financial services 007:01673
    fintech 117:25478                                1.0  ...                           0.0
    financial inclusion 017:03823                    1.0  ...                           0.0
    financial technology 014:02508                   1.0  ...                           0.0
    green finance 011:02844                          1.0  ...                           0.0
    blockchain 011:02023                             1.0  ...                           0.0
    banking 010:02599                                0.0  ...                           0.0
    china 009:01947                                  1.0  ...                           0.0
    innovation 009:01703                             1.0  ...                           0.0
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
    ...     # CROSS WITH:
    ...     .with_cross_field(Field.CTRY_ISO3)
    ...     #
    ...     # CORRELATION:
    ...     .with_correlation_method(Correlation.MAXPROPORTIONAL)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).round(3)
                                       fintech 117:25478  ...  financial services 007:01673
    fintech 117:25478                              1.000  ...                         0.159
    financial inclusion 017:03823                  0.455  ...                         0.250
    financial technology 014:02508                 0.455  ...                         0.227
    green finance 011:02844                        0.205  ...                         0.222
    blockchain 011:02023                           0.273  ...                         0.462
    banking 010:02599                              0.227  ...                         0.455
    china 009:01947                                0.136  ...                         0.143
    innovation 009:01703                           0.136  ...                         0.286
    artificial intelligence 008:01915              0.273  ...                         0.308
    financial services 007:01673                   0.159  ...                         1.000
    <BLANKLINE>
    [10 rows x 10 columns]


"""

from tm2p import ItemOrderBy
from tm2p._intern import ParamsMixin
from tm2p.discov.occur_matrix import Matrix as OCCMatrix

from .._intern import comput_correl_matrix


class Matrix(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        data_matrix = (
            OCCMatrix()
            .update(**self.params.__dict__)
            #
            .with_column_field(self.params.source_field)
            .having_column_items_in_top(self.params.top_n)
            .having_column_items_ordered_by(ItemOrderBy.OCC)
            .having_column_item_occurrences_between(
                self.params.item_occurrences_range[0],
                self.params.item_occurrences_range[1],
            )
            .having_column_item_citations_between(
                self.params.item_citations_range[0],
                self.params.item_citations_range[1],
            )
            .having_column_items_in(self.params.items_in)
            #
            .with_index_field(self.params.cross_field)
            .having_index_items_ordered_by(ItemOrderBy.OCC)
            .having_index_item_occurrences_between(None, None)
            .having_index_item_citations_between(None, None)
            .having_index_items_in(None)
            #
            .run()
        )

        data_matrix = data_matrix.map(lambda x: 1.0 if x > 0 else 0.0)
        data_matrix = data_matrix.loc[~(data_matrix == 0).all(axis=1), :]
        data_matrix = data_matrix.loc[:, ~(data_matrix == 0).all(axis=0)]

        matrix = comput_correl_matrix(
            params=self.params,
            tfidf=data_matrix,
        )

        return matrix
