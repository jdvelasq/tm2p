"""
Coverage
===============================================================================

Smoke tests:
    >>> from tm2p import CorpusField
    >>> from tm2p.ingest.records import Coverage
    >>> (
    ...     Coverage()
    ...     .with_source_field(CorpusField.AUTH_KEY_RAW)
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .run()
    ... )



"""

from tm2p import CorpusField
from tm2p._intern import ParamsMixin
from tm2p._intern.data_access.load_filtered_main_csv_zip import (
    load_filtered_main_csv_zip,
)


class Coverage(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        source_field = self.params.source_field.value
        record_id = CorpusField.RID.value

        documents = load_filtered_main_csv_zip(params=self.params)
        documents = documents.reset_index()
        documents = documents[[source_field, record_id]]

        n_documents = len(documents)

        documents = documents.dropna()
        documents = documents.assign(num_documents=1)
        documents[source_field] = documents[source_field].str.split("; ")
        documents = documents.explode(source_field)

        documents = documents.groupby(by=[source_field]).agg(
            {"num_documents": "count", record_id: list}
        )
        documents = documents.sort_values(by=["num_documents"], ascending=False)

        documents = documents.reset_index()

        documents = documents.groupby(by="num_documents", as_index=False).agg(
            {record_id: list, source_field: list}
        )

        documents = documents.sort_values(by=["num_documents"], ascending=False)
        documents[record_id] = documents[record_id].apply(
            lambda x: [term for sublist in x for term in sublist]
        )

        documents = documents.assign(cum_sum_documents=documents[record_id].cumsum())
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

        documents = documents.assign(cum_sum_items=documents[source_field].cumsum())
        documents = documents.assign(cum_sum_items=documents.cum_sum_items.apply(set))
        documents = documents.assign(cum_sum_items=documents.cum_sum_items.apply(len))

        documents.drop(record_id, axis=1, inplace=True)
        documents.drop(source_field, axis=1, inplace=True)
        documents = documents.reset_index(drop=True)

        documents = documents.rename(
            columns={
                "num_documents": "min_occ",
                "cum_sum": "cum num documents",
                "cum_sum_items": "cum num items",
            }
        )

        return documents
