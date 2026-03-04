"""
Terms to Cluster Mapping
===============================================================================


Smoke tests:
    >>> from tm2p import Field, AssociationIndex, ItemOrderBy, RecordOrderBy
    >>> from tm2p.synthes.netw.co_occur import DocumentsByClusterMapping
    >>> documents_by_cluster = (
    ...     DocumentsByClusterMapping()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # NETWORK:
    ...     .using_association_index(AssociationIndex.NONE)
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_ordered_by(RecordOrderBy.YEAR_NEWEST)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> print(len(documents_by_cluster))
    3
    >>> print(documents_by_cluster[0][0])



"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.rec import RecordViewer
from tm2p.synthes.netw.co_occur.clusters_to_items_mapping import ClustersToItemsMapping


class DocumentsByClusterMapping(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        c2t_mapping = (
            ClustersToItemsMapping()
            .update(**self.params.__dict__)
            .using_item_counters(True)
            .using_node_n_labels(self.params.top_n or 1000)
            .run()
        )

        mapping = {}
        field = self.params.source_field

        for key, values in c2t_mapping.items():

            params = {field: values}

            records_match = self.params.records_match
            if records_match is not None:
                records_match = {**records_match, **params}
            else:
                records_match = params

            mapping[key] = (
                RecordViewer()
                .update(**self.params.__dict__)
                .where_records_match(records_match)
                .run()
            )

        return mapping


#
