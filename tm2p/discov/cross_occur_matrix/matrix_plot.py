"""
MatrixPlot
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.discov.occur_matrix.matrix_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>


Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.discov.cross_occur_matrix import MatrixPlot
    >>> fig = (
    ...     MatrixPlot()
    ...     #
    ...     # COLUMNS:
    ...     .with_column_field(Field.AUTHKW_TOK)
    ...     .having_column_items_in_top(10)
    ...     .having_column_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_column_item_occurrences_between(None, None)
    ...     .having_column_item_citations_between(None, None)
    ...     .having_column_items_in(None)
    ...     #
    ...     # ROWS:
    ...     .with_index_field(Field.AUTH_NORM)
    ...     .having_index_items_in_top(15)
    ...     .having_index_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_index_item_occurrences_between(0, None)
    ...     .having_index_item_citations_between(None, None)
    ...     .having_index_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # NETWORK:
    ...     .using_spring_layout_k(None)
    ...     .using_spring_layout_iterations(30)
    ...     .using_spring_layout_seed(0)
    ...     #
    ...     .using_node_n_labels(4)
    ...     .using_node_size_range(30, 70)
    ...     .using_node_colors(("#7793a5", "#465c6b"))
    ...     .using_textfont_size_range(10, 20)
    ...     .using_textfont_opacity_range(0.35, 1.00)
    ...     #
    ...     .using_edge_colors(("#b8c6d0",))
    ...     .using_edge_width_range(0.8, 4.0)
    ...     #
    ...     .using_xaxes_range(None, None)
    ...     .using_yaxes_range(None, None)
    ...     .using_axes_visible(False)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> type(fig).__name__
    'Figure'
    >>> fig.write_html("docsrc/_generated/px.discov.occur_matrix.matrix_plot.html")

"""

import networkx as nx  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    assign_constant_to_edge_colors,
    assign_edge_widths_based_on_weight,
    assign_node_sizes_based_on_occurrences,
    assign_text_positions_based_on_quadrants,
    assign_textfont_opacity_based_on_occurrences,
    assign_textfont_sizes_based_on_occurrences,
    compute_spring_layout_positions,
    plot_nx_graph,
)
from tm2p.discov.cross_occur_matrix.matrix import Matrix


def create_co_occurrence_matrix(params):
    return Matrix().update(**params.__dict__).run()


def create_a_empty_networkx_graph():
    return nx.Graph()


def add_nodes_from_matrix(params, nx_graph, matrix):

    matrix = matrix.copy()

    idx_node_color = params.node_colors[0]
    col_node_color = params.node_colors[1]

    idx_nodes = matrix.index.tolist()
    idx_labeled = idx_nodes[: params.node_n_labels]
    nx_graph.add_nodes_from(idx_nodes, group=0, node_color=idx_node_color)

    col_nodes = matrix.columns.tolist()
    col_labeled = col_nodes[: params.node_n_labels]
    nx_graph.add_nodes_from(col_nodes, group=1, node_color=col_node_color)

    for node in nx_graph.nodes():
        nx_graph.nodes[node]["text"] = node
        if node in idx_labeled or node in col_labeled:
            nx_graph.nodes[node]["labeled"] = True
        else:
            nx_graph.nodes[node]["labeled"] = False

    return nx_graph


class MatrixPlot(
    ParamsMixin,
):
    """:meta private:"""

    def _step_04_add_weighted_edges_from_matrix(self, nx_graph, matrix):

        matrix = matrix.copy()

        if matrix.index.tolist() == matrix.columns.tolist():
            #
            # This is a symmetric matrix:
            #
            for i_row, row in enumerate(matrix.index.tolist()):
                for i_col, col in enumerate(matrix.columns.tolist()):
                    #
                    if matrix.iloc[i_row, i_col] > 0:
                        #
                        # Unicamente toma valores por encima de la diagonal principal
                        if i_col <= i_row:
                            continue

                        weight = matrix.loc[row, col]
                        nx_graph.add_weighted_edges_from(
                            ebunch_to_add=[(row, col, weight)],
                            dash="solid",
                        )

            return nx_graph

        #
        # This is a non-symmetric matrix:
        #
        for i_row, row in enumerate(matrix.index.tolist()):
            for i_col, col in enumerate(matrix.columns.tolist()):
                #
                if matrix.loc[row, col] > 0:
                    #
                    weight = matrix.loc[row, col]
                    nx_graph.add_weighted_edges_from(
                        ebunch_to_add=[(row, col, weight)],
                        dash="solid",
                    )

        return nx_graph

    def _step_05_compute_spring_layout_positions(self, nx_graph):
        return compute_spring_layout_positions(
            self.params,
            nx_graph,
        )

    def _step_06_assign_node_sizes_based_on_occurrences(self, nx_graph):
        return assign_node_sizes_based_on_occurrences(
            self.params,
            nx_graph,
        )

    def _step_07_assign_textfont_sizes_based_on_occurrences(self, nx_graph):
        return assign_textfont_sizes_based_on_occurrences(
            self.params,
            nx_graph,
        )

    def _step_08_assign_text_opacity_based_on_occurrences(self, nx_graph):
        return assign_textfont_opacity_based_on_occurrences(self.params, nx_graph)

    def _step_09_assign_edge_colors_based_on_weight(self, nx_graph):
        return assign_constant_to_edge_colors(
            self.params,
            nx_graph,
        )

    def _step_10_assign_edge_widths_based_on_weight(self, nx_graph):
        return assign_edge_widths_based_on_weight(
            self.params,
            nx_graph,
        )

    def _step_11_assign_text_positions_based_on_quadrants(self, nx_graph):
        return assign_text_positions_based_on_quadrants(nx_graph)

    def run(self):

        matrix = create_co_occurrence_matrix(self.params)
        nx_graph = create_a_empty_networkx_graph()

        nx_graph = add_nodes_from_matrix(self.params, nx_graph, matrix)

        nx_graph = self._step_04_add_weighted_edges_from_matrix(nx_graph, matrix)
        nx_graph = self._step_05_compute_spring_layout_positions(nx_graph)
        nx_graph = self._step_06_assign_node_sizes_based_on_occurrences(nx_graph)
        nx_graph = self._step_07_assign_textfont_sizes_based_on_occurrences(nx_graph)
        nx_graph = self._step_08_assign_text_opacity_based_on_occurrences(nx_graph)
        nx_graph = self._step_09_assign_edge_colors_based_on_weight(nx_graph)
        nx_graph = self._step_10_assign_edge_widths_based_on_weight(nx_graph)
        nx_graph = self._step_11_assign_text_positions_based_on_quadrants(nx_graph)

        return plot_nx_graph(
            params=self.params,
            nx_graph=nx_graph,
        )


#
