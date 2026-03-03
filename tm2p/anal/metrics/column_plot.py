"""
Column Plot
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.anal.bibliom.column_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.anal.metrics import ColumnPlot
    >>> plot = (
    ...     ColumnPlot()
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
    ...     .using_title_text("Ranking Plot")
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
    >>> plot.write_html("docsrc/_generated/px.anal.bibliom.column_plot.html")


"""

from tm2p._intern import ParamsMixin
from tm2p._intern.plot.column_plot import column_plot

from .metrics import Metrics


class ColumnPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        df = Metrics().update(**self.params.__dict__).run()
        fig = column_plot(params=self.params, dataframe=df)

        return fig


#
