"""
ContainsExtractor
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.ingest.extr import ContainsExtractor
    >>> terms = (
    ...     ContainsExtractor()
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
    ['bank fintech',
     'bank fintech partnership',
     'financial technology ( fintech )',
     'fintech',
     'fintech adoption',
     'fintech developers',
     'fintech development',
     'fintech disruption',
     'fintech for development',
     'fintech governance']


"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.extr._helpers.contains import extract_contains


class ContainsExtractor(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        return extract_contains(self.params)
