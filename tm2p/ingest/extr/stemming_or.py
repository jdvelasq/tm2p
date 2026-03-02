"""
StemmingOrExtractor
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.ingest.extr import StemmingOrExtractor
    >>> terms = (
    ...     StemmingOrExtractor()
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
    >>> pprint(terms[:10]) # doctest: +SKIP




"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.extr._helpers.stemming import extract_stemming_or


class StemmingOrExtractor(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        return extract_stemming_or(self.params)


#
