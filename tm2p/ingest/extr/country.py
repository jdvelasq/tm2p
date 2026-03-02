"""
CountryExtractor
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.ingest.extr import CountryExtractor
    >>> terms = (
    ...     CountryExtractor()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     #
    ...     # SEARCH:
    ...     .having_text_matching("FINTECH")
    ...     .having_case_sensitive(False)
    ...     .having_regex_flags(0)
    ...     .having_regex_search(False)
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
    ['China', 'Hong Kong', 'Jordan', 'Russia', 'Saudi Arabia', 'Taiwan', 'Ukraine']


"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.extr._helpers.country import extract_country


class CountryExtractor(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        return extract_country(self.params)
