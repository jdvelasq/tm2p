"""
Coverage
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.ingest.rec import Coverage
    >>> (
    ...     Coverage()
    ...     .with_source_field(Field.AUTHKW_RAW)
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .run()
    ... )
        OCC  CUM_SUM_DOCS COVERAGE  CUM_SUM_ITEMS
    0    59            59  32.78 %              1
    1    50           109  60.56 %              2
    2    13           115  63.89 %              3
    3    11           118  65.56 %              4
    4    10           120  66.67 %              5
    5     9           127  70.56 %              9
    6     8           134  74.44 %             10
    7     7           136  75.56 %             12
    8     6           137  76.11 %             15
    9     5           138  76.67 %             19
    10    4           138  76.67 %             22
    11    3           142  78.89 %             39
    12    2           146  81.11 %             81
    13    1           154  85.56 %            582


"""

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access.load_filtered_main_csv_zip import (
    load_filtered_main_csv_zip,
)
from tm2p.enum.column import COVERAGE, CUM_SUM_DOCS, CUM_SUM_ITEMS, OCC, RID


class Coverage(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        FIELD = self.params.source_field.value

        documents = load_filtered_main_csv_zip(params=self.params)
        documents = documents.reset_index()
        documents = documents[[FIELD, RID]]

        n_documents = len(documents)

        documents = documents.dropna()
        documents = documents.assign(num_documents=1)
        documents[FIELD] = documents[FIELD].str.split("; ")
        documents = documents.explode(FIELD)

        documents = documents.groupby(by=[FIELD]).agg(
            {"num_documents": "count", RID: list}
        )
        documents = documents.sort_values(by=["num_documents"], ascending=False)

        documents = documents.reset_index()

        documents = documents.groupby(by="num_documents", as_index=False).agg(
            {RID: list, FIELD: list}
        )

        documents = documents.sort_values(by=["num_documents"], ascending=False)
        documents[RID] = documents[RID].apply(
            lambda x: [term for sublist in x for term in sublist]
        )

        documents = documents.assign(cum_sum_documents=documents[RID].cumsum())
        documents = documents.assign(
            cum_sum_documents=documents.cum_sum_documents.apply(set)
        )
        documents = documents.assign(
            cum_sum_documents=documents.cum_sum_documents.apply(len)
        )

        documents = documents.assign(
            coverage=documents.cum_sum_documents.map(
                lambda x: f"{100 * x / n_documents:5.2f} %"
            )
        )

        documents = documents.assign(cum_sum_items=documents[FIELD].cumsum())
        documents = documents.assign(cum_sum_items=documents.cum_sum_items.apply(set))
        documents = documents.assign(cum_sum_items=documents.cum_sum_items.apply(len))

        documents.drop(RID, axis=1, inplace=True)
        documents.drop(FIELD, axis=1, inplace=True)
        documents = documents.reset_index(drop=True)

        documents = documents.rename(
            columns={
                "num_documents": OCC,
                "cum_sum_documents": CUM_SUM_DOCS,
                "cum_sum_items": CUM_SUM_ITEMS,
                "coverage": COVERAGE,
            }
        )

        return documents
