"""
Query
===============================================================================

Smoke test:
    >>> from tm2p.ingest.operations import Query
    >>> df = (
    ...     Query()
    ...     #
    ...     .with_query_expression("SELECT SRC_TITLE_NORM FROM database LIMIT 5;")
    ...     #
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... )
    >>> df
                                          SRC_TITLE_NORM
    0                   Journal of Innovation Management
    1  Proceedings - 3rd International Conference on ...
    2                          Telecommunications Policy
    3                               Financial Innovation
    4  International Journal of Applied Engineering R...





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
