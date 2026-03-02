"""
Bar Chart
===============================================================================


Smoke tests:
    >>> # Create, configure, and run the plotter
    >>> from tm2p.analyze.metrics.trending_terms_by_year.user import BarChart
    >>> (
    ...     BarChart()
    ...     #
    ...     # FIELD:
    ...     .with_field("author_keywords_raw")
    ...     .having_terms_per_year(5)
    ...     .having_items_in(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).write_html("docsrc/_generated/px.database.metrics.ternding_terms_by_year.user.bar_chart.html")

.. raw:: html

    <iframe src="../_generated/px.database.metrics.ternding_terms_by_year.user.bar_chart.html"
    height="600px" width="100%" frameBorder="0"></iframe>


"""

import plotly.graph_objects as go  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.anal.trending_items_by_year.data_frame import DataFrame


class BarChart(
    ParamsMixin,
):
    """:meta private:"""

    # ---------------------------------------------------------------------------
    def run(self):

        words_by_year = (
            DataFrame()
            .update(**self.params.__dict__)
            .update(terms_order_by="OCC")
            .run()
        )

        fig = go.Figure(
            go.Bar(
                x=words_by_year.width,
                y=words_by_year.index,
                base=words_by_year.year_q1,
                width=words_by_year.height,
                orientation="h",
                marker_color="lightslategrey",
            ),
        )
        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
        )
        fig.update_yaxes(
            linecolor="gray",
            linewidth=1,
            gridcolor="lightgray",
            griddash="dot",
        )
        fig.update_xaxes(
            linecolor="gray",
            linewidth=1,
            gridcolor="lightgray",
            griddash="dot",
            tickangle=270,
            dtick=1.0,
        )

        return fig


#
