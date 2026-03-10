"""
TopicDynamicsPlot
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.anal.topic_trends.burst.topic_dynamics_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.anal.topic_trends.burst.topic_dynamics_plot import TopicDynamicsPlot
    >>> fig = (
    ...     TopicDynamicsPlot()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.CONCEPT_NORM)
    ...     .having_items_in_top(50)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # KLEINBERG BURST:
    ...     .using_kleinberg_burst_rate(2.0)
    ...     .using_kleinberg_burst_gamma(1.0)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> fig.write_html("docsrc/_generated/px.anal.topic_trends.burst.topic_dynamics_plot.html")



"""

import plotly.graph_objects as go  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.anal.topic_trends.burst.topic_dynamics import TopicDynamics


class TopicDynamicsPlot(
    ParamsMixin,
):
    """:meta private:"""

    # ---------------------------------------------------------------------------
    def run(self):

        df = TopicDynamics().update(**self.params.__dict__).run()
        min_occ = df.OCC.min()
        max_occ = df.OCC.max()
        df["height"] = 0.15 + 0.82 * (df.OCC - min_occ) / (max_occ - min_occ)

        df["width"] = df.DURATION

        fig = go.Figure(
            go.Bar(
                x=df.width,
                y=df.index,
                base=df.START,
                width=df.height,
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
