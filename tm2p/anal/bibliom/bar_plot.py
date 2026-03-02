"""
Bar Plot
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.report.visualization import BarPlot
    >>> plot = (
    ...     BarPlot()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     #
    ...     # TERMS:
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # PLOT:
    ...     .using_title_text("Bar Plot")
    ...     .using_xaxes_title_text("Author Keywords")
    ...     .using_yaxes_title_text("OCC")
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
    >>> plot.write_html("tmp/px.database.metrics.performance.bar_plot.html")

"""

from tm2p._intern import ParamsMixin
from tm2p._intern.plot.bar_plot import bar_plot
from tm2p.anal._intern.performance.performance_metrics import PerformanceMetrics


class BarPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        df = PerformanceMetrics().update(**self.params.__dict__).run()
        fig = bar_plot(params=self.params, df=df)

        return fig
