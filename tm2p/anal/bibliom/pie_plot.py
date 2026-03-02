"""
Pie Plot
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.anal.bibliom.pie_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>


Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.anal.bibliom import PiePlot
    >>> plot = (
    ...     PiePlot()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     #
    ...     # TERMS:
    ...     .having_items_in_top(15)
    ...     .having_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # PLOT:
    ...     .using_title_text("Most Frequent Author Keywords")
    ...     .using_pie_hole(0.4)
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
    >>> plot.write_html("docsrc/_generated/px.anal.bibliom.pie_plot.html")



"""

from tm2p._intern import ParamsMixin
from tm2p._intern.indic import BibliometricIndicators
from tm2p._intern.plot.pie_plot import pie_plot


class PiePlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        df = BibliometricIndicators().update(**self.params.__dict__).run()
        fig = pie_plot(params=self.params, dataframe=df)

        return fig


#
