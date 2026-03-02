"""
Query
===============================================================================

Smoke test:
    >>> from tm2p.ingest.oper import Query
    >>> df = (
    ...     Query()
    ...     #
    ...     .with_query_expression("SELECT SRC_NORM FROM database LIMIT 5;")
    ...     #
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... )
    >>> df
                                                SRC_NORM
    0      Journal of Financial Reporting and Accounting
    1  Harnessing Blockchain-Digital Twin Fusion for ...
    2      Journal of Financial Reporting and Accounting
    3                       Electronic Commerce Research
    4      International Review of Economics and Finance

"""

import duckdb

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip


class Query(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        database = load_filtered_main_csv_zip(params=self.params)
        duckdb.register("database", database)
        if self.params.query_expression is None:
            raise ValueError(
                "Query expression cannot be None. Use .with_query_expression() to set it."
            )
        return duckdb.query(self.params.query_expression).df()
