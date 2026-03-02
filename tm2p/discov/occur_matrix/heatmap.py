"""
Heatmap
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.discov.occur_matrix.heatmap.html"
    height="800px" width="100%" frameBorder="0"></iframe>

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix import Heatmap
    >>> fig = (
    ...     Heatmap()
    ...     #
    ...     # COLUMNS:
    ...     .with_column_field(CorpusField.AUTHKW_TOK)
    ...     .having_column_items_in_top(10)
    ...     .having_column_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_column_item_occurrences_between(None, None)
    ...     .having_column_item_citations_between(None, None)
    ...     .having_column_items_in(None)
    ...     #
    ...     # ROWS:
    ...     .with_index_field(CorpusField.AUTH_NORM)
    ...     .having_index_items_in_top(15)
    ...     .having_index_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_index_item_occurrences_between(0, None)
    ...     .having_index_item_citations_between(None, None)
    ...     .having_index_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_item_counters(True)
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
    >>> fig.write_html("docsrc/_generated/px.discov.occur_matrix.heatmap.html")




"""

from tm2p._intern import ParamsMixin
from tm2p._intern.plot.heatmap import heatmap
from tm2p.discov.occur_matrix.matrix import Matrix


class Heatmap(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        data_frame = Matrix().update(**self.params.__dict__).run()
        fig = heatmap(self.params, data_frame)
        return fig
