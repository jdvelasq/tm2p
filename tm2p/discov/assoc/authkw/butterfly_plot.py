"""
ButterflyPlot
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.packages.associations import ButterflyPlot
    >>> plot = (
    ...     ButterflyPlot()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_RAW)
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by("OCC")
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(["FINTECH", "INNOVATION", "FINANCIAL_SERVICES"])
    ...     #
    ...     # ROWS:
    ...     .having_other_terms_in_top(10)
    ...     .having_other_terms_ordered_by("OCC")
    ...     .having_other_term_occurrences_between(None, None)
    ...     .having_other_term_citations_between(None, None)
    ...     .having_other_terms_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # CHART PARAMS:
    ...     .using_title_text("Butterfly Plot")
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> plot.write_html("docsrc/_generated/px.discov.associations.butterfly_plot.html")

.. raw:: html

    <iframe src="../_generated/px.discov.associations/butterfly_plot.html"
    height="800px" width="100%" frameBorder="0"></iframe>


"""

import plotly.graph_objects as go  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.discov.assoc._intern.dataframe import DataFrame


class ButterflyPlot(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def _step_01_create_data_frame(self):
        return DataFrame().update(**self.params.__dict__).run()

    # -------------------------------------------------------------------------
    def _step_02_remove_col_terms_from_index(self, matrix):
        return matrix.drop(index=matrix.columns)

    # -------------------------------------------------------------------------
    def _step_03_build_butterfly_plot(self, matrix):

        name_a = matrix.columns[0]
        name_b = matrix.columns[1]

        x_max_value = matrix.max().max()

        title_text = self.params.title_text
        if title_text == "":
            title_text = "Butterfly Plot"

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                y=matrix.index,
                x=matrix[name_a],
                name=name_a,
                orientation="h",
                marker={"color": "#7793a5"},
            )
        )

        fig.add_trace(
            go.Bar(
                y=matrix.index,
                x=matrix[name_b].map(lambda w: -w),
                name=name_b,
                orientation="h",
                marker={"color": "#465c6b"},
            )
        )

        fig.update_layout(barmode="overlay")

        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            title_text=title_text,
        )
        fig.add_vline(
            x=0.0,
            line={
                "color": "lightgray",
                "width": 2,
                "dash": "dot",
            },
        )

        fig.update_xaxes(
            linecolor="gray",
            linewidth=2,
            gridcolor="lightgray",
            griddash="dot",
            title_text="OCC",
        )
        fig.update_yaxes(
            linecolor="white",
            linewidth=0,
            autorange="reversed",
            gridcolor="lightgray",
            griddash="dot",
            # title_text=field_label,
        )

        # sets xaxis range to (-x_max_value, x_max_value)
        fig.update_layout(
            xaxis_range=[-x_max_value, x_max_value],
        )

        # sets the legend position upper left
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            )
        )

        return fig

    # -------------------------------------------------------------------------
    def run(self):
        matrix = self._step_01_create_data_frame()
        col_terms = self._step_02_remove_col_terms_from_index(matrix)
        return self._step_03_build_butterfly_plot(matrix)
