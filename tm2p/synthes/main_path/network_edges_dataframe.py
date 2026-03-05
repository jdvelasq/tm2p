"""
Network Edges Frame
===============================================================================

Smoke tests:
    >>> from tm2p.synthes.main_path import NetworkEdgesDataFrame
    >>> df = (
    ...     NetworkEdgesDataFrame()
    ...     #
    ...     # ANALYSIS UNIT:
    ...     .having_items_in_top(None)
    ...     .having_citation_threshold(0)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/regtech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> print(df.head().to_string())
                                                                  CITING_DOC                                                          CITED_DOC  POINTS
    0                    Anagnostopoulos, 2018, J ECON BUS, V100, P7 1:00436            Arner, 2017, NORTHWEST J INT LAW BUS, V37, P373 1:00367      60
    1      Becker, 2020, INTELL SYST ACCOUNT FINANC MANAG, V27, P161 1:00030                Anagnostopoulos, 2018, J ECON BUS, V100, P7 1:00436      12
    2      Becker, 2020, INTELL SYST ACCOUNT FINANC MANAG, V27, P161 1:00030            Arner, 2017, NORTHWEST J INT LAW BUS, V37, P373 1:00367      12
    3  Firmansyah, 2023, INDONES J ELECTR ENG INFORMATICS, V11, P453 1:00006            Arner, 2017, NORTHWEST J INT LAW BUS, V37, P373 1:00367       1
    4  Firmansyah, 2023, INDONES J ELECTR ENG INFORMATICS, V11, P453 1:00006  Becker, 2020, INTELL SYST ACCOUNT FINANC MANAG, V27, P161 1:00030       3

"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.main_path._intern.compute_main_path import compute_main_path


class NetworkEdgesDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        #
        # Creates a table with citing and cited articles
        _, data_frame = compute_main_path(params=self.params)
        return data_frame
