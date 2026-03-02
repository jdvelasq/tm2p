"""
Network Edges Frame
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.main_path import NetworkEdgesDataFrame
    >>> (
    ...     NetworkEdgesDataFrame()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(None)
    ...     .using_citation_threshold(0)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
                                          citing_article  ... points
    0  Gomber P., 2018, J MANAGE INF SYST, V35, P220 ...  ...      3
    1  Gomber P., 2018, J MANAGE INF SYST, V35, P220 ...  ...      3
    2                   Hu Z., 2019, SYMMETRY, V11 1:176  ...      4
    3       Alt R., 2018, ELECTRON MARK, V28, P235 1:150  ...      1
    4       Alt R., 2018, ELECTRON MARK, V28, P235 1:150  ...      2
    5  Gozman D., 2018, J MANAGE INF SYST, V35, P145 ...  ...      3
    <BLANKLINE>
    [6 rows x 3 columns]


"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.main_path._intern.compute_main_path import internal__compute_main_path


class NetworkEdgesDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        #
        # Creates a table with citing and cited articles
        _, data_frame = internal__compute_main_path(params=self.params)
        return data_frame
