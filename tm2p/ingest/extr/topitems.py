"""
TopItemsExtractor
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.ingest.extr import TopItemsExtractor
    >>> items = (
    ...     TopItemsExtractor()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     #
    ...     # SEARCH:
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... )
    >>> from pprint import pprint
    >>> pprint(items[:10])
    ['artificial intelligence',
     'banking',
     'blockchain',
     'china',
     'financial inclusion',
     'financial services',
     'financial technology',
     'fintech',
     'green finance',
     'innovation']


"""

from tm2p._intern import ParamsMixin
from tm2p.anal.metrics.metrics import Metrics


class TopItemsExtractor(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        data_frame = Metrics().update(**self.params.__dict__).run()
        terms = data_frame.index.tolist()
        terms = sorted(terms)

        return terms
