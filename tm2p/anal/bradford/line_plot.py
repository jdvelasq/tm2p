"""
Line Plot
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.anal.bradford.line_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>


Smoke tests:
    >>> from tm2p.anal.bradford import LinePlot
    >>> (
    ...     LinePlot()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... ).write_html("docsrc/_generated/px.anal.bradford.line_plot.html")



"""

import plotly.express as px  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.anal.bradford.zones import ZonesDataFrame


class LinePlot(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        """:meta private:"""

        zones = ZonesDataFrame().update(**self.params.__dict__).run()

        fig = px.line(
            zones,
            x="NO",
            y="OCC",
            title="Source Clustering through Bradford's Law",
            markers=True,
            hover_data=[zones.index, "OCC"],
            log_x=True,
        )
        fig.update_traces(
            marker=dict(size=5, line=dict(color="darkslategray", width=1)),
            marker_color="rgb(171,171,171)",
            line=dict(color="darkslategray"),
        )
        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title=None,
            xaxis_showticklabels=False,
        )
        fig.update_yaxes(
            linecolor="gray",
            linewidth=2,
            gridcolor="lightgray",
            griddash="dot",
        )
        fig.update_xaxes(
            linecolor="gray",
            linewidth=2,
            gridcolor="lightgray",
            griddash="dot",
            tickangle=270,
        )

        core = len(zones.loc[zones.ZONE == 1])

        fig.add_shape(
            type="rect",
            x0=1,
            y0=0,
            x1=core,
            y1=zones.OCC.max(),
            line=dict(
                color="lightgrey",
                width=2,
            ),
            fillcolor="lightgrey",
            opacity=0.2,
        )

        fig.data = fig.data[::-1]

        return fig


#
#
