"""
MergeColumns
===============================================================================

Smoke test:
    >>> from tm2p import Field
    >>> from tm2p.ingest.oper import MergeColumns
    >>> (
    ...     MergeColumns()
    ...     .with_source_fields(
    ...         (
    ...             Field.AUTHKW_RAW,
    ...             Field.IDXKW_RAW,
    ...         )
    ...     )
    ...     .with_target_field(Field.USR0)
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    162

    >>> from tm2p.ingest.oper import Query
    >>> (
    ...     Query()
    ...     .with_query_expression("SELECT USR0 FROM database LIMIT 10;")
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .run()
    ... )
                                                    USR0
    0  Digital transformation; FinTech; FinTech gover...
    1                                               None
    2  Artificial intelligence; Banking industry sect...
    3  China; Fintech; G38; Intention to use; L16; M1...
    4  Fintech; Green environmental index; Green fina...
    5  Banking; Dark side; FinTech; FinTech developer...
    6  CO2 emissions; Carbon; Carbon taxes; China; De...
    7  Fintech; carbon emission; corporate carbon emi...
    8  'current; A comparative study; Comparative ana...
    9  COVID-19; Carbon; Carbon emission: green finan...

/Volumes/GitHub/tm2p



"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.datab._intern.oper.merge_col import merge_columns
from tm2p.ingest.extr._helpers._protected_fields import PROTECTED_FIELDS


class MergeColumns(
    ParamsMixin,
):
    """:meta private:"""

    def run(self) -> int:

        for source_field in self.params.source_fields:
            if source_field == self.params.target_field:
                raise ValueError(
                    f"Source and target fields must differ (got `{source_field}`)"
                )

        if self.params.target_field in PROTECTED_FIELDS:
            raise ValueError(
                f"Cannot overwrite protected field `{self.params.target_field}`"
            )

        return merge_columns(
            sources=self.params.source_fields,
            target=self.params.target_field,
            root_directory=self.params.root_directory,
        )
