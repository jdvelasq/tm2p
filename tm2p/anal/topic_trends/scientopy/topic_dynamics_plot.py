"""
TopicDynamicsPlot
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.anal.topic_trends.scientopy.topic_dynamics_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.anal.topic_trends.scientopy.topic_dynamics_plot import TopicDynamicsPlot
    >>> fig = (
    ...     TopicDynamicsPlot()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_RAW)
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # TIME WINDOW:
    ...     .with_time_window(2)
    ...     #
    ...     # CHART PARAMS:
    ...     .using_xaxes_title_text(None)
    ...     .using_yaxes_title_text(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> type(fig).__name__
    'Figure'
    >>> fig.write_html("docsrc/_generated/px.anal.topic_trends.scientopy.topic_dynamics_plot.html")



"""

import plotly.express as px  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.anal.topic_trends.scientopy.topic_dynamics import TopicDynamics


class TopicDynamicsPlot(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def internal__compute_data_frame(self):

        data_frame = TopicDynamics().update(**self.params.__dict__).run()

        # extracts the name of column starting with 'between'
        between = [_ for _ in data_frame.columns if _.startswith("between")][0]
        before = [_ for _ in data_frame.columns if _.startswith("before")][0]

        fig_data = data_frame[["OCC", before, between]].copy()
        fig_data[self.params.source_field] = fig_data.index
        fig_data = fig_data.reset_index(drop=True)

        fig_data = fig_data.melt(
            id_vars=self.params.source_field,
            value_vars=[before, between],
        )

        fig_data = fig_data.rename(
            columns={
                self.params.source_field: self.params.source_field.value.replace(
                    "_", " "
                ).title(),
                "variable": "Period",
                "value": "Num Documents",
            }
        )

        self.before = before
        self.between = between
        self.data_frame = fig_data

    # -------------------------------------------------------------------------
    def internal__make_fig(self):

        #
        # Extracs only the performance metrics data frame
        fig = px.bar(
            self.data_frame,
            x="Num Documents",
            y=self.params.source_field.value.replace("_", " ").title(),
            color="Period",
            orientation="h",
            color_discrete_map={
                self.before: "#7793a5",
                self.between: "#465c6b",
            },
        )
        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
        )
        fig.update_yaxes(
            linecolor="gray",
            linewidth=2,
            autorange="reversed",
            title=self.params.yaxes_title_text,
        )
        fig.update_xaxes(
            linecolor="gray",
            linewidth=2,
            gridcolor="gray",
            griddash="dot",
            title=self.params.xaxes_title_text,
        )

        self.fig = fig

    # -------------------------------------------------------------------------
    def run(self):
        self.internal__compute_data_frame()
        self.internal__make_fig()
        return self.fig


# =============================================================================
