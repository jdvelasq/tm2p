"""
ItemsByClusterDataFrame
===============================================================================

Smoke tests:
    >>> from tm2p import CoCitationUnit
    >>> from tm2p.synthes.netw.co_cit import ItemsByClusterDataFrame
    >>> df = (
    ...     ItemsByClusterDataFrame()
    ...     #
    ...     # ANALYSIS UNIT:
    ...     .with_co_citation_unit(CoCitationUnit.CITED_AUTH)
    ...     .having_items_in_top(30)
    ...     .having_citation_threshold(0)
    ...     .having_items_in(None)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).head()
    >>> print(df)  # doctest: +NORMALIZE_WHITESPACE
                    0            1  ...             4           5
    0       Ashta 1:6   Ahlers 1:5  ...  Croutzet 1:3   Autor 1:2
    1       Davis 1:5  Allison 1:4  ...   Vergara 1:3  Billio 1:2
    2    Bollaert 1:3    Adner 1:3  ...
    3  Zavolokina 1:3  Agrawal 1:3  ...
    4    Acemoglu 1:2    Allen 1:3  ...
    <BLANKLINE>
    [5 rows x 6 columns]


"""

from tm2p._intern import ParamsMixin, remove_counters
from tm2p._intern.nx import cluster_nx_graph, extract_communities
from tm2p.synthes.netw.co_cit._intern.create_nx_graph import create_nx_graph


class ItemsByClusterDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        use_counters = self.params.counters
        self.params.counters = True
        nx_graph = create_nx_graph(self.params)
        nx_graph = cluster_nx_graph(self.params, nx_graph)
        communities = extract_communities(nx_graph)
        if use_counters is False:
            self.params.counters = False
            for col in communities.columns:
                communities[col] = communities[col].apply(remove_counters)

        return communities
