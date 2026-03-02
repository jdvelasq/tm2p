"""
IntersectionExtractor
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.ingest.extr import IntersectionExtractor
    >>> terms = (
    ...     IntersectionExtractor()
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
    >>> # Print the first 10 extracted terms
    >>> from pprint import pprint
    >>> pprint(terms[:10])
    ['a comparative study',
     'actor network theory',
     'actualization',
     'agriculture',
     'agropay',
     'alipay',
     'and systemic risk',
     'apicist 2016',
     'artificial intelligence',
     'bank']

"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.extr._helpers.intersection import extract_intersection


class IntersectionExtractor(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        return extract_intersection(self.params)


#

#
#
