"""
World Map
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.anal.bibliom.world_map.html"
    height="600px" width="100%" frameBorder="0"></iframe>


Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.anal.metrics import WorldMap
    >>> plot = (
    ...     WorldMap()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.CTRY)
    ...     #
    ...     # TERMS:
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # PLOT:
    ...     .using_title_text("Countries' Scientific Production")
    ...     .using_colormap("Blues")
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
    >>> plot.write_html("docsrc/_generated/px.anal.bibliom.world_map.html")



"""

from tm2p._intern import ParamsMixin
from tm2p._intern.plot.world_map import world_map

from .metrics import Metrics


class WorldMap(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        df = Metrics().update(**self.params.__dict__).run()
        fig = world_map(params=self.params, dataframe=df)

        return fig


#
