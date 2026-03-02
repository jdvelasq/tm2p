"""
DifferenceExtractor
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.ingest.extr import DifferenceExtractor
    >>> terms = (
    ...     DifferenceExtractor()
    ...     #
    ...     # FIELDS:
    ...     .with_source_fields(
    ...         (Field.AUTHKW_NORM, Field.IDXKW_NORM)
    ...     )
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... )
    >>> from pprint import pprint
    >>> pprint(terms[:10])
    ['5g',
     '6g',
     'access to finance',
     'adoption',
     'adoption drivers',
     'aggregating operators',
     'ai',
     'algorithmic underwriting',
     'alternative data',
     'alternative finance']

"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.extr._helpers.difference import extract_difference


class DifferenceExtractor(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        return extract_difference(self.params)


#
