"""
Ranking Chart
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.discov.overview.average_citations_per_year.ranking_chart.html"
    height="600px" width="100%" frameBorder="0"></iframe>


Smoke tests:
    >>> from tm2p.discov.overview.average_citations_per_year import RankingChart
    >>> fig = (
    ...     RankingChart()
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
    >>> fig.write_html("docsrc/_generated/px.discov.overview.average_citations_per_year.ranking_chart.html") # doctest: +SKIP




"""

from tm2p import ItemOrderBy
from tm2p._intern import ParamsMixin
from tm2p._intern.plot.ranking_chart import ranking_chart
from tm2p.discov.overview.aver_cit_per_year.dataframe import DataFrame


class RankingChart(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        dataframe = DataFrame().update(**self.params.__dict__).run()
        dataframe["Rank"] = range(1, len(dataframe) + 1)
        self.having_items_ordered_by(ItemOrderBy.GCS_PER_YEAR_AVG)
        fig = ranking_chart(params=self.params, dataframe=dataframe)

        return fig
