"""
Cleveland Dot Plot
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.report.visualization import ClevelandDotPlot
    >>> plot = (
    ...     ClevelandDotPlot()
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
    ...     .using_title_text("Cleveland Dot Plot")
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
    >>> plot.write_html("tmp/px.database.metrics.performance.cleveland_dot_plot.html")

"""

from tm2p._intern import ParamsMixin
from tm2p._intern.indic import BibliometricIndicators
from tm2p._intern.plot.cleveland_dot_plot import cleveland_dot_plot


class ClevelandDotPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        df = BibliometricIndicators().update(**self.params.__dict__).run()
        fig = cleveland_dot_plot(params=self.params, dataframe=df)

        return fig


#
#
