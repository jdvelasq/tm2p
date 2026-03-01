"""
RecordsDataFrame
=======================================================================================


Smoke tests:
    >>> from tm2p.analyze.metrics.records import DataFrame

    >>> # Create, configure, and run the DataFrame generator.
    >>> # The options for the "where_records_ordered_by" method are:
    >>> #   date_newest, date_oldest, global_cited_by_highest, global_cited_by_lowest
    >>> #   local_cited_by_highest, local_cited_by_lowest, first_author_a_to_z
    >>> #   first_author_z_to_a, source_title_a_to_z, source_title_z_to_a
    >>> generator = (
    ...     DataFrame()
    ...     #
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     .where_records_ordered_by("global_cited_by_highest")
    ... )
    >>> df = generator.run()
    >>> df.head()
                                      raw_document_title  ...  year
    0  On the Fintech Revolution: Interpreting the Fo...  ...  2018
    1  Fintech: Ecosystem, business models, investmen...  ...  2018
    2  Digital Finance and FinTech: current research ...  ...  2017
    3  Fintech, regulatory arbitrage, and the rise of...  ...  2018
    4  The digital revolution in financial inclusion:...  ...  2017
    <BLANKLINE>
    [5 rows x 9 columns]

"""

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip


class RecordDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        data_frame = load_filtered_main_csv_zip(params=self.params)
        data_frame = data_frame.assign(_order_=range(1, len(data_frame) + 1))
        data_frame = data_frame.reset_index(drop=True)

        max_year = data_frame.year.dropna().max()

        #
        # Global citations per year
        data_frame["global_citations"] = data_frame.global_citations.astype(int)
        data_frame = data_frame.assign(
            global_citations_per_year=data_frame.global_citations.astype(float)
            / (max_year - data_frame.year + 1)
        )
        data_frame = data_frame.assign(
            global_citations_per_year=data_frame.global_citations_per_year.round(3)
        )

        #
        # Global citation score rank
        data_frame = data_frame.sort_values(
            ["global_citations", "local_citations", "year", "authors"],
            ascending=[False, False, True, True],
        )
        data_frame["rank_gcs"] = range(1, len(data_frame) + 1)

        #
        # Local citation score rank
        data_frame = data_frame.sort_values(
            ["local_citations", "global_citations", "year", "authors"],
            ascending=[False, False, True, True],
        )
        data_frame["rank_lcs"] = range(1, len(data_frame) + 1)

        #
        # Local citations per year
        data_frame["local_citations"] = data_frame.local_citations.astype(int)
        data_frame = data_frame.assign(
            local_citations_per_year=data_frame.local_citations.astype(float)
            / (max_year - data_frame.year + 1)
        )
        data_frame = data_frame.assign(
            local_citations_per_year=data_frame.local_citations_per_year.round(3)
        )

        #
        # Order
        data_frame = data_frame.sort_values("_order_", ascending=True)
        data_frame = data_frame[
            [
                "raw_document_title",
                "authors",
                "record_no",
                "document_type",
                "rank_gcs",
                "global_citations",
                "rank_lcs",
                "local_citations",
                "year",
            ]
        ]

        return data_frame


#
