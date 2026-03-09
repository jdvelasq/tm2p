"""
Sankey Plot
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.discov.sankey/sankey_plot.html"
    height="800px" width="100%" frameBorder="0"></iframe>


Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.discov.sankey import SankeyPlot
    >>> fig = (
    ...     SankeyPlot()
    ...     #
    ...     # COLUMNS:
    ...     .with_source_fields(
    ...         [
    ...             Field.CTRY_ISO3,
    ...             Field.AUTH_NORM,
    ...             Field.CONCEPT_NORM,
    ...         ]
    ...     )
    ...     .having_sankey_items_in_top_n((20, 20, 10))
    ...     #
    ...     # PLOT:
    ...     .using_color("#7793a5")
    ...     .using_textfont_size(8)
    ...     .using_title_text("Sankey Plot")
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/regtech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> type(fig).__name__
    'Figure'
    >>> fig.write_html("docsrc/_generated/px.discov.sankey.sankey_plot.html")


"""

import plotly.graph_objects as go  # type: ignore

from tm2p import ItemOrderBy
from tm2p._intern import ParamsMixin
from tm2p.discov.cross_occur_matrix.matrix import Matrix


class SankeyPlot(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def _step_01_build_matrices(self):

        matrices = []
        fields = self.params.source_fields
        top_n = self.params.sankey_top_n

        for (
            idx,
            col_field,
            idx_top_n,
            col_top_n,
        ) in zip(
            fields[:-1],
            fields[1:],
            top_n[:-1],
            top_n[1:],
        ):

            matrix = (
                Matrix()
                .update(**self.params.__dict__)
                #
                # COLUMNS:
                .with_column_field(col_field)
                .having_column_items_ordered_by(ItemOrderBy.OCC)
                .having_column_items_in_top(col_top_n)
                #
                # ROWS:
                .with_index_field(idx)
                .having_index_items_ordered_by(ItemOrderBy.OCC)
                .having_index_items_in_top(
                    idx_top_n,
                )
                #
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
        return {key: pos for pos, key in enumerate(node_names)}

    # -------------------------------------------------------------------------
    def _step_04_build_links(self, matrices, node_indexes):

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
