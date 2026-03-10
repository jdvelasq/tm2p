"""
ConceptGridPlot
===============================================================================


## >>> from tm2p.synthes.netw.co_occur import concept_grid_plot
## >>> chart = concept_grid_plot(
## ...     #
## ...     # FIELD:
## ...     .with_field("author_keywords")
## ...     .having_items_in_top(30)
## ...     .having_items_ordered_by("OCC")
## ...     .having_item_occurrences_between(None, None)
## ...     .having_item_citations_between(None, None)
## ...     .having_items_in(None)
## ...     #
## ...     # COUNTERS:
## ...     .using_counters(True)
## ...     #
## ...     # NETWORK:
## ...     .using_clustering_algorithm_or_dict("louvain")
## ...     .using_association_index("association")
## ...     #
## ...     # DATABASE:
## ...     .where_root_directory("tests/scopus/")
## ...     .where_database("main")
## ...     .where_record_years_range(None, None)
## ...     .where_record_citations_range(None, None)
## ...     .where_records_match(None)
## ...     #
## ...     .run()
## ... )
## >>> chart.render("sphinx/images/co_occurrence_network/concept_grid_plot", format="png")


# .. image:: /images/co_occurrence_network/concept_grid_plot.png
#     :width: 900px
#     :align: center

"""

from tm2p._intern import ParamsMixin

# from tm2p._intern.nx import cluster_nx_graph, concept_grid_plot
# from tm2p.synthes.netw.co_occur._intern.create_nx_graph import create_nx_graph


class ConceptGridPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        # nx_graph = create_nx_graph(self.params)
        # nx_graph = cluster_nx_graph(self.params, nx_graph)
        # return concept_grid_plot(self.params, nx_graph)
