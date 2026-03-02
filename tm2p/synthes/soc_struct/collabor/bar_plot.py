"""
Bar Plot
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.analyze.metrics.collaboration import BarPlot
    >>> fig = (
    ...     BarPlot()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.COUNTRY)
    ...     .having_items_in_top(10)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_items_in(None)
    ...     #
    ...     # PLOT:
    ...     .using_title_text("Collaboration Plot")
    ...     .using_xaxes_title_text("Countries")
    ...     .using_yaxes_title_text("OCC")
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    >>> type(fig).__name__
    'Figure'
    >>> fig.write_html("docsrc/_generated/px.database.metrics.collaboration.bar_plot.html")

.. raw:: html

    <iframe src="../_generated/px.database.metrics.collaboration.bar_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>




"""

import plotly.express as px  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.synthes.soc_struct.collabor.data_frame import DataFrame


class BarPlot(
    ParamsMixin,
):
    """:meta private:"""

    def get_collaboration_metrics(self):
        return DataFrame().update(**self.params.__dict__).run()

    def build_collaboration_bar_plot(self, metrics):

        field = self.params.source_field
        title_text = self.params.title_text
        xaxes_title_text = self.params.xaxes_title_text
        yaxes_title_text = self.params.yaxes_title_text

        metrics = metrics.copy()
        metrics = metrics.reset_index()

        metrics = metrics.melt(
            id_vars=field,
            value_vars=[
                "single_publication",
                "multiple_publication",
            ],
        )
        metrics = metrics.rename(
            columns={
                "variable": "publication",
                "value": "Num Documents",
            }
        )
        metrics.publication = metrics.publication.map(
            lambda x: x.replace("_", " ").title()
        )
        metrics[field] = metrics[field].map(lambda x: x.title())

        fig = px.bar(
            metrics,
            x="Num Documents",
            y=field,
            color="publication",
            title=title_text,
            hover_data=["Num Documents"],
            orientation="h",
            color_discrete_map={
                "Single Publication": "#7793a5",
                "Multiple Publication": "#465c6b",
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
            title_text=yaxes_title_text,
        )
        fig.update_xaxes(
            linecolor="gray",
            linewidth=2,
            gridcolor="gray",
            griddash="dot",
            title_text=xaxes_title_text,
        )

        return fig

    def run(self):

        metrics = self.get_collaboration_metrics()
        fig = self.build_collaboration_bar_plot(metrics)
        return fig


#
#
