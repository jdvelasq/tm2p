"""
.. raw:: html

    <iframe src="../_generated/px.anal.rpys.rpys_plot.html"
    height="800px" width="100%" frameBorder="0"></iframe>

===============================================================================

.. raw:: html

    <iframe src="../_generated/px.anal.rpys.rpys_plot.html"
    height="800px" width="100%" frameBorder="0"></iframe>


Smoke tests:
    >>> from tm2p.anal.rpys import RPYSPlot
    >>> plot = (
    ...     RPYSPlot()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .run()
    ... )
    >>> plot.write_html("docsrc/_generated/px.anal.rpys.rpys_plot.html")



"""

import plotly.graph_objects as go  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.anal.rpys.metrics import Metrics


class RPYSPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        data_frame = Metrics().update(**self.params.__dict__).run()

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=data_frame.index,
                y=data_frame["N_GCR"],
                fill="tozeroy",
                name="N_GCR",
                opacity=0.3,
                marker_color="lightgrey",  # darkslategray
            )
        )
        fig.add_trace(
            go.Scatter(
                x=data_frame.index,
                y=data_frame["MEDIAN"],
                fill="tozeroy",
                name="Median",
                opacity=0.8,
                marker_color="darkslategray",
            )
        )
        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            title="Reference Spectroscopy",
        )

        fig.update_traces(
            marker=dict(
                size=6,
                line=dict(color="darkslategray", width=2),
            ),
        )
        fig.update_xaxes(
            linecolor="gray",
            linewidth=2,
            gridcolor="lightgray",
            griddash="dot",
        )
        fig.update_yaxes(
            linecolor="gray",
            linewidth=2,
            gridcolor="lightgray",
            griddash="dot",
            title="Cited References",
        )

        return fig
