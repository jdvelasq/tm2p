"""
Sankey Plot
===============================================================================


Smoke tests:
    >>> from tm2p.packages.occurrence_matrix import SankeyPlot
    >>> fig = (
    ...     SankeyPlot()
    ...     #
    ...     # COLUMNS:
    ...     .with_column_field(CorpusField.AUTHKW_TOK)
    ...     .having_column_items_in_top(10)
    ...     .having_column_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_column_item_occurrences_between(None, None)
    ...     .having_column_item_citations_between(None, None)
    ...     .having_column_items_in(None)
    ...     #
    ...     # ROWS:
    ...     .with_index_field(CorpusField.AUTH_NORM)
    ...     .having_index_items_in_top(15)
    ...     .having_index_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_index_item_occurrences_between(0, None)
    ...     .having_index_item_citations_between(None, None)
    ...     .having_index_items_in(None)
    ...     #
    ...     # PLOT:
    ...     .using_color(None)
    ...     .using_textfont_size(8)
    ...     .using_title_text("Sankey Plot")
    ...     #
    ...     # COUNTERS:
    ...     .using_item_counters(True)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> type(fig).__name__
    'Figure'
    >>> fig.write_html("docsrc/_generated/px.packages.occur_matrix.sankey_plot.html")

.. raw:: html

    <iframe src="../_generated/px.packages.occurrence_matrix/sankey_plot.html"
    height="800px" width="100%" frameBorder="0"></iframe>

"""

import plotly.graph_objects as go  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.discov.occur_matrix.matrix import Matrix


class SankeyPlot(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def _step_01_build_matrices(self):

        matrices = []
        fields = [self.params.source_field.value, self.params.index_field.value]

        for row_field, col_field in zip(fields[:-1], fields[1:]):

            matrix = (
                Matrix()
                .update(**self.params.__dict__)
                #
                # COLUMNS:
                .with_source_field(
                    col_field,
                )
                .having_items_ordered_by(
                    "OCC",
                )
                .having_items_in_top(
                    self.params.top_n,
                )
                .having_item_occurrences_between(
                    self.params.item_occurrences_range[0],
                    self.params.item_occurrences_range[1],
                )
                .having_item_citations_between(
                    self.params.item_citations_range[0],
                    self.params.item_citations_range[1],
                )
                .having_items_in(
                    self.params.items_in,
                )
                #
                # ROWS:
                .with_other_field(
                    row_field,
                )
                .having_index_items_ordered_by(
                    "OCC",
                )
                .having_index_items_in_top(
                    self.params.top_n,
                )
                .having_index_item_occurrences_between(
                    self.params.item_occurrences_range[0],
                    self.params.item_occurrences_range[1],
                )
                .having_index_item_citations_between(
                    self.params.item_citations_range[0],
                    self.params.item_citations_range[1],
                )
                .having_index_items_in(
                    self.params.items_in,
                )
                .run()
            )

            matrices.append(matrix)

        return matrices

    # -------------------------------------------------------------------------
    def _step_02_build_node_names(self, matrices):

        node_names = []
        for i_matrix, matrix in enumerate(matrices):
            if i_matrix == 0:
                node_names.extend(matrix.index.to_list())
            node_names.extend(matrix.columns.to_list())

        return node_names

    # -------------------------------------------------------------------------

    def _step_03_build_node_indexes(self, node_names):
        """Builds the node indices"""
        return {key: pos for pos, key in enumerate(node_names)}

    # -------------------------------------------------------------------------
    def _step_04_build_links(self, matrices, node_indexes):
        """Links are a node dictionary with source, target and value"""

        source = []
        target = []
        value = []

        for coc_matrix in matrices:
            matrix = coc_matrix.copy()

            for row in matrix.index:
                for col in matrix.columns:
                    source.append(node_indexes[row])
                    target.append(node_indexes[col])
                    value.append(matrix.loc[row, col])
        return {"source": source, "target": target, "value": value}

    # -------------------------------------------------------------------------
    def _step_05_build_diagram(self, node_names, links):
        fig = go.Figure(
            data=[
                go.Sankey(
                    node={
                        "label": node_names,
                        "color": self.params.color,
                    },
                    link=links,
                )
            ]
        )
        fig.update_layout(
            title_text=self.params.title_text,
            font_size=self.params.textfont_size,
        )
        return fig

    # -------------------------------------------------------------------------
    def run(self):

        matrices = self._step_01_build_matrices()
        node_names = self._step_02_build_node_names(matrices)
        node_indexes = self._step_03_build_node_indexes(node_names)
        links = self._step_04_build_links(matrices, node_indexes)
        fig = self._step_05_build_diagram(node_names, links)

        return fig
