"""
FullMatchExtractor
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.ingest.extr import FullMatchExtractor
    >>> terms = (
    ...     FullMatchExtractor()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     #
    ...     # SEARCH:
    ...     .having_text_matching("b.+")
    ...     .having_case_sensitive(False)
    ...     .having_regex_flags(0)
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
    ['bank',
     'bank 30',
     'bank competition',
     'bank credit',
     'bank fintech',
     'bank fintech partnership',
     'bank performance',
     'bank risk-taking',
     'banking',
     'banking competition']


"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.extr._helpers.fullmatch import extract_fullmatch


class FullMatchExtractor(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        return extract_fullmatch(self.params)
