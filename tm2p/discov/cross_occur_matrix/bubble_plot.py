"""
Bubble Plot
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.discov.cross_occur_matrix.bubble_plot.html"
    height="800px" width="100%" frameBorder="0"></iframe>

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.discov.cross_occur_matrix import BubblePlot
    >>> fig = (
    ...     BubblePlot()
    ...     #
    ...     # COLUMNS:
    ...     .with_column_field(Field.AUTHKW_TOK)
    ...     .having_column_items_in_top(10)
    ...     .having_column_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_column_item_occurrences_between(None, None)
    ...     .having_column_item_citations_between(None, None)
    ...     .having_column_items_in(None)
    ...     #
    ...     # ROWS:
    ...     .with_index_field(Field.AUTH_NORM)
    ...     .having_index_items_in_top(15)
    ...     .having_index_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_index_item_occurrences_between(0, None)
    ...     .having_index_item_citations_between(None, None)
    ...     .having_index_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # PLOT:
    ...     .using_title_text(None)
    ...     .using_colormap("Blues")
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
    >>> fig.write_html("docsrc/_generated/px.discov.cross_occur_matrix.bubble_plot.html")


"""

from tm2p._intern import ParamsMixin
from tm2p._intern.plot.bubble_plot import bubble_plot
from tm2p.discov.cross_occur_matrix.matrix_list import MatrixList


class BubblePlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        data_frame = MatrixList().update(**self.params.__dict__).run()

        fig = bubble_plot(
            self.params,
            x_name="rows",
            y_name="columns",
            size_col="OCC",
            dataframe=data_frame,
        )

        return fig
