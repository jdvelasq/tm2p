"""
ItemsByCluster
===============================================================================

Smoke tests:
    >>> from tm2p import CoCitationUnit
    >>> from tm2p.synthes.netw.co_cit import ItemsByCluster
    >>> df = (
    ...     ItemsByCluster()
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


"""

from tm2p._intern import ParamsMixin, remove_counters
from tm2p._intern.nx import cluster_nx_graph, extract_communities
from tm2p.synthes.netw.co_cit._intern.create_nx_graph import create_nx_graph


class ItemsByCluster(
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
