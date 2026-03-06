"""
Ranking Chart
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.anal.annual_metrics.ranking_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>


Smoke tests:
>>> from tm2p.anal.annual_metrics import Column
    >>> from tm2p.anal.annual_metrics import RankingPlot
    >>> fig = (
    ...     RankingPlot()
    ...     #
    ...     .with_plotting_column(Column.CUMUL_OCC)
    ...     #
    ...     .using_title_text("Average Citations Per Year")
    ...     .using_xaxes_title_text("Years")
    ...     .using_yaxes_title_text("Average Citations Per Year")
    ...     #
    ...     .using_line_width(1.5)
    ...     .using_marker_size(7)
    ...     .using_textfont_size(10)
    ...     .using_yshift(4)
    ...     #
    ...     .where_root_directory("tests/regtech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... )
    >>> type(fig).__name__
    'Figure'
    >>> fig.write_html("docsrc/_generated/px.anal.annual_metrics.ranking_plot.html")




"""

import plotly.express as px  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.anal.annual_metrics.metrics import Metrics

MARKER_COLOR = "#7793a5"
MARKER_LINE_COLOR = "#465c6b"


class RankingPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        df = Metrics().update(**self.params.__dict__).run()
        df["Rank"] = range(1, len(df) + 1)

        fig = px.line(
            df,
            x="Rank",
            y=self.params.plotting_column.value,  # type: ignore
            hover_data=df.columns.to_list(),
            markers=True,
        )

        fig.update_traces(
            marker={
                "size": self.params.marker_size,
                "line": {
                    "color": MARKER_LINE_COLOR,
                    "width": 1,
                },
            },
            marker_color=MARKER_COLOR,
            line={
                "color": MARKER_LINE_COLOR,
                "width": self.params.line_width,
            },
        )
        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            title_text=self.params.title_text,
        )
        fig.update_yaxes(
            linecolor="gray",
            linewidth=1,
            gridcolor="lightgray",
            griddash="dot",
            title=self.params.yaxes_title_text,
        )
        fig.update_xaxes(
            linecolor="gray",
            linewidth=1,
            gridcolor="lightgray",
            griddash="dot",
            title=self.params.xaxes_title_text,
        )

        for name, row in df.iterrows():
            fig.add_annotation(
                x=row["Rank"],
                y=row[self.params.items_order_by.value],
                text=name,
                showarrow=False,
                textangle=-90,
                yanchor="bottom",
                font={
                    "size": self.params.textfont_size,
                },
                yshift=self.params.yshift,
            )

        return fig
