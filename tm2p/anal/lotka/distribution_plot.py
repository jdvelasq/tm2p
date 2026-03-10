"""
DistributionPlot
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.anal.lotka.distribution_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>


Smoke tests:
    >>> from tm2p.anal.lotka import DistributionPlot

    >>> fig = (
    ...     DistributionPlot()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...      #
    ...      .run()
    ... )
    >>> type(fig).__name__
    'Figure'
    >>> fig.write_html("docsrc/_generated/px.anal.lotka.distribution_plot.html")




"""

import plotly.graph_objects as go  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.anal.lotka.distribution import Distribution


class DistributionPlot(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        """:meta private:"""

        data_frame = Distribution().update(**self.params.__dict__).run()

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=data_frame["DOC_WRITTEN"],
                y=data_frame["AUTH_PROP"],
                fill="tozeroy",
                name="Real",
                opacity=0.5,
                marker_color="darkslategray",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=data_frame["DOC_WRITTEN"],
                y=data_frame["PROP_AUTH_THEO"],
                fill="tozeroy",
                name="Theoretical",
                opacity=0.5,
                marker_color="lightgrey",
            )
        )
        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            title="Author Productivity through Lotka's Law",
        )

        fig.update_traces(
            marker=dict(
                size=7,
                line=dict(color="darkslategray", width=2),
            ),
        )
        fig.update_xaxes(
            linecolor="gray",
            linewidth=2,
            gridcolor="lightgray",
            griddash="dot",
            title="DOC_WRITTEN",
        )
        fig.update_yaxes(
            linecolor="gray",
            linewidth=2,
            gridcolor="lightgray",
            griddash="dot",
            title="AUTH_PROP",
        )

        return fig


#
