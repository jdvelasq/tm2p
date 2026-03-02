"""
StemmingAndExtractor
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.ingest.extr import StemmingAndExtractor
    >>> terms = (
    ...     StemmingAndExtractor()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     #
    ...     # SEARCH:
    ...     .having_text_matching(
    ...         (
    ...             "financial technology",
    ...             "artificial intelligence",
    ...         ),
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
    ['artificial intelligence',
     'artificial intelligence ( ai )',
     'artificial intelligence in agriculture',
     'financial technologies',
     'financial technology',
     'financial technology ( fintech )',
     'the role of artificial intelligence in addressing poverty']


"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.extr._helpers.stemming import extract_stemming_and


class StemmingAndExtractor(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        return extract_stemming_and(self.params)


#
