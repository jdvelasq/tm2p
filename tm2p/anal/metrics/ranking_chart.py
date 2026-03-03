"""
Ranking Chart
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.anal.bibliom.ranking_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>


Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.anal.metrics import RankingPlot
    >>> plot = (
    ...     RankingPlot()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     #
    ...     # TERMS:
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # PLOT:
    ...     .using_line_color("black")
    ...     .using_line_width(1.5)
    ...     .using_marker_size(7)
    ...     .using_textfont_size(10)
    ...     .using_title_text("Ranking Plot")
    ...     .using_xaxes_title_text("Author Keywords")
    ...     .using_yaxes_title_text("OCC")
    ...     .using_yshift(4)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... )
    >>> type(plot).__name__
    'Figure'
    >>> plot.write_html("docsrc/_generated/px.anal.bibliom.ranking_plot.html")



"""

from tm2p._intern import ParamsMixin
from tm2p._intern.plot.ranking_chart import ranking_chart

from .metrics import Metrics


class RankingPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        df = Metrics().update(**self.params.__dict__).run()
        df["Rank"] = range(1, len(df) + 1)
        fig = ranking_chart(params=self.params, dataframe=df)

        return fig


#
