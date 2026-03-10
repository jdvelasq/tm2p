"""
TopicDynamicsPlot
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.anal.topic_trends.bibliometrix.topic_dynamics_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>


Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.anal.topic_trends.bibliometrix.topic_dynamics_plot import TopicDynamicsPlot
    >>> fig = (
    ...     TopicDynamicsPlot()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_RAW)
    ...     .having_items_per_year(5)
    ...     .having_items_in(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> fig.write_html("docsrc/_generated/px.anal.topic_trends.bibliometrix.topic_dynamics_plot.html")



"""

import plotly.graph_objects as go  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.anal.topic_trends.bibliometrix.topic_dynamics import TopicDynamics


class TopicDynamicsPlot(
    ParamsMixin,
):
    """:meta private:"""

    # ---------------------------------------------------------------------------
    def run(self):

        words_by_year = (
            TopicDynamics()
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
