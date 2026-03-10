"""
CumulativeTrendsPlot
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.anal.trends.cumulative_trends_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.anal.trends import CumulativeTrendsPlot
    >>> fig = (
    ...     CumulativeTrendsPlot()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     #
    ...     # ITEMS:
    ...     .having_items_in_top(5)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # PLOT:
    ...     .using_title_text("Cumulative Line Plot")
    ...     .using_xaxes_title_text("YEAR")
    ...     .using_yaxes_title_text("Cumulative occurrences")
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> fig.write_html("docsrc/_generated/px.anal.trends.cumulative_trends_plot.html")

"""

import plotly.express as px  # type: ignore

from tm2p._intern import ParamsMixin

from .cumulative_trends import CumulativeTrends

LINE_COLORS = (
    #
    # TABLEAU COLORS:
    # from matplotlib.colors.TABLEAU_COLORS
    [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]
    + px.colors.qualitative.Pastel1
    + px.colors.qualitative.Pastel2
    + px.colors.qualitative.Dark24
    + px.colors.qualitative.Light24
    + px.colors.qualitative.Set1
    + px.colors.qualitative.Set2
    + px.colors.qualitative.Set3
)
TEXTLEN = 40


class CumulativeTrendsPlot(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        """:meta private:"""

        df = CumulativeTrends().update(**self.params.__dict__).run()
        df = df.T

        title_text = self.params.title_text
        xaxes_title_text = self.params.xaxes_title_text
        yaxes_title_text = self.params.yaxes_title_text

        fig = px.line(
            df,
            x=df.index.to_list(),
            y=df.columns.to_list(),
            # hover_data=df,
            markers=True,
        )

        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            title_text=title_text,
        )

        fig.update_traces(
            marker={
                "size": 9,
                "line": {
                    "color": "#465c6b",
                    "width": 1,
                },
            }
        )

        for i, trace in enumerate(fig.data):
            color = LINE_COLORS[i]
            trace.update(line={"color": color}, marker_color=color)  # type: ignore

        tick_vals = df.index.to_list()
        tick_text = [str(v) for v in tick_vals]

        fig.update_xaxes(
            linecolor="gray",
            linewidth=2,
            gridcolor="lightgray",
            griddash="dot",
            tickangle=270,
            title_text=xaxes_title_text,
            tickmode="array",
            tickvals=tick_vals,
            ticktext=tick_text,
        )
        fig.update_yaxes(
            linecolor="gray",
            linewidth=2,
            gridcolor="lightgray",
            griddash="dot",
            title_text=yaxes_title_text,
        )

        return fig
