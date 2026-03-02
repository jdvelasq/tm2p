"""
EndsWithExtractor
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.ingest.extr import EndsWithExtractor
    >>> terms = (
    ...     EndsWithExtractor()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     #
    ...     # SEARCH:
    ...     .having_text_matching("ing")
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
    ['algorithmic underwriting',
     'alternative lending',
     'bank risk-taking',
     'banking',
     'benefit sharing',
     'big-data lending',
     'cloud computing',
     'credit scoring',
     'crowdfunding',
     'data mining']

"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.extr._helpers.endswith import extract_endswith


class EndsWithExtractor(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        return extract_endswith(self.params)


#
