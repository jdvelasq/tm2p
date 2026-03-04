"""
Heatmap
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.discov.co_occur_matrix.heatmap.html"
    height="600px" width="100%" frameBorder="0"></iframe>

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.discov.co_occur_matrix import Heatmap
    >>> fig = (
    ...     Heatmap()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
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
    >>> fig.write_html("docsrc/_generated/px.discov.co_occur_matrix.heatmap.html")




"""

from tm2p._intern import ParamsMixin
from tm2p._intern.plot.heatmap import heatmap

from .matrix import Matrix


class Heatmap(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        data_frame = Matrix().update(**self.params.__dict__).run()
        fig = heatmap(self.params, data_frame)
        return fig
