"""
StartsWithExtractor
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.ingest.extr import StartsWithExtractor
    >>> terms = (
    ...     StartsWithExtractor()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     #
    ...     # SEARCH:
    ...     .having_text_matching("finan")
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
    ['finance',
     'finance technology',
     'financial capability',
     'financial computing',
     'financial constraints',
     'financial crisis',
     'financial development',
     'financial disintermediation',
     'financial exclusion',
     'financial globalization']


"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.extr._helpers.startswith import extract_startswith


class StartsWithExtractor(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        return extract_startswith(self.params)


#
